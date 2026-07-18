import { defineConfig } from '@edoxen/browser/config'

export default defineConfig({
  site: {
    title: 'ISO/TC 184/SC 4 Resolutions',
    description: 'Resolutions of ISO/TC 184/SC 4 — Industrial data.',
    url: 'https://resolutions.isotc184sc4.org',
  },
  data: {
    decisions: '../plenary',
    meetings: '../meetings',
    contacts: '../_data/contacts.yaml',
    venues: '../_data/venues.yaml',
    bodies: '../_data/bodies.yaml',
  },
  theme: {
    primary: '#1e3a8a',
    accent: '#3b82f6',
    surface: '#ffffff',
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
