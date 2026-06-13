// src/data/committee.ts
// SINGLE SOURCE OF TRUTH for committee metadata not derivable from resolution data.
// Update this file when committee facts change.

export const committee = {
  // Identity
  name: 'ISO/TC 184/SC 4',
  title: 'Industrial data',
  tagline: 'Standards developed for the people who need them',
  scope: 'Standardization of the content, meaning, structure, representation and quality management of information for engineered products throughout their lifecycle.',

  // Committee facts (from ISO.org — not derivable from resolution YAML)
  secretariat: 'ANSI (United States)',
  chair: 'Mr Kenneth Swope',
  established: 1984,
  publishedStandards: 822,
  participatingMembers: 21,
  observingMembers: 14,

  // External links
  links: {
    iso: 'https://www.iso.org',
    isoCommittee: 'https://www.iso.org/committee/54158.html',
    committeeSite: 'https://committee.iso.org/home/tc184sc4',
    linkedin: 'https://www.linkedin.com/company/iso-tc-184-sc-4-standards-for-industrial-data/',
    github: 'https://github.com/ISO-TC184-SC4',
  },
} as const

export type Committee = typeof committee
