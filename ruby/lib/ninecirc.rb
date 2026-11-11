require "digest"
require "fiddle"
require "json"

module Ninecirc
  MAXIMUM_INPUT_BYTES = 64 * 1024 * 1024
  ABI_VERSION = 1
  ZERO_RUN_LIMIT = 4096

  class NativeScanner
    def initialize
      library = ENV.fetch("NINECIRC_NATIVE_LIBRARY", "libninecirc_core.so")
      @handle = Fiddle.dlopen(library)
      @abi_version = Fiddle::Function.new(
        @handle["ninecirc_abi_version"], [], Fiddle::TYPE_INT
      )
      @scan = Fiddle::Function.new(
        @handle["ninecirc_scan"],
        [Fiddle::TYPE_VOIDP, Fiddle::TYPE_SIZE_T, Fiddle::TYPE_VOIDP],
        Fiddle::TYPE_INT
      )
      actual = @abi_version.call
      raise "Unsupported 9circ native ABI version: #{actual}" unless actual == ABI_VERSION
    rescue Fiddle::DLError => error
      raise "Unable to load the 9circ native library (#{library}): #{error.message}"
    end

    def scan(bytes)
      input = Fiddle::Pointer.malloc([bytes.bytesize, 1].max)
      output = Fiddle::Pointer.malloc(48)
      input[0, bytes.bytesize] = bytes
      status = @scan.call(input, bytes.bytesize, output)
      raise "9circ native scan failed with code #{status}" unless status.zero?

      status_field, flags, byte_count, zero_bytes, line_count, fnv64, longest_zero_run =
        output[0, 48].unpack("l<L<Q<Q<Q<Q<Q<")
      raise "9circ native result contains status #{status_field}" unless status_field.zero?

      {
        byteCount: byte_count,
        zeroBytes: zero_bytes,
        lineCount: line_count,
        longestZeroRun: longest_zero_run,
        fnv64: format("%016x", fnv64),
        utf8Valid: (flags & 1) != 0,
        containsNul: (flags & 2) != 0
      }
    ensure
      input&.free
      output&.free
    end
  end

  def self.diagnostics(metrics)
    findings = []
    if metrics[:byteCount].zero?
      findings << finding(
        "9circ-empty-input", "Structural Defects", "warning",
        "The input file is empty.", "The file contains zero bytes.",
        "Review whether an empty artifact is intentional.",
        "Re-scan after the expected source content is restored."
      )
    end

    if metrics[:containsNul]
      findings << finding(
        "9circ-binary-content", "Content Classification", "info",
        "The input contains NUL bytes and is classified as binary.",
        "At least one byte has the value 0x00.",
        "Use a format-aware binary verifier before interpreting this artifact as source code.",
        "Compare the detected format with the declared input type."
      )
    elsif !metrics[:utf8Valid]
      findings << finding(
        "9circ-invalid-utf8", "Structural Defects", "warning",
        "The input is not valid UTF-8 text.",
        "The byte sequence cannot be decoded as UTF-8.",
        "Confirm the declared text encoding; do not rewrite bytes automatically.",
        "Validate the file with its documented encoding."
      )
    end

    if metrics[:longestZeroRun] >= ZERO_RUN_LIMIT
      findings << finding(
        "9circ-zero-run", "Resource Constraints", "warning",
        "A long contiguous run of zero bytes was detected.",
        "At least 4096 consecutive bytes are zero.",
        "Inspect the relevant binary section or padding boundary.",
        "Re-scan and compare the zero-run metric after an approved change."
      )
    end
    findings
  end

  def self.analyze(input_name, bytes, scanner: NativeScanner.new)
    metrics = scanner.scan(bytes)
    {
      schemaVersion: 1,
      product: "9circ",
      input: input_name,
      sha256: Digest::SHA256.hexdigest(bytes),
      classification: (metrics[:containsNul] || !metrics[:utf8Valid]) ? "binary" : "text",
      metrics: metrics.reject { |key, _value| key == :containsNul },
      diagnostics: diagnostics(metrics),
      stages: %w[Import Identification Analysis Verification Diagnosis Report]
    }
  end

  def self.run(arguments, stdout: $stdout, stderr: $stderr)
    unless arguments.length == 2 && arguments[0] == "scan"
      stderr.puts("Usage: 9circ scan <file>")
      return 64
    end

    path = File.expand_path(arguments[1])
    raise "Input file does not exist: #{path}" unless File.file?(path)
    raise "Symbolic links are not accepted as direct input." if File.symlink?(path)
    raise "Input exceeds the 64 MiB safety limit." if File.size(path) > MAXIMUM_INPUT_BYTES

    bytes = File.binread(path)
    report = analyze(File.basename(path), bytes)
    stdout.puts(JSON.pretty_generate(report))
    0
  rescue StandardError => error
    stderr.puts("9circ: #{error.message}")
    1
  end

  def self.finding(id, category, severity, description, cause, recommendation, verification)
    {
      id: id,
      category: category,
      severity: severity,
      description: description,
      cause: cause,
      recommendation: recommendation,
      verification: verification
    }
  end
  private_class_method :finding
end
