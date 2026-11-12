using System.Diagnostics;
using System.Diagnostics.Metrics;

namespace NineCirc.Core.Telemetry;

public static class NineCircTelemetry
{
    public const string InstrumentationName = "9circ";
    public static readonly ActivitySource Activities = new(InstrumentationName);
    public static readonly Meter Meter = new(InstrumentationName, "0.1.0");

    public static readonly Counter<long> ClusterRuns =
        Meter.CreateCounter<long>("ninecirc.cluster.runs");
    public static readonly Histogram<double> ClusterDuration =
        Meter.CreateHistogram<double>("ninecirc.cluster.duration", "ms");
    public static readonly Histogram<double> BufferOccupancy =
        Meter.CreateHistogram<double>("ninecirc.buffer.occupancy", "percent");
    public static readonly Counter<long> ComponentReloads =
        Meter.CreateCounter<long>("ninecirc.component.reloads");
    public static readonly Histogram<double> MotivationIndex =
        Meter.CreateHistogram<double>("ninecirc.motivation.index");
    public static readonly Counter<long> GeneratedPatchProposals =
        Meter.CreateCounter<long>("ninecirc.creative.patch.proposals");
}
