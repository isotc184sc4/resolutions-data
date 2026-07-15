#!/usr/bin/env ruby
# frozen_string_literal: true

# Validate plenary/*.yaml directly against the canonical edoxen-model
# JSON Schema — independent of the `edoxen` gem. Useful when the gem
# version is in flux or you want to check data against a model checkout
# that is newer than the pinned gem.

require "yaml"
require "json_schemer"
require "pathname"

ROOT = Pathname.new(File.expand_path("..", __dir__))
SCHEMA_PATH = ENV.fetch("EDOXEN_SCHEMA",
                        File.expand_path("../../edoxen/edoxen-model/schema/decision-collection.yaml", ROOT))
GLOB = ENV.fetch("GLOB", File.join(ROOT, "plenary", "*.yaml"))

abort "Schema not found: #{SCHEMA_PATH}" unless File.exist?(SCHEMA_PATH)

schema = JSONSchemer.schema(YAML.load_file(SCHEMA_PATH))

total = 0
invalid = 0
error_tally = Hash.new(0)

Dir.glob(GLOB).sort.each do |path|
  total += 1
  data = YAML.load_file(path)
  errors = schema.validate(data).to_a
  next if errors.empty?

  invalid += 1
  puts "INVALID #{File.basename(path)}"
  errors.first(10).each do |err|
    pointer = err["data_pointer"]
    schema_loc = err["schema_pointer"]
    msg = err.fetch("error") do
      err["errors"]&.values&.first&.dig("error") || err.inspect
    end
    puts "  at #{pointer.empty? ? "<root>" : pointer}  (schema #{schema_loc})"
    puts "    #{msg}"
    error_tally["#{pointer} :: #{schema_loc}"] += 1
  end
  puts "  ... (#{errors.size} total)" if errors.size > 10
end

puts
puts "Schema:   #{SCHEMA_PATH}"
puts "Files:    #{total}"
puts "Invalid:  #{invalid}"

if invalid.positive?
  puts
  puts "Top error patterns:"
  error_tally.sort_by { |_, n| -n }.first(15).each do |key, n|
    puts "  #{n}×  #{key}"
  end
  exit 1
end
