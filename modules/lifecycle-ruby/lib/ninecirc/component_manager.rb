# frozen_string_literal: true

module NineCirc
  class ComponentManager
    Slot = Struct.new(:component, :version, :leases, :retired, keyword_init: true)

    class Lease
      attr_reader :component, :version

      def initialize(manager, slot)
        @manager = manager
        @slot = slot
        @component = slot.component
        @version = slot.version
        @released = false
      end

      def release
        return if @released

        @released = true
        @manager.__send__(:release, @slot)
      end

      def with
        yield @component
      ensure
        release
      end
    end

    def initialize(loader: NativeComponent.method(:load))
      @loader = loader
      @mutex = Mutex.new
      @active = nil
      @retired = []
      @version = 0
    end

    # Load and initialize the replacement before swapping the active slot.
    # Existing leases keep the old component alive until their work completes.
    def reload(path)
      replacement = @loader.call(path)
      old_to_close = nil

      @mutex.synchronize do
        @version += 1
        previous = @active
        @active = Slot.new(component: replacement, version: @version, leases: 0, retired: false)

        if previous
          previous.retired = true
          if previous.leases.zero?
            old_to_close = previous.component
          else
            @retired << previous
          end
        end
      end

      old_to_close&.close
      @version
    rescue StandardError
      replacement&.close
      raise
    end

    def acquire
      @mutex.synchronize do
        raise "no native component is loaded" unless @active

        @active.leases += 1
        Lease.new(self, @active)
      end
    end

    def with_component
      lease = acquire
      lease.with { |component| yield component }
    end

    def close
      to_close = @mutex.synchronize do
        slots = [@active, *@retired].compact
        raise "cannot close while native component leases are active" if slots.any? { |slot| slot.leases.positive? }

        @active = nil
        @retired.clear
        slots.map(&:component)
      end
      to_close.each(&:close)
    end

    private

    def release(slot)
      to_close = nil
      @mutex.synchronize do
        raise "component lease underflow" unless slot.leases.positive?

        slot.leases -= 1
        if slot.retired && slot.leases.zero?
          @retired.delete(slot)
          to_close = slot.component
        end
      end
      to_close&.close
    end
  end
end
