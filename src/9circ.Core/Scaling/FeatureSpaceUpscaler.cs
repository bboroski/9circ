namespace NineCirc.Core.Scaling;

/// <summary>Fills missing values in a row-major feature matrix and normalizes vectors.</summary>
public static class FeatureSpaceUpscaler
{
    public static void InterpolateMissing(
        Span<float> matrix, int rows, int columns, float missingValue = float.NaN)
    {
        if (rows < 0) throw new ArgumentOutOfRangeException(nameof(rows));
        if (columns <= 0) throw new ArgumentOutOfRangeException(nameof(columns));
        if (matrix.Length < checked(rows * columns))
            throw new ArgumentException("Matrix buffer is too small.", nameof(matrix));

        for (var column = 0; column < columns; column++)
        {
            var first = -1;
            for (var row = 0; row < rows; row++)
            {
                var value = matrix[row * columns + column];
                if (IsKnown(value, missingValue)) { first = row; break; }
            }

            if (first < 0)
            {
                for (var row = 0; row < rows; row++)
                    matrix[row * columns + column] = 0f;
                continue;
            }

            var previous = first;
            var firstValue = matrix[first * columns + column];
            for (var row = 0; row < first; row++)
                matrix[row * columns + column] = firstValue;

            for (var row = first + 1; row < rows; row++)
            {
                var currentValue = matrix[row * columns + column];
                if (!IsKnown(currentValue, missingValue)) continue;

                var left = matrix[previous * columns + column];
                var gap = row - previous;
                for (var step = 1; step < gap; step++)
                {
                    var t = (float)step / gap;
                    matrix[(previous + step) * columns + column] = left + ((currentValue - left) * t);
                }
                previous = row;
            }

            var lastValue = matrix[previous * columns + column];
            for (var row = previous + 1; row < rows; row++)
                matrix[row * columns + column] = lastValue;
        }
    }

    public static bool NormalizeL2(Span<float> vector)
    {
        double sum = 0;
        foreach (var value in vector)
        {
            if (!float.IsFinite(value)) return false;
            sum += value * value;
        }

        if (sum <= double.Epsilon) return false;
        var inverse = (float)(1.0 / Math.Sqrt(sum));
        for (var i = 0; i < vector.Length; i++) vector[i] *= inverse;
        return true;
    }

    private static bool IsKnown(float value, float missingValue) =>
        float.IsFinite(value) &&
        (float.IsNaN(missingValue) ? !float.IsNaN(value) : value != missingValue);
}
