# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

ISO/TC 184/SC 4 resolution data (1,456 decisions across 86 plenary YAML files,
1984–2026) plus an Astro-based browser that publishes to GitHub Pages. The YAML
is the source of truth; the browser is derived from it.

## Pipeline

```
plenary/*.yaml  ──[ edoxen validate ]──▶  valid YAML
                  │
                  └─[ @edoxen/browser build (Astro) ]─▶  browser/dist  ─▶  GitHub Pages
```

- `plenary/*.yaml` — Decision data in edoxen format. Validated by CI on every push/PR.
- `meetings/*.yaml` — Meeting side of the same data (one per plenary, references Decisions by identifier).
- `browser/` — Astro SPA built on `@edoxen/browser`. Consumes `plenary/*.yaml` directly via `edoxen.config.ts → data.decisions`.
- `browser-legacy/` — Previous Vue/Vite SPA. Preserved for reference; do not modify.
- `reference-docs/` — Original PDF sources (e.g., `N4118_Cumulative Resolutions…`). Never delete; these are the irreplaceable provenance.

## Common commands

Validate YAML (the only test that matters for data correctness):
```sh
bundle install
bundle exec edoxen validate "plenary/*.yaml"                # all files
bundle exec edoxen validate plenary/plenary-1984-07-gaithersburg-washington-dc-usa.yaml
bundle exec edoxen normalize "plenary/*.yaml" --inplace     # reformat
```

Schema-direct validation (independent of the pinned `edoxen` gem — useful when
the gem version is stale or you want to test against a newer model checkout):
```sh
ruby scripts/validate-against-schema.rb                     # plenary/*.yaml vs decision-collection.yaml
EDOXEN_SCHEMA=../../edoxen/edoxen-model/schema/meeting.yaml \
  GLOB="$(pwd)/meetings/*.yaml" ruby scripts/validate-against-schema.rb
```
The canonical schemas live off-repo at `../../edoxen/edoxen-model/schema/`
(`decision-collection.yaml`, `meeting.yaml`). They enforce
`additionalProperties: false` at every object — a pass means tight conformance.

Browser dev/build (run inside `browser/`):
```sh
pnpm install
pnpm dev       # Vite/Astro dev server with HMR
pnpm build     # type-check (vue-tsc) + Astro build → browser/dist
pnpm preview
```

## URN scheme

```
urn:iso:tc184:sc4:resolution:{number}        # e.g. urn:iso:tc184:sc4:resolution:1142
urn:iso:tc184:sc4:meeting:{source_basename}  # e.g. urn:iso:tc184:sc4:meeting:plenary-1984-07
```

RFC 5141 delegates URN management for TC resources to the TC itself — that's why
this isn't under `urn:iso:std:`. Both Decision and Meeting YAMLs carry their URN
in the `urn:` field.

## Data format — current state

All 86 plenary files are on edoxen **v1.0** shape (the canonical model version;
the script that produced them is `scripts/migrate-to-v3.rb`, where `v3` is an
internal staging name, not the model version):

- Top-level key is `decisions:` (NOT `resolutions:`).
- Every translatable string is **per-field Localized**: `[{ spelling: eng, value: "…" }]`.
  There is no `localizations: []` block; each field (`title`, `subject`, `message`,
  `actions[].message`, etc.) carries its own language tags. Always verbose —
  single-language data uses the same array shape as multi-language.
- `metadata.title` is `[{ spelling, value }]`.
- Each Decision has a `urn:` field.
- Meeting YAMLs use `scheduled_date_range:`, `venues: [{ kind: physical, unlocode, country_code }]`,
  and a `decisions:` array of `{ prefix, number }` references.

**`README.adoc` is stale** — its example shows the v1.0 shape (`resolutions:`,
plain string messages, no `urn:`). Trust the real files in `plenary/`, not the
README example, when reasoning about the wire format.

## Migration tooling pattern

Schema migrations are one-shot Ruby scripts in `scripts/`, named `migrate_to_vN.rb`
or `migrate-to-vN.rb` — the `vN` is an internal staging number, not the edoxen
model version (the data is on canonical model v1.0 today). The convention
(see `migrate-to-v3.rb`):

1. Read every `plenary/*.yaml` via `YAML.safe_load`.
2. Back up originals to `legacy/v{prev}/` before rewriting in place.
3. Be idempotent — skip files that don't have the "old" marker.
4. After running, re-validate with `bundle exec edoxen validate`
   (or `scripts/validate-against-schema.rb` against the latest model).

Existing scripts: `migrate_to_v2.rb`, `migrate-to-v3.rb`, `generate-meetings.rb`
(creates `meetings/*.yaml` from plenary data), `add_venue_metadata.rb`.

## Canonical edoxen model — off-repo

The canonical LutaML definitions live at `/Users/mulgogi/src/edoxen/edoxen-model/`
(checkout of `edoxen/edoxen-model`). Treat it as the source of truth for:

- Attribute names and shapes (`models/*.lutaml`).
- Wire-format constraints (`schema/decision-collection.yaml`, `schema/meeting.yaml`).
- Enum value sets and the per-field Localized convention (`CHANGELOG.adoc` for v1.0.0 / v2.2 OCP refactor notes).

The Ruby gem implementing this model is `edoxen` (unpinned in `Gemfile`).
When the model and the data disagree, the
model wins; write a migration script.

## CI

- `.github/workflows/validate.yml` — `bundle exec edoxen validate "plenary/*.yaml"` on push to main + PRs.
- `.github/workflows/deploy-pages.yml` — validates, builds `browser/` (`npm ci` + `npm run build`), deploys `browser/dist` to GitHub Pages on push to `main`.

The deploy workflow uses `npm`, but `browser/` is a pnpm project (`pnpm-lock.yaml`
is canonical). Don't accidentally commit `package-lock.json` from running `npm install` locally.

## File-naming conventions

- Plenary: `plenary-YYYY-MM-{city-state-country}.yaml` (e.g., `plenary-1984-07-gaithersburg-washington-dc-usa.yaml`).
- Meeting side: `plenary-YYYY-MM.yaml` (no location — meetings are keyed by date).
- Venue `unlocode` is a UN/LOCODE (5 chars, e.g., `USGAI` = Gaithersburg MD).
