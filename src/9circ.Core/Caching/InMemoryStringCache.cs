using System.Collections.Concurrent;

namespace NineCirc.Core.Caching;

/// <summary>Bounded process-local TTL cache. It is an optimization, never the source of truth.</summary>
public sealed class InMemoryStringCache
{
    private sealed record Entry(string Value, long ExpiresAtTicks);
    private readonly ConcurrentDictionary<string, Entry> _entries = new(StringComparer.Ordinal);
    private readonly int _maximumEntries;

    public InMemoryStringCache(int maximumEntries = 4096)
    {
        if (maximumEntries < 1) throw new ArgumentOutOfRangeException(nameof(maximumEntries));
        _maximumEntries = maximumEntries;
    }

    public bool TryGet(string key, out string? value)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(key);
        value = null;
        if (!_entries.TryGetValue(key, out var entry)) return false;
        if (DateTime.UtcNow.Ticks >= entry.ExpiresAtTicks)
        {
            _entries.TryRemove(key, out _);
            return false;
        }
        value = entry.Value;
        return true;
    }

    public void Set(string key, string value, TimeSpan ttl)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(key);
        ArgumentNullException.ThrowIfNull(value);
        if (ttl <= TimeSpan.Zero) throw new ArgumentOutOfRangeException(nameof(ttl));

        if (_entries.Count >= _maximumEntries && !_entries.ContainsKey(key))
        {
            foreach (var candidate in _entries.Keys.Take(Math.Max(1, _maximumEntries / 16)))
                _entries.TryRemove(candidate, out _);
        }

        var expiresAt = DateTime.UtcNow.Add(ttl).Ticks;
        _entries[key] = new Entry(value, expiresAt);
    }

    public bool Remove(string key) => _entries.TryRemove(key, out _);
    public int Count => _entries.Count;
}
