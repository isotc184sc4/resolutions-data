// Loads committee metadata from the generated `committee.json` (built
// by `scripts/build-data.mjs` from the v2.2 MeetingSeries fixture
// `_data/committee.yaml`). Replaces the hard-coded committee object.
//
// Single source of truth: the MeetingSeries fixture. Update the
// fixture, rebuild, and the site picks up the new facts.

import committeeRaw from '../../public/data/committee.json'

export interface Committee {
  name: string
  title: string
  tagline: string
  scope: string
  secretariat: string
  chair: string
  established: number | null
  publishedStandards: number | null
  participatingMembers: number | null
  observingMembers: number | null
  links: {
    iso: string
    isoCommittee: string
    committeeSite: string
    linkedin: string
    github: string
  }
}

export const committee: Committee = committeeRaw as Committee
