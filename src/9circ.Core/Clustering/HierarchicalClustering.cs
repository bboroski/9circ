namespace NineCirc.Core.Clustering;

/// <summary>
/// Agglomerative centroid-linkage clustering. Centroids and scratch spans are caller-owned,
/// so repeated merges do not allocate managed memory. Complexity is O(n^2 * dimensions).
/// </summary>
public static class HierarchicalClustering
{
    public static int Cluster(
        ReadOnlySpan<float> points, int pointCount, int dimensions, int targetClusterCount,
        Span<float> centroids, Span<int> sizes, Span<int> labels,
        Span<byte> active, Span<int> remap)
    {
        if (pointCount < 0) throw new ArgumentOutOfRangeException(nameof(pointCount));
        if (dimensions <= 0) throw new ArgumentOutOfRangeException(nameof(dimensions));
        if (targetClusterCount < 1 || targetClusterCount > Math.Max(pointCount, 1))
            throw new ArgumentOutOfRangeException(nameof(targetClusterCount));
        var matrixLength = checked(pointCount * dimensions);
        if (points.Length < matrixLength || centroids.Length < matrixLength ||
            sizes.Length < pointCount || labels.Length < pointCount ||
            active.Length < pointCount || remap.Length < pointCount)
            throw new ArgumentException("One or more caller-owned workspace spans are too small.");

        if (pointCount == 0) return 0;
        foreach (var value in points[..matrixLength])
            if (!float.IsFinite(value))
                throw new ArgumentException("Input coordinates must be finite.", nameof(points));

        points[..matrixLength].CopyTo(centroids);
        sizes = sizes[..pointCount];
        labels = labels[..pointCount];
        active = active[..pointCount];
        remap = remap[..pointCount];
        sizes.Fill(1);
        active.Fill(1);
        for (var i = 0; i < pointCount; i++) labels[i] = i;

        var clusterCount = pointCount;
        while (clusterCount > targetClusterCount)
        {
            var bestDistance = double.PositiveInfinity;
            var bestLeft = -1;
            var bestRight = -1;

            for (var left = 0; left < pointCount; left++)
            {
                if (active[left] == 0) continue;
                for (var right = left + 1; right < pointCount; right++)
                {
                    if (active[right] == 0) continue;
                    var distance = DistanceSquared(
                        centroids.Slice(left * dimensions, dimensions),
                        centroids.Slice(right * dimensions, dimensions));
                    if (distance < bestDistance)
                    {
                        bestDistance = distance;
                        bestLeft = left;
                        bestRight = right;
                    }
                }
            }

            if (bestLeft < 0 || bestRight < 0) break;

            var leftSize = sizes[bestLeft];
            var rightSize = sizes[bestRight];
            var totalSize = checked(leftSize + rightSize);
            var leftCentroid = centroids.Slice(bestLeft * dimensions, dimensions);
            var rightCentroid = centroids.Slice(bestRight * dimensions, dimensions);

            for (var axis = 0; axis < dimensions; axis++)
                leftCentroid[axis] =
                    (float)(((double)leftCentroid[axis] * leftSize) +
                            ((double)rightCentroid[axis] * rightSize)) / totalSize;

            sizes[bestLeft] = totalSize;
            active[bestRight] = 0;
            for (var i = 0; i < pointCount; i++)
                if (labels[i] == bestRight) labels[i] = bestLeft;

            clusterCount--;
        }

        remap.Fill(-1);
        var nextLabel = 0;
        for (var cluster = 0; cluster < pointCount; cluster++)
            if (active[cluster] != 0) remap[cluster] = nextLabel++;

        for (var point = 0; point < pointCount; point++)
            labels[point] = remap[labels[point]];

        return nextLabel;
    }

    private static double DistanceSquared(ReadOnlySpan<float> left, ReadOnlySpan<float> right)
    {
        double sum = 0;
        for (var axis = 0; axis < left.Length; axis++)
        {
            var delta = (double)left[axis] - right[axis];
            sum += delta * delta;
        }
        return sum;
    }
}
