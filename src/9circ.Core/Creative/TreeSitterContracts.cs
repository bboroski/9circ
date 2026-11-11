namespace NineCirc.Core.Creative;

public enum SourceLanguage { CSharp, Ruby, Swift }

public sealed record SyntaxDeclaration(
    string Kind, string Name, int StartByte, int EndByte, string NormalizedBody);

public sealed record ParsedSource(
    SourceLanguage Language, IReadOnlyList<SyntaxDeclaration> Declarations);

/// <summary>
/// Adapter boundary for native Tree-sitter grammars. Language workers implement this contract
/// and return byte-ranged syntax nodes; parser instances must be isolated per worker/thread.
/// </summary>
public interface ITreeSitterParser
{
    SourceLanguage Language { get; }
    ParsedSource Parse(ReadOnlyMemory<byte> source);
}

public sealed record RefactorProposal(
    SourceLanguage Language,
    string SourceSymbol,
    string SimilarSymbol,
    double Similarity,
    string Rationale,
    bool RequiresSandboxEvaluation = true);

public static class CodeEvolutionPlanner
{
    /// <summary>
    /// Proposes reviewable refactors from AST declaration bodies. It never writes source files
    /// or executes generated code; all proposals require a sandboxed evaluator and human approval.
    /// </summary>
    public static IReadOnlyList<RefactorProposal> Suggest(
        ParsedSource source, double minimumSimilarity = 0.72)
    {
        ArgumentNullException.ThrowIfNull(source);
        if (!double.IsFinite(minimumSimilarity) || minimumSimilarity is < 0 or > 1)
            throw new ArgumentOutOfRangeException(nameof(minimumSimilarity));

        var declarations = source.Declarations;
        var proposals = new List<RefactorProposal>();

        for (var left = 0; left < declarations.Count; left++)
        {
            for (var right = left + 1; right < declarations.Count; right++)
            {
                var a = declarations[left];
                var b = declarations[right];
                if (a.Kind != b.Kind || a.Name == b.Name) continue;

                var similarity = Similarity(a.NormalizedBody, b.NormalizedBody);
                if (similarity < minimumSimilarity) continue;

                proposals.Add(new RefactorProposal(
                    source.Language, a.Name, b.Name, similarity,
                    "Similar AST declaration bodies may share a helper or common implementation."));
            }
        }

        return proposals.OrderByDescending(item => item.Similarity).ToArray();
    }

    private static double Similarity(string left, string right)
    {
        var a = Tokenize(left);
        var b = Tokenize(right);
        if (a.Count == 0 || b.Count == 0) return 0;

        var intersection = a.Count(token => b.Contains(token));
        var union = a.Count + b.Count - intersection;
        return union == 0 ? 0 : (double)intersection / union;
    }

    private static HashSet<string> Tokenize(string source) =>
        source.Split((char[]?)null, StringSplitOptions.RemoveEmptyEntries)
              .Select(token => token.Trim())
              .Where(token => token.Length > 1)
              .ToHashSet(StringComparer.Ordinal);
}
