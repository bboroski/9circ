using System.Buffers.Binary;

namespace NineCirc.Core.Ipc;

/// <summary>
/// 32-byte little-endian frame header shared by C#, Swift and Ruby.
/// Layout: magic[4], version[u16], type[u16], sequence[u64],
/// payloadLength[u32], crc32[u32], monotonicNanoseconds[u64].
/// Payload bytes remain in shared memory; only this header is decoded.
/// </summary>
public readonly record struct IpcFrameHeader(
    ushort Version, ushort Type, ulong Sequence,
    uint PayloadLength, uint Crc32, ulong MonotonicNanoseconds);

public static class SharedMemoryProtocol
{
    public const int HeaderSize = 32;
    public const ushort CurrentVersion = 1;
    private static ReadOnlySpan<byte> Magic => "9CIR"u8;

    public static IpcFrameHeader Read(ReadOnlySpan<byte> source)
    {
        if (source.Length < HeaderSize) throw new ArgumentException("Incomplete IPC header.");
        if (!source[..4].SequenceEqual(Magic)) throw new InvalidDataException("Invalid IPC magic.");

        var version = BinaryPrimitives.ReadUInt16LittleEndian(source[4..6]);
        if (version != CurrentVersion) throw new InvalidDataException($"Unsupported IPC version: {version}.");

        return new IpcFrameHeader(
            version,
            BinaryPrimitives.ReadUInt16LittleEndian(source[6..8]),
            BinaryPrimitives.ReadUInt64LittleEndian(source[8..16]),
            BinaryPrimitives.ReadUInt32LittleEndian(source[16..20]),
            BinaryPrimitives.ReadUInt32LittleEndian(source[20..24]),
            BinaryPrimitives.ReadUInt64LittleEndian(source[24..32]));
    }

    public static void Write(Span<byte> destination, in IpcFrameHeader header)
    {
        if (destination.Length < HeaderSize) throw new ArgumentException("Destination is too small.");
        if (header.Version != CurrentVersion) throw new ArgumentOutOfRangeException(nameof(header));
        Magic.CopyTo(destination);
        BinaryPrimitives.WriteUInt16LittleEndian(destination[4..6], header.Version);
        BinaryPrimitives.WriteUInt16LittleEndian(destination[6..8], header.Type);
        BinaryPrimitives.WriteUInt64LittleEndian(destination[8..16], header.Sequence);
        BinaryPrimitives.WriteUInt32LittleEndian(destination[16..20], header.PayloadLength);
        BinaryPrimitives.WriteUInt32LittleEndian(destination[20..24], header.Crc32);
        BinaryPrimitives.WriteUInt64LittleEndian(destination[24..32], header.MonotonicNanoseconds);
    }

    public static bool ValidatePayload(in IpcFrameHeader header, ReadOnlySpan<byte> payload)
    {
        if (payload.Length != header.PayloadLength) return false;
        return ComputeCrc32(payload) == header.Crc32;
    }

    public static uint ComputeCrc32(ReadOnlySpan<byte> payload)
    {
        var crc = 0xFFFFFFFFu;
        foreach (var value in payload)
        {
            crc ^= value;
            for (var bit = 0; bit < 8; bit++)
                crc = (crc & 1) != 0 ? (crc >> 1) ^ 0xEDB88320u : crc >> 1;
        }
        return ~crc;
    }
}
