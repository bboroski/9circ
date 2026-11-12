# frozen_string_literal: true

require "ffi"

module NineCirc
  class NativeComponent
    ABI_VERSION = 1

    attr_reader :path

    def self.load(path)
      raise ArgumentError, "native module path is required" if path.nil? || path.empty?
      raise LoadError, "native module path must be absolute" unless File.absolute_path(path) == path
      raise LoadError, "native module does not exist: #{path}" unless File.file?(path)

      resolved = File.realpath(path)
      allowed_root = File.realpath(ENV.fetch("NINECIRC_NATIVE_DIR", File.dirname(resolved)))
      unless resolved.start_with?(File.join(allowed_root, ""))
        raise LoadError, "native module path is outside NINECIRC_NATIVE_DIR"
      end

      api = Class.new do
        extend FFI::Library
        ffi_lib resolved
        attach_function :ninecirc_component_abi_version, [], :uint32
        attach_function :ninecirc_component_init, [], :int
        attach_function :ninecirc_component_shutdown, [], :void
      end

      instance = allocate
      instance.send(:initialize_native, resolved, api)
      instance
    end

    def close
      return if @closed

      @api.ninecirc_component_shutdown
      @closed = true
    end

    private

    def initialize_native(path, api)
      @path = path.freeze
      @api = api
      @closed = false
      abi = @api.ninecirc_component_abi_version
      raise LoadError, "native ABI #{abi} does not match #{ABI_VERSION}" unless abi == ABI_VERSION

      result = @api.ninecirc_component_init
      unless result.zero?
        @api.ninecirc_component_shutdown
        @closed = true
        raise LoadError, "native component init returned #{result}"
      end
    end
  end
end
