#!/usr/bin/env ruby
# frozen_string_literal: true

# One-shot migration (edoxen TODO.updates/02): promote scalar
# `committee: ISO/TC 184/SC 4` to an inline Body in every
# meetings/*.yaml:
#
#   committee:
#     code: ISO/TC 184/SC 4
#     name:
#     - spelling: eng
#       value: ISO/TC 184/SC 4
#
# Pure single-line text replacement (no YAML round-trip) so the
# rest of each file — formatting, wrapping, key order — is
# untouched and the diff stays minimal. Idempotent: files that
# no longer carry the scalar form are skipped.

OLD = "committee: ISO/TC 184/SC 4\n"
NEW = "committee:\n" \
      "  code: ISO/TC 184/SC 4\n" \
      "  name:\n" \
      "  - spelling: eng\n" \
      "    value: ISO/TC 184/SC 4\n"

migrated = 0
skipped = 0
Dir.glob(File.expand_path("../meetings/*.yaml", __dir__)).sort.each do |path|
  text = File.read(path)
  occurrences = text.scan(OLD).size
  if occurrences.zero?
    skipped += 1
    next
  end
  abort "ABORT: #{path} contains #{occurrences} scalar committee lines" unless occurrences == 1

  File.write(path, text.sub(OLD, NEW))
  migrated += 1
end

puts "Migrated: #{migrated}, skipped (already migrated): #{skipped}"
