using Npgsql;

namespace NineCirc.Core.Storage;

public sealed record ArtifactManifest(
    Guid Id, string Component, string Version, string Sha256, string StorageUri, DateTimeOffset CreatedAt);

public sealed class PostgresArtifactRegistry : IAsyncDisposable
{
    private readonly NpgsqlDataSource _dataSource;

    public PostgresArtifactRegistry(string connectionString)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(connectionString);
        _dataSource = NpgsqlDataSource.Create(connectionString);
    }

    public async Task RegisterAsync(
        ArtifactManifest artifact, CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(artifact.Component);
        ArgumentException.ThrowIfNullOrWhiteSpace(artifact.Version);
        ArgumentException.ThrowIfNullOrWhiteSpace(artifact.StorageUri);
        if (artifact.Sha256.Length != 64 || artifact.Sha256.Any(c => !Uri.IsHexDigit(c)))
            throw new ArgumentException("SHA-256 must contain exactly 64 hexadecimal characters.", nameof(artifact));

        const string sql = """
            INSERT INTO ninecirc_artifacts (id, component, version, sha256, storage_uri, created_at)
            VALUES (@id, @component, @version, @sha256, @uri, @created)
            ON CONFLICT (component, version) DO NOTHING;
            """;
        await using var command = _dataSource.CreateCommand(sql);
        command.Parameters.AddWithValue("id", artifact.Id);
        command.Parameters.AddWithValue("component", artifact.Component);
        command.Parameters.AddWithValue("version", artifact.Version);
        command.Parameters.AddWithValue("sha256", artifact.Sha256.ToLowerInvariant());
        command.Parameters.AddWithValue("uri", artifact.StorageUri);
        command.Parameters.AddWithValue("created", artifact.CreatedAt);
        await command.ExecuteNonQueryAsync(cancellationToken).ConfigureAwait(false);
    }

    public async Task<ArtifactManifest?> GetLatestAsync(
        string component, CancellationToken cancellationToken = default)
    {
        const string sql = """
            SELECT id, component, version, sha256, storage_uri, created_at
            FROM ninecirc_artifacts
            WHERE component = @component
            ORDER BY created_at DESC
            LIMIT 1;
            """;
        await using var command = _dataSource.CreateCommand(sql);
        command.Parameters.AddWithValue("component", component);
        await using var reader = await command.ExecuteReaderAsync(cancellationToken).ConfigureAwait(false);
        if (!await reader.ReadAsync(cancellationToken).ConfigureAwait(false)) return null;

        return new ArtifactManifest(
            reader.GetGuid(0), reader.GetString(1), reader.GetString(2),
            reader.GetString(3).Trim(), reader.GetString(4), reader.GetFieldValue<DateTimeOffset>(5));
    }

    public ValueTask DisposeAsync() => _dataSource.DisposeAsync();
}
