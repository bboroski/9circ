namespace NineCirc.Core.Motivation;

public sealed record MotivationDiagnostic(
    bool IsBalanced, double CpuPressure, double MemoryPressure,
    double PrioritySpread, IReadOnlyList<string> Alerts);

public static class MotivationDiagnostics
{
    public static MotivationDiagnostic Evaluate(
        IReadOnlyList<MotivationNodeSnapshot> nodes,
        double cpuPressure, double memoryPressure)
    {
        ArgumentNullException.ThrowIfNull(nodes);
        if (!double.IsFinite(cpuPressure) || cpuPressure is < 0 or > 1 ||
            !double.IsFinite(memoryPressure) || memoryPressure is < 0 or > 1)
            throw new ArgumentOutOfRangeException(nameof(cpuPressure), "Pressure must be in the [0,1] range.");

        var alerts = new List<string>();
        var spread = nodes.Count == 0
            ? 0
            : nodes.Max(node => node.Priority) - nodes.Min(node => node.Priority);

        if (cpuPressure >= 0.85) alerts.Add("CPU pressure is critically high.");
        if (memoryPressure >= 0.85) alerts.Add("Memory pressure is critically high.");
        if (spread >= 2.5) alerts.Add("Motivation priority spread indicates possible resource imbalance.");
        if (nodes.Any(node => !double.IsFinite(node.Priority) || node.Priority < 0))
            alerts.Add("A motivation node contains an invalid priority.");

        return new MotivationDiagnostic(alerts.Count == 0, cpuPressure, memoryPressure, spread, alerts);
    }
}
