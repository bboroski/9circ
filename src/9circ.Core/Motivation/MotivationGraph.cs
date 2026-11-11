namespace NineCirc.Core.Motivation;

public readonly record struct RuntimeFeedback(
    double ThroughputPerSecond,
    double CpuPressure,
    double MemoryPressure,
    double ErrorRate,
    double LatencyMilliseconds);

public readonly record struct MotivationNodeSnapshot(
    string Id, double Weight, double Priority, long Executions, double LastReward);

/// <summary>
/// A bounded, thread-safe dependency graph. Scores influence scheduling hints only;
/// they never bypass operating-system scheduling or resource quotas.
/// </summary>
public sealed class MotivationGraph
{
    private sealed class Node
    {
        public required string Id { get; init; }
        public double Weight;
        public long Executions;
        public double LastReward;
        public readonly List<(string Target, double Strength)> Dependencies = [];
    }

    private readonly object _gate = new();
    private readonly Dictionary<string, Node> _nodes = new(StringComparer.Ordinal);
    private readonly double _learningRate;

    public MotivationGraph(double learningRate = 0.05)
    {
        if (!double.IsFinite(learningRate) || learningRate <= 0 || learningRate > 1)
            throw new ArgumentOutOfRangeException(nameof(learningRate));
        _learningRate = learningRate;
    }

    public void AddNode(string id, double initialWeight = 1.0)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(id);
        if (!double.IsFinite(initialWeight)) throw new ArgumentOutOfRangeException(nameof(initialWeight));
        lock (_gate)
        {
            if (_nodes.ContainsKey(id)) throw new InvalidOperationException($"Node '{id}' already exists.");
            _nodes.Add(id, new Node { Id = id, Weight = Math.Clamp(initialWeight, 0.0, 10.0) });
        }
    }

    public void AddDependency(string source, string target, double strength = 1.0)
    {
        if (!double.IsFinite(strength) || strength < 0 || strength > 1)
            throw new ArgumentOutOfRangeException(nameof(strength));
        lock (_gate)
        {
            if (!_nodes.TryGetValue(source, out var node) || !_nodes.ContainsKey(target))
                throw new KeyNotFoundException("Both dependency nodes must exist.");
            if (node.Dependencies.Any(edge => edge.Target == target))
                throw new InvalidOperationException("Dependency already exists.");
            node.Dependencies.Add((target, strength));
        }
    }

    public void ApplyFeedback(RuntimeFeedback feedback)
    {
        Validate(feedback);
        lock (_gate)
        {
            var pressure = Math.Clamp((feedback.CpuPressure + feedback.MemoryPressure) / 2.0, 0, 1);
            var quality = Math.Clamp(1.0 - feedback.ErrorRate, 0, 1);
            var latencyPenalty = Math.Clamp(feedback.LatencyMilliseconds / 10_000.0, 0, 1);
            var throughputReward = Math.Clamp(Math.Log(1.0 + feedback.ThroughputPerSecond) / 12.0, 0, 1);
            var reward = (0.55 * quality + 0.45 * throughputReward) *
                         (1.0 - 0.35 * pressure) * (1.0 - 0.25 * latencyPenalty);

            foreach (var node in _nodes.Values)
            {
                var dependencyBoost = 0.0;
                foreach (var edge in node.Dependencies)
                    dependencyBoost += _nodes[edge.Target].Weight * edge.Strength;

                var target = Math.Clamp(reward + Math.Min(dependencyBoost, 2.0) * 0.1, 0, 1.2);
                node.Weight = Math.Clamp(
                    node.Weight + _learningRate * (target - node.Weight) - _learningRate * pressure * 0.05,
                    0.0, 10.0);
                node.LastReward = reward;
            }
        }
    }

    public void RecordExecution(string id)
    {
        lock (_gate)
        {
            if (!_nodes.TryGetValue(id, out var node)) throw new KeyNotFoundException(id);
            node.Executions++;
        }
    }

    public double GetPriority(string id)
    {
        lock (_gate)
        {
            if (!_nodes.TryGetValue(id, out var node)) throw new KeyNotFoundException(id);
            return node.Weight;
        }
    }

    public MotivationNodeSnapshot[] Snapshot()
    {
        lock (_gate)
            return _nodes.Values
                .Select(node => new MotivationNodeSnapshot(
                    node.Id, node.Weight, node.Weight, node.Executions, node.LastReward))
                .OrderByDescending(node => node.Priority)
                .ToArray();
    }

    private static void Validate(RuntimeFeedback f)
    {
        if (!double.IsFinite(f.ThroughputPerSecond) || f.ThroughputPerSecond < 0 ||
            !double.IsFinite(f.CpuPressure) || f.CpuPressure < 0 ||
            !double.IsFinite(f.MemoryPressure) || f.MemoryPressure < 0 ||
            !double.IsFinite(f.ErrorRate) || f.ErrorRate < 0 ||
            !double.IsFinite(f.LatencyMilliseconds) || f.LatencyMilliseconds < 0)
            throw new ArgumentOutOfRangeException(nameof(f), "Feedback metrics must be finite and non-negative.");
    }
}
