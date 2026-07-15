#!/usr/bin/env ruby
# frozen_string_literal: true

# Migrate ISO/TC 184/SC 4 resolution YAML from v2.1 (localizations[])
# to v3.0 (per-field LocalizedString[]). Also adds URNs and fixes
# metadata.title format.
#
# Idempotent: skips files with no localizations key.
# Originals are backed up to legacy/v2.1/.

require "fileutils"
require "yaml"
require "date"

SRC_DIR = File.expand_path("../plenary", __dir__)
LEGACY_DIR = File.expand_path("../legacy/v2.1", __dir__)

def ls_array(value, lang)
  return nil if value.nil?
  [{ "spelling" => lang, "value" => value.to_s }]
end

def migrate_consideration(c, lang)
  out = {}
  out["type"] = c["type"] if c["type"]
  out["date_effective"] = c["date_effective"] if c["date_effective"]
  out["message"] = ls_array(c["message"], lang) if c["message"]
  out
end

def migrate_action(a, lang)
  out = {}
  out["type"] = a["type"] if a["type"]
  out["date_effective"] = a["date_effective"] if a["date_effective"]
  out["message"] = ls_array(a["message"], lang) if a["message"]
  out
end

def migrate_approval(a, lang)
  out = {}
  out["type"] = a["type"] if a["type"]
  out["degree"] = a["degree"] if a["degree"]
  out["date"] = a["date"] if a["date"]
  out["message"] = ls_array(a["message"], lang) if a["message"]
  out
end

def migrate_decision(d)
  locs = Array(d["localizations"])
  without_loc = d.reject { |k, _| k == "localizations" }
  return without_loc if locs.empty?

  first = locs.first || {}
  lang = first["language_code"] || "eng"

  out = {}
  out["identifier"] = d["identifier"] if d["identifier"]
  out["kind"] = d["kind"] if d["kind"]
  out["status"] = d["status"] if d["status"]
  out["doi"] = d["doi"] if d["doi"]
  out["urn"] = d["urn"] if d["urn"]
  out["dates"] = d["dates"] if d["dates"]
  out["categories"] = d["categories"] if d["categories"]

  loc = locs.first
  out["title"] = ls_array(loc["title"], lang) if loc["title"]
  out["subject"] = ls_array(loc["subject"], lang) if loc["subject"]
  out["message"] = ls_array(loc["message"], lang) if loc["message"]
  out["considering"] = ls_array(loc["considering"], lang) if loc["considering"]
  out["considerations"] = Array(loc["considerations"]).map { |c| migrate_consideration(c, lang) } if loc["considerations"]
  out["approvals"] = Array(loc["approvals"]).map { |a| migrate_approval(a, lang) } if loc["approvals"]
  out["actions"] = Array(loc["actions"]).map { |a| migrate_action(a, lang) } if loc["actions"]
  out
end

count = 0
Dir.glob(File.join(SRC_DIR, "*.yaml")).sort.each do |path|
  source = File.read(path)
  data = YAML.safe_load(source, permitted_classes: [Date, Time])
  next unless data.is_a?(Hash) && data["decisions"]

  has_localizations = Array(data["decisions"]).any? { |d| d.is_a?(Hash) && d["localizations"] }

  meta = data["metadata"]
  if meta&.dig("title").is_a?(String)
    meta["title"] = [{ "spelling" => "eng", "value" => meta["title"] }]
  end

  if has_localizations
    backup_path = File.join(LEGACY_DIR, File.basename(path))
    FileUtils.mkdir_p(File.dirname(backup_path))
    FileUtils.cp(path, backup_path) unless File.exist?(backup_path)
  end

  data["decisions"] = Array(data["decisions"]).map do |d|
    migrated = migrate_decision(d)
    unless migrated["urn"]
      number = migrated["identifier"]&.first&.fetch("number", nil)
      migrated["urn"] = "urn:iso:tc184:sc4:resolution:#{number}" if number
    end
    migrated
  end

  File.write(path, YAML.dump(data))
  count += 1
end

puts "Migrated #{count} file(s)"
