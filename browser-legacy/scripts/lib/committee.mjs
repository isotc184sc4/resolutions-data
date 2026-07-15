// Builds the committee.json record from a v2.2 MeetingSeries fixture.
//
// The MeetingSeries fixture is the single source of truth for
// committee identity, scope, chair, secretariat host, and external
// links. Site-specific extras (tagline, live ISO metrics,
// social-media URLs) live under `extensions[]` with profile
// `isotc184sc4`.
//
// Field shape matches what `browser/src/data/committee.ts` consumes;
// that file is now a thin loader around the generated JSON.

function pickExtensionAttribute(series, kind, key) {
  if (!Array.isArray(series?.extensions)) return null
  const block = series.extensions.find((e) => e && e.kind === kind)
  if (!block || !Array.isArray(block.attributes)) return null
  const attr = block.attributes.find((a) => a && a.key === key)
  if (!attr) return null
  if (attr.type === 'integer') return attr.intValue
  if (attr.type === 'float') return attr.floatValue
  if (attr.type === 'boolean') return attr.booleanValue
  return attr.value
}

function displayName(name) {
  if (!name) return ''
  if (typeof name === 'string') return name
  if (name.formatted) return name.formatted
  return [name.prefix, name.given, name.additional, name.family, name.suffix]
    .filter((s) => s != null && String(s).trim() !== '')
    .join(' ')
}

export function buildCommitteeRecord(series) {
  if (!series) throw new Error('MeetingSeries fixture is required')

  // Secretariat host: hosts[] with role: secretariat.
  const secretariatHost = (series.hosts || []).find((h) => h && h.role === 'secretariat')
  const secretariatName = secretariatHost?.ref
    ? `${secretariatHost.ref.toUpperCase()} (Secretariat)`
    : pickExtensionAttribute(series, 'committee_facts', 'secretariat') || ''

  // Chair: carried by `contact` (v2.2 Contact; was `organizer` pre-v2.2).
  const chairName = series.contact ? displayName(series.contact.name) : ''

  return {
    name: series.name || '',
    title: pickExtensionAttribute(series, 'committee_facts', 'title') || '',
    tagline: pickExtensionAttribute(series, 'committee_facts', 'tagline') || '',
    scope: series.description || '',
    secretariat: secretariatName,
    chair: chairName,
    established: pickExtensionAttribute(series, 'committee_facts', 'established_year') || null,
    publishedStandards: pickExtensionAttribute(series, 'committee_facts', 'published_standards') || null,
    participatingMembers: pickExtensionAttribute(series, 'committee_facts', 'participating_members') || null,
    observingMembers: pickExtensionAttribute(series, 'committee_facts', 'observing_members') || null,
    links: {
      iso: pickExtensionAttribute(series, 'external_links', 'iso_home') || '',
      isoCommittee: pickExtensionAttribute(series, 'external_links', 'iso_committee') || '',
      committeeSite: pickExtensionAttribute(series, 'external_links', 'committee_site') || '',
      linkedin: pickExtensionAttribute(series, 'external_links', 'linkedin') || '',
      github: pickExtensionAttribute(series, 'external_links', 'github') || '',
    },
  }
}
