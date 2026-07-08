import { venueDisplay, venueFlag } from './unlocodes.mjs'

export const URN_BASE = 'urn:iso:tc:184:sc:4'

const PUA_BULLET_REPLACEMENTS = [
  [//g, '•'],
  [//g, '‣'],
  [//g, '▸'],
  [//g, ' '],
]

export function normalizeSnippet(rawMessage) {
  if (!rawMessage) return ''
  let snippet = rawMessage
  for (const [pattern, replacement] of PUA_BULLET_REPLACEMENTS) {
    snippet = snippet.replace(pattern, replacement)
  }
  snippet = snippet
    .replace(/\n+/g, ' ')
    .replace(/  +/g, ' ')
    .trim()
  if (snippet.length > 200) {
    snippet = snippet.substring(0, 197) + '...'
  }
  return snippet
}

export function isAcclamation(identifier) {
  return String(identifier).includes('-acclaim-')
}

export function deriveDisplayTitle(loc, acclamation) {
  if (loc.title) return loc.title
  if (acclamation && loc.actions && loc.actions.length > 0) return 'Acclamation'
  return ''
}

// Extract the first (eng) Localization from a v2.1 Decision.
// Returns an empty object if no localizations exist.
function primaryLocalization(decision) {
  if (!decision.localizations || decision.localizations.length === 0) return {}
  return decision.localizations[0]
}

export function buildResolutionRecord(decision, sourceFile, metadata) {
  const loc = primaryLocalization(decision)
  const idList = decision.identifier || []
  const identifier = idList.length > 0 ? String(idList[0].number) : ''
  const acclamation = isAcclamation(identifier)

  // v2.1 metadata.date is a single date string (not an array).
  const meetingDate = metadata.date || ''
  const year = meetingDate ? meetingDate.substring(0, 4) : ''

  return {
    id: identifier,
    urn: `${URN_BASE}:decision:${identifier}`,
    title: deriveDisplayTitle(loc, acclamation),
    subject: loc.subject || '',
    year,
    venue: venueDisplay(metadata.city),
    venue_flag: venueFlag(metadata.city),
    city: metadata.city || '',
    country_code: metadata.country_code || '',
    source_file: sourceFile,
    meeting_urn: `${URN_BASE}:meeting:${sourceFile}`,
    source_title: metadata.title || '',
    meeting_date: meetingDate,
    is_acclamation: acclamation,
    actions: loc.actions || [],
    considerations: loc.considerations || [],
    approvals: loc.approvals || [],
    dates: decision.dates || [],
    snippet: normalizeSnippet(loc.actions && loc.actions.length > 0 ? loc.actions[0].message : '')
  }
}

export function sortResolutions(a, b) {
  if (a.meeting_date !== b.meeting_date) {
    return (b.meeting_date || '').localeCompare(a.meeting_date || '')
  }
  const aIsAcc = isAcclamation(a.id)
  const bIsAcc = isAcclamation(b.id)
  if (!aIsAcc && !bIsAcc) {
    const aNum = parseFloat(a.id)
    const bNum = parseFloat(b.id)
    if (!isNaN(aNum) && !isNaN(bNum)) return bNum - aNum
    return (b.id || '').localeCompare(b.id || '')
  }
  if (aIsAcc !== bIsAcc) return aIsAcc ? 1 : -1
  return (a.id || '').localeCompare(b.id || '')
}
