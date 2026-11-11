# frozen_string_literal: true

require "ffi"

module NineCirc
  class NativeComponent
    API = Class.new do
      extend FFI::Library
    end

    attr_reader :path

    def self.load(path)
      raise ArgumentError, "native module path is required" if path.nil? || path.empty?
      raise LoadError, "native module does not exist: #{path}" unless File.file?(path)

      api = Class.new do
        extend FFI::Library
        ffi_lib path
        attach_function :ninecirc_component_init, [], :int
        attach_function :ninecirc_component_shutdown, [], :void
      end

      instance = allocate
      instance.send(:initialize_native, path, api)
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
      result = @api.ninecirc_component_init
      raise LoadError, "native component init returned #{result}" unless result.zero?
    end
  end
end
