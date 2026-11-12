using System.IO.MemoryMappedFiles;
using System.Runtime.InteropServices;

namespace NineCirc.Core.Ipc;

/// <summary>
/// File-backed view compatible with POSIX mmap users in the Swift worker.
/// The caller owns cross-process synchronization and slot ownership.
/// </summary>
public sealed unsafe class SharedMemoryRegion : IDisposable
{
    private readonly MemoryMappedFile _mapping;
    private readonly MemoryMappedViewAccessor _view;
    private byte* _pointer;
    private bool _disposed;

    public int Capacity { get; }

    public SharedMemoryRegion(string path, int capacity)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(path);
        if (capacity <= 0) throw new ArgumentOutOfRangeException(nameof(capacity));

        var stream = new FileStream(path, FileMode.OpenOrCreate, FileAccess.ReadWrite, FileShare.ReadWrite);
        try
        {
            if (stream.Length != capacity) stream.SetLength(capacity);
            _mapping = MemoryMappedFile.CreateFromFile(
                stream, null, capacity, MemoryMappedFileAccess.ReadWrite,
                HandleInheritability.None, leaveOpen: false);
            _view = _mapping.CreateViewAccessor(0, capacity, MemoryMappedFileAccess.ReadWrite);
            byte* acquired = null;
            _view.SafeMemoryMappedViewHandle.AcquirePointer(ref acquired);
            _pointer = acquired + _view.PointerOffset;
            Capacity = capacity;
        }
        catch
        {
            stream.Dispose();
            throw;
        }
    }

    public Span<byte> Bytes
    {
        get
        {
            ObjectDisposedException.ThrowIf(_disposed, this);
            return new Span<byte>(_pointer, Capacity);
        }
    }

    public void Flush()
    {
        ObjectDisposedException.ThrowIf(_disposed, this);
        _view.Flush();
    }

    public void Dispose()
    {
        if (_disposed) return;
        _disposed = true;
        if (_pointer != null)
        {
            _view.SafeMemoryMappedViewHandle.ReleasePointer();
            _pointer = null;
        }
        _view.Dispose();
        _mapping.Dispose();
        GC.SuppressFinalize(this);
    }
}
