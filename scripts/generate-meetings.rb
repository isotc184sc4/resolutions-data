#!/usr/bin/env ruby
# frozen_string_literal: true

# Generate edoxen v3.0 meeting YAML files from ISO/TC 184/SC 4
# resolution metadata. Each plenary file contains meeting info
# (date, city, country_code, title) in its metadata block.

require "yaml"
require "date"

SRC_DIR = File.expand_path("../plenary", __dir__)
OUT_DIR = File.expand_path("../meetings", __dir__)

require "fileutils"
FileUtils.mkdir_p(OUT_DIR)

count = 0
Dir.glob(File.join(SRC_DIR, "*.yaml")).sort.each do |path|
  data = YAML.safe_load(File.read(path), permitted_classes: [Date, Time])
  next unless data.is_a?(Hash) && data["decisions"]

  meta = data["metadata"] || {}
  date_str = meta["date"].to_s
  year_month = date_str.match(/(\d{4}-\d{2})/)&.captures&.first
  year = date_str.match(/(\d{4})/)&.captures&.first
  next unless year_month

  title_val = meta["title"].is_a?(Array) ? meta["title"].first&.fetch("value", nil) : meta["title"].to_s

  end_date = nil
  title_val.to_s.match(/(\d{4}),.*?--\s*(\w+\s+\d+,?\s*\d{4})/)&.captures&.last&.tap { |m| end_date = Date.parse(m.to_s)&.iso8601 rescue nil }

  meeting = {
    "identifier" => [{ "prefix" => "ISO/TC 184/SC 4", "number" => year_month }],
    "urn" => "urn:iso:tc184:sc4:meeting:plenary-#{year_month}",
    "type" => "plenary",
    "status" => "completed",
    "scheduled_date_range" => { "start" => date_str, "end" => end_date || date_str },
    "committee" => {
      "code" => "ISO/TC 184/SC 4",
      "name" => [{ "spelling" => "eng", "value" => "ISO/TC 184/SC 4" }],
    },
    "title" => meta["title"],
  }
  meeting["city"] = meta["city"] if meta["city"]
  meeting["country_code"] = meta["country_code"] if meta["country_code"]

  meeting["venues"] = [{
    "kind" => "physical",
    "country_code" => meta["country_code"],
  }.compact]
  meeting["venues"][0]["unlocode"] = meta["city"] if meta["city"]

  decisions = Array(data["decisions"]).map do |d|
    id = d["identifier"]&.first
    next unless id
    { "prefix" => id["prefix"], "number" => id["number"] }
  end.compact
  meeting["decisions"] = decisions if decisions.any?

  out_file = File.join(OUT_DIR, "plenary-#{year_month}.yaml")
  File.write(out_file, YAML.dump(meeting))
  count += 1
end

puts "Generated #{count} meeting file(s)"
