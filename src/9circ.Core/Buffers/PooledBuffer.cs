using System.Buffers;
using System.Runtime.CompilerServices;

namespace NineCirc.Core.Buffers;

/// <summary>
/// Thread-safe, idempotently disposable lease over a shared ArrayPool buffer.
/// A Span/Memory obtained from this owner must not be used after Dispose.
/// </summary>
public sealed class PooledBuffer<T> : IMemoryOwner<T>
{
    private T[]? _array;
    public int Length { get; }

    private PooledBuffer(T[] array, int length)
    {
        _array = array;
        Length = length;
    }

    public static PooledBuffer<T> Rent(int minimumLength)
    {
        if (minimumLength < 0) throw new ArgumentOutOfRangeException(nameof(minimumLength));
        return new PooledBuffer<T>(ArrayPool<T>.Shared.Rent(Math.Max(1, minimumLength)), minimumLength);
    }

    public Memory<T> Memory =>
        (Volatile.Read(ref _array) ?? throw new ObjectDisposedException(nameof(PooledBuffer<T>)))
            .AsMemory(0, Length);

    public Span<T> Span => Memory.Span;

    public void Dispose()
    {
        var array = Interlocked.Exchange(ref _array, null);
        if (array is not null)
            ArrayPool<T>.Shared.Return(array, clearArray: RuntimeHelpers.IsReferenceOrContainsReferences<T>());
    }
}
