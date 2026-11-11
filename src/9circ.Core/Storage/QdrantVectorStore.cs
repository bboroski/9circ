using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;

namespace NineCirc.Core.Storage;

public sealed record QdrantPoint(Guid Id, float[] Vector, IReadOnlyDictionary<string, object?>? Payload = null);

public sealed class QdrantVectorStore(HttpClient httpClient)
{
    private readonly HttpClient _http = httpClient ?? throw new ArgumentNullException(nameof(httpClient));

    public async Task EnsureCollectionAsync(
        string collection, int dimensions, CancellationToken cancellationToken = default)
    {
        ValidateCollection(collection);
        if (dimensions <= 0) throw new ArgumentOutOfRangeException(nameof(dimensions));

        using var get = await _http.GetAsync(
            $"collections/{Uri.EscapeDataString(collection)}", cancellationToken);
        if (get.IsSuccessStatusCode) return;
        if (get.StatusCode != HttpStatusCode.NotFound)
            get.EnsureSuccessStatusCode();

        using var create = await _http.PutAsJsonAsync(
            $"collections/{Uri.EscapeDataString(collection)}",
            new { vectors = new { size = dimensions, distance = "Cosine" } },
            cancellationToken);
        create.EnsureSuccessStatusCode();
    }

    public async Task UpsertAsync(
        string collection, IReadOnlyCollection<QdrantPoint> points,
        CancellationToken cancellationToken = default)
    {
        ValidateCollection(collection);
        ArgumentNullException.ThrowIfNull(points);
        if (points.Count == 0) return;

        foreach (var point in points)
            if (point.Vector.Length == 0 || point.Vector.Any(value => !float.IsFinite(value)))
                throw new ArgumentException("Every vector must be non-empty and finite.", nameof(points));

        using var response = await _http.PutAsJsonAsync(
            $"collections/{Uri.EscapeDataString(collection)}/points?wait=true",
            new { points = points.Select(point => new { id = point.Id, vector = point.Vector, payload = point.Payload }) },
            cancellationToken);
        response.EnsureSuccessStatusCode();
    }

    public static HttpClient CreateClient(string endpoint, string? apiKey = null)
    {
        var client = new HttpClient { BaseAddress = new Uri(endpoint, UriKind.Absolute), Timeout = TimeSpan.FromSeconds(15) };
        if (!string.IsNullOrWhiteSpace(apiKey))
            client.DefaultRequestHeaders.Add("api-key", apiKey);
        client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
        return client;
    }

    private static void ValidateCollection(string collection)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(collection);
        if (collection.Length > 128 || collection.Any(c => !(char.IsAsciiLetterOrDigit(c) || c is '_' or '-')))
            throw new ArgumentException("Collection names may contain only ASCII letters, digits, '_' and '-'.", nameof(collection));
    }
}
