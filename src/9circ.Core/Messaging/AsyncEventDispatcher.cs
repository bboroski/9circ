using System.Threading.Channels;

namespace NineCirc.Core.Messaging;

/// <summary>
/// Bounded single-consumer event dispatcher with asynchronous backpressure.
/// This is an in-process transport adapter; distributed deployments should bridge it to
/// a broker and preserve the same event envelope/ordering requirements.
/// </summary>
public sealed class AsyncEventDispatcher<T> : IAsyncDisposable
{
    private readonly Channel<T> _channel;
    private readonly Func<T, CancellationToken, ValueTask> _handler;
    private readonly CancellationTokenSource _shutdown = new();
    private readonly Task _worker;
    private int _completed;

    public AsyncEventDispatcher(
        int capacity,
        Func<T, CancellationToken, ValueTask> handler)
    {
        if (capacity <= 0) throw new ArgumentOutOfRangeException(nameof(capacity));
        _handler = handler ?? throw new ArgumentNullException(nameof(handler));
        _channel = Channel.CreateBounded<T>(new BoundedChannelOptions(capacity)
        {
            FullMode = BoundedChannelFullMode.Wait,
            SingleReader = true,
            SingleWriter = false,
            AllowSynchronousContinuations = false
        });
        _worker = RunAsync();
    }

    public Task Completion => _worker;

    public ValueTask PublishAsync(T message, CancellationToken cancellationToken = default)
    {
        ObjectDisposedException.ThrowIf(Volatile.Read(ref _completed) != 0, this);
        return _channel.Writer.WriteAsync(message, cancellationToken);
    }

    public async ValueTask CompleteAsync()
    {
        if (Interlocked.Exchange(ref _completed, 1) == 0)
            _channel.Writer.TryComplete();
        await _worker.ConfigureAwait(false);
    }

    private async Task RunAsync()
    {
        try
        {
            await foreach (var message in _channel.Reader.ReadAllAsync(_shutdown.Token).ConfigureAwait(false))
                await _handler(message, _shutdown.Token).ConfigureAwait(false);
        }
        catch (Exception exception)
        {
            _channel.Writer.TryComplete(exception);
            throw;
        }
    }

    public async ValueTask DisposeAsync()
    {
        await CompleteAsync().ConfigureAwait(false);
        _shutdown.Cancel();
        _shutdown.Dispose();
    }
}
