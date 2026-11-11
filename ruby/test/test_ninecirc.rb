require "minitest/autorun"
require_relative "../lib/ninecirc"

class NinecircTest < Minitest::Test
  def setup
    @scanner = Ninecirc::NativeScanner.new
  end

  def test_native_binary_metrics
    metrics = @scanner.scan("A\x00B\n".b)
    assert_equal 4, metrics[:byteCount]
    assert_equal 1, metrics[:zeroBytes]
    assert_equal 1, metrics[:lineCount]
    assert_equal true, metrics[:containsNul]
  end

  def test_empty_input
    metrics = @scanner.scan("".b)
    assert_equal 0, metrics[:byteCount]
    assert_equal true, metrics[:utf8Valid]
  end

  def test_sha256_and_report_schema
    report = Ninecirc.analyze("sample.txt", "abc".b, scanner: @scanner)
    assert_equal "9circ", report[:product]
    assert_equal "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad", report[:sha256]
    assert_equal "text", report[:classification]
    assert_equal 1, report[:schemaVersion]
  end
end
