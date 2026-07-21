import { defineConfig } from '@edoxen/browser/config'

export default defineConfig({
  site: {
    title: 'ISO/TC 184/SC 4 Resolutions',
    // Brand lockup second line (the committee's working field, as on
    // the original site header).
    subtitle: 'Industrial data',
    description: 'Resolutions of ISO/TC 184/SC 4 — Industrial data.',
    url: 'https://isotc184sc4.github.io',
    // Deployed to GitHub Pages under the repo subpath. All routes,
    // assets, and data endpoints are prefixed from this — without it
    // every link and the CSS asset 404 at the root.
    basePath: '/resolutions-data/',
  },
  data: {
    decisions: '../plenary',
    meetings: '../meetings',
    contacts: '../_data/contacts.yaml',
    venues: '../_data/venues.yaml',
    bodies: '../_data/bodies.yaml',
    // Committee MeetingSeries — feeds the About page's committee facts.
    committee: '../_data/committee.yaml',
    // UN/LOCODE → localized city names (regenerate EN skeleton with
    // scripts/build-unlocodes.mjs; FR names are curated in-file).
    unlocodes: '../_data/unlocodes.yaml',
  },
  // This committee adopts "resolutions", not "decisions" — rename the
  // record everywhere (nav, titles, headings, stat strip, about) and
  // move the routes to /resolutions/…
  terminology: {
    decision: 'resolution',
    decisions: 'Resolutions',
  },
  decisionsSlug: 'resolutions',
  theme: {
    // Original site palette (slate ramp + ISO blue accent).
    primary: '#0f172a',
    accent: '#0061ad',
    surface: '#ffffff',
    background: '#f8fafc',
    text: '#0f172a',
    muted: '#64748b',
    border: '#e2e8f0',
    dark: {
      primary: '#f8fafc',
      accent: '#38bdf8',
      surface: '#1e293b',
      background: '#0f172a',
      text: '#f1f5f9',
      muted: '#94a3b8',
      border: '#334155',
    },
    logos: {
      primary: '/assets/iso-red.svg',
      footer: '/assets/iso-red.svg',
      favicon: '/favicon.svg',
    },
  },
  features: {
    search: true,
    timeline: true,
    urnCopy: true,
    doi: true,
    darkMode: true,
    printStyles: true,
  },
})
