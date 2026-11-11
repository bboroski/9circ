using Npgsql;

namespace NineCirc.Core.Storage;

public sealed class PostgresDocumentStore : IAsyncDisposable
{
    private readonly NpgsqlDataSource _dataSource;

    public PostgresDocumentStore(string connectionString)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(connectionString);
        _dataSource = NpgsqlDataSource.Create(connectionString);
    }

    public async Task SaveAsync(
        Guid id, string source, string content, CancellationToken cancellationToken = default)
    {
        const string sql = """
            INSERT INTO ninecirc_documents (id, source, content, updated_at)
            VALUES (@id, @source, @content, now())
            ON CONFLICT (id) DO UPDATE
            SET source = EXCLUDED.source,
                content = EXCLUDED.content,
                updated_at = now();
            """;

        await using var command = _dataSource.CreateCommand(sql);
        command.Parameters.AddWithValue("id", id);
        command.Parameters.AddWithValue("source", source);
        command.Parameters.AddWithValue("content", content);
        await command.ExecuteNonQueryAsync(cancellationToken);
    }

    public async ValueTask DisposeAsync() => await _dataSource.DisposeAsync();
}
