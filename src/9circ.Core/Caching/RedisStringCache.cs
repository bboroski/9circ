using StackExchange.Redis;

namespace NineCirc.Core.Caching;

public sealed class RedisStringCache : IAsyncDisposable
{
    private readonly ConnectionMultiplexer _connection;
    private readonly IDatabase _database;

    private RedisStringCache(ConnectionMultiplexer connection)
    {
        _connection = connection;
        _database = connection.GetDatabase();
    }

    public static async Task<RedisStringCache> ConnectAsync(
        string connectionString, CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(connectionString);
        cancellationToken.ThrowIfCancellationRequested();
        var connection = await ConnectionMultiplexer.ConnectAsync(connectionString).ConfigureAwait(false);
        return new RedisStringCache(connection);
    }

    public async Task<string?> GetAsync(string key)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(key);
        var value = await _database.StringGetAsync(key).ConfigureAwait(false);
        return value.HasValue ? value.ToString() : null;
    }

    public Task<bool> SetAsync(string key, string value, TimeSpan ttl)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(key);
        ArgumentNullException.ThrowIfNull(value);
        if (ttl <= TimeSpan.Zero) throw new ArgumentOutOfRangeException(nameof(ttl));
        return _database.StringSetAsync(key, value, ttl);
    }

    public async ValueTask DisposeAsync() => await _connection.DisposeAsync().ConfigureAwait(false);
}
