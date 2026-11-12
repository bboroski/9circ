# frozen_string_literal: true

module NineCirc
  module IPCHeader
    MAGIC = "9CIR".b.freeze
    VERSION = 1
    HEADER_SIZE = 32
    FORMAT = "a4S<S<Q<L<L<Q<"

    module_function

    def encode(type:, sequence:, payload_length:, crc32:, monotonic_nanoseconds:)
      frame = [MAGIC, VERSION, type, sequence, payload_length, crc32, monotonic_nanoseconds].pack(FORMAT)
      raise RangeError, "invalid 9circ header length" unless frame.bytesize == HEADER_SIZE

      frame
    end

    def decode(frame)
      raise ArgumentError, "incomplete 9circ IPC header" unless frame && frame.bytesize >= HEADER_SIZE

      magic, version, type, sequence, payload_length, crc32, monotonic_ns =
        frame.byteslice(0, HEADER_SIZE).unpack(FORMAT)
      raise ArgumentError, "invalid 9circ IPC magic" unless magic == MAGIC
      raise ArgumentError, "unsupported 9circ IPC version" unless version == VERSION

      {
        version: version,
        type: type,
        sequence: sequence,
        payload_length: payload_length,
        crc32: crc32,
        monotonic_nanoseconds: monotonic_ns
      }.freeze
    end
  end
end
