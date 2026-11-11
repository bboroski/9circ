using NineCirc.Core.Storage;

namespace NineCirc.Core.Corpus;

public interface ITextEmbedder
{
    ValueTask<float[]> EmbedAsync(string text, CancellationToken cancellationToken = default);
}

public sealed record CorpusIngestResult(Guid DocumentId, int ChunkCount, int VectorDimensions);

/// <summary>
/// Ingests cleaned documents and vectorizes bounded text chunks. A deployment supplies
/// an ITextEmbedder backed by its approved model/runtime; no model is silently downloaded.
/// </summary>
public sealed class CorpusPipeline(
    PostgresDocumentStore documents,
    QdrantVectorStore vectors,
    ITextEmbedder embedder,
    string collection,
    int maximumTokensPerChunk = 384)
{
    private const int UpsertBatchSize = 64;

    public async Task<CorpusIngestResult> IngestAsync(
        Guid documentId, string source, string content,
        CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(source);
        ArgumentNullException.ThrowIfNull(content);
        if (maximumTokensPerChunk < 8) throw new InvalidOperationException("Chunk size must be at least 8 tokens.");

        var cleaned = Clean(content);
        await documents.SaveAsync(documentId, source, cleaned, cancellationToken).ConfigureAwait(false);

        var batch = new List<QdrantPoint>(UpsertBatchSize);
        var chunkCount = 0;
        var vectorDimensions = 0;

        foreach (var chunk in Split(cleaned, maximumTokensPerChunk))
        {
            cancellationToken.ThrowIfCancellationRequested();
            var embedding = await embedder.EmbedAsync(chunk, cancellationToken).ConfigureAwait(false);
            if (embedding.Length == 0 || embedding.Any(value => !float.IsFinite(value)))
                throw new InvalidDataException("Embedder returned an empty or non-finite vector.");

            if (vectorDimensions == 0)
            {
                vectorDimensions = embedding.Length;
                await vectors.EnsureCollectionAsync(collection, vectorDimensions, cancellationToken)
                    .ConfigureAwait(false);
            }
            else if (embedding.Length != vectorDimensions)
            {
                throw new InvalidDataException("Embedder changed vector dimensions during one document ingestion.");
            }

            batch.Add(new QdrantPoint(
                Guid.NewGuid(), embedding,
                new Dictionary<string, object?>
                {
                    ["document_id"] = documentId,
                    ["source"] = source,
                    ["chunk_index"] = chunkCount
                }));
            chunkCount++;

            if (batch.Count == UpsertBatchSize)
            {
                await vectors.UpsertAsync(collection, batch, cancellationToken).ConfigureAwait(false);
                batch.Clear();
            }
        }

        if (batch.Count > 0)
            await vectors.UpsertAsync(collection, batch, cancellationToken).ConfigureAwait(false);

        return new CorpusIngestResult(documentId, chunkCount, vectorDimensions);
    }

    private static string Clean(string input)
    {
        var filtered = input.Where(character =>
            !char.IsControl(character) || character is '\n' or '\r' or '\t').ToArray();
        return string.Join(" ", new string(filtered).Split(
            (char[]?)null, StringSplitOptions.RemoveEmptyEntries));
    }

    private static IEnumerable<string> Split(string content, int maximumTokens)
    {
        var tokens = content.Split((char[]?)null, StringSplitOptions.RemoveEmptyEntries);
        for (var start = 0; start < tokens.Length; start += maximumTokens)
            yield return string.Join(" ", tokens.Skip(start).Take(maximumTokens));
    }
}
