# ISO/TC 184/SC 4 Resolutions Browser (new)

This is the new `@edoxen/browser` (Astro) site, replacing the old
Vue/Vite browser in `browser-legacy/`.

## Status

- **Data:** All 345 YAML files are on edoxen 1.0 format (per-field
  Localized, `scheduled_date_range`, no `localizations[]`).
- **Browser:** New Astro setup with `@edoxen/browser` v0.1.6.
  Config in `edoxen.config.ts`. Theme tokens extracted from the
  legacy browser's CSS.
- **Legacy:** The old Vue/Vite browser is preserved in
  `browser-legacy/` for reference.

## What remains (for a colleague)

1. `pnpm install` in this directory.
2. `pnpm build` — verify the Astro build succeeds.
3. Refine the theme in `edoxen.config.ts` → `theme` and
   `src/styles/override.css` to match the exact colors/fonts/layout
   from `browser-legacy/src/assets/`.
4. Migrate custom features from the legacy browser:
   - AsciiDoc rendering of resolution narratives.
   - FlexSearch search (or use the built-in @edoxen/browser search).
   - Custom pages (about, committee info).
5. Remove `browser-legacy/` once the new browser is verified.
6. Update CI/CD to build from this directory.
