# frozen_string_literal: true

require "minitest/autorun"
require_relative "../lib/ninecirc"

class NineCircTests < Minitest::Test
  FakeComponent = Struct.new(:path, :closed) do
    def close
      self.closed = true
    end
  end

  def test_ipc_header_round_trip
    frame = NineCirc::IPCHeader.encode(
      type: 3, sequence: 42, payload_length: 128,
      crc32: 0xAABBCCDD, monotonic_nanoseconds: 900
    )
    header = NineCirc::IPCHeader.decode(frame)
    assert_equal 32, frame.bytesize
    assert_equal 42, header[:sequence]
    assert_equal 0xAABBCCDD, header[:crc32]
  end

  def test_hot_reload_keeps_leased_component_alive
    loader = ->(path) { FakeComponent.new(path, false) }
    manager = NineCirc::ComponentManager.new(loader: loader)
    manager.reload("v1")
    lease = manager.acquire
    old_component = lease.component

    manager.reload("v2")
    assert_equal false, old_component.closed
    lease.release
    assert_equal true, old_component.closed

    manager.close
  end
end
