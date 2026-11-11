Gem::Specification.new do |spec|
  spec.name = "ninecirc-lifecycle"
  spec.version = "0.1.0"
  spec.summary = "Native component lifecycle and hot-reload runtime for 9circ"
  spec.authors = ["9circ contributors"]
  spec.files = Dir["lib/**/*.rb"]
  spec.require_paths = ["lib"]
  spec.required_ruby_version = ">= 3.2"
  spec.add_dependency "ffi", ">= 1.16", "< 2.0"
end
