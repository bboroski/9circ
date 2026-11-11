namespace NineCirc.Core.Clustering;

/// <summary>
/// Allocation-free DBSCAN over a contiguous row-major float matrix.
/// All scratch memory is supplied by the caller; the hot path performs no managed allocations.
/// </summary>
public static unsafe class Dbscan
{
    public const int Unclassified = -2;
    public const int Noise = -1;

    public static int Cluster(
        ReadOnlySpan<float> points,
        int pointCount,
        int dimensions,
        float epsilon,
        int minPoints,
        Span<int> labels,
        Span<byte> visited,
        Span<byte> queued,
        Span<int> queue)
    {
        if (pointCount < 0) throw new ArgumentOutOfRangeException(nameof(pointCount));
        if (dimensions <= 0) throw new ArgumentOutOfRangeException(nameof(dimensions));
        var requiredLength = checked(pointCount * dimensions);
        if (points.Length < requiredLength)
            throw new ArgumentException("Input matrix is shorter than pointCount * dimensions.", nameof(points));
        if (!float.IsFinite(epsilon) || epsilon <= 0)
            throw new ArgumentOutOfRangeException(nameof(epsilon));
        if (minPoints < 1) throw new ArgumentOutOfRangeException(nameof(minPoints));
        if (labels.Length < pointCount || visited.Length < pointCount ||
            queued.Length < pointCount || queue.Length < pointCount)
            throw new ArgumentException("All workspace spans must contain at least pointCount elements.");

        if (pointCount == 0) return 0;
        foreach (var value in points[..requiredLength])
            if (!float.IsFinite(value))
                throw new ArgumentException("Input coordinates must be finite.", nameof(points));

        labels = labels[..pointCount];
        visited = visited[..pointCount];
        queued = queued[..pointCount];
        queue = queue[..pointCount];

        labels.Fill(Unclassified);
        visited.Clear();
        queued.Clear();

        var epsilonSquared = (double)epsilon * epsilon;
        var clusterId = 0;

        fixed (float* basePointer = points)
        {
            for (var point = 0; point < pointCount; point++)
            {
                if (visited[point] != 0) continue;
                visited[point] = 1;

                var tail = CollectNeighbors(
                    basePointer, pointCount, dimensions, point,
                    epsilonSquared, queue, queued);

                if (tail < minPoints)
                {
                    labels[point] = Noise;
                    continue;
                }

                labels[point] = clusterId;
                for (var i = 0; i < tail; i++) queued[queue[i]] = 1;

                var head = 0;
                while (head < tail)
                {
                    var candidate = queue[head++];

                    if (visited[candidate] == 0)
                    {
                        visited[candidate] = 1;
                        var added = CollectNeighbors(
                            basePointer, pointCount, dimensions, candidate,
                            epsilonSquared, queue[tail..], queued);

                        if (added >= minPoints)
                        {
                            for (var i = 0; i < added; i++)
                                queued[queue[tail + i]] = 1;
                            tail += added;
                        }
                    }

                    if (labels[candidate] < 0)
                        labels[candidate] = clusterId;
                }

                for (var i = 0; i < tail; i++) queued[queue[i]] = 0;
                clusterId++;
            }
        }

        return clusterId;
    }

    private static int CollectNeighbors(
        float* data, int count, int dimensions, int point,
        double epsilonSquared, Span<int> destination, Span<byte> queued)
    {
        var found = 0;
        var origin = data + (point * dimensions);

        for (var candidate = 0; candidate < count; candidate++)
        {
            if (queued[candidate] != 0) continue;

            var other = data + (candidate * dimensions);
            double distanceSquared = 0;

            for (var axis = 0; axis < dimensions; axis++)
            {
                var delta = (double)origin[axis] - other[axis];
                distanceSquared += delta * delta;
                if (distanceSquared > epsilonSquared) break;
            }

            if (distanceSquared <= epsilonSquared)
                destination[found++] = candidate;
        }

        return found;
    }
}
