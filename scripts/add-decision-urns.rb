#!/usr/bin/env ruby
# frozen_string_literal: true

# One-shot migration: add a `urn:` field to every Decision in
# plenary/*.yaml, per the repo URN scheme (see CLAUDE.md):
#
#   urn:iso:tc184:sc4:resolution:{number}
#
# The browser's decision detail pages are keyed by decision URN —
# without these, `@edoxen/browser` builds zero detail pages.
#
# Pure text insertion (no YAML round-trip): inserts
# `  urn: …` immediately after each decision identifier's
# `    number: …` line, preserving all existing formatting.
# Idempotent: decisions that already carry a `urn:` are skipped.

URN_PREFIX = "urn:iso:tc184:sc4:resolution:"

total_added = 0
total_skipped = 0

Dir.glob(File.expand_path("../plenary/*.yaml", __dir__)).sort.each do |path|
  lines = File.readlines(path, chomp: true)
  out = []
  added = 0
  skipped = 0

  lines.each_with_index do |line, i|
    out << line
    next unless line =~ /^    number: (.+)$/

    number = Regexp.last_match(1).delete_prefix("'").delete_suffix("'")
    nxt = lines[i + 1]
    if nxt&.start_with?("  urn:")
      skipped += 1
      next
    end
    out << "  urn: #{URN_PREFIX}#{number}"
    added += 1
  end

  File.write(path, out.join("\n") + "\n") if added.positive?
  total_added += added
  total_skipped += skipped
end

puts "URNs added: #{total_added}, already present: #{total_skipped}"
