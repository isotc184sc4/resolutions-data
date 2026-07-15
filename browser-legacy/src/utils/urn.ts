// Site-specific URN construction for ISO/TC 184/SC 4.
//
// The committee has chosen `urn:iso:tc:184:sc:4` as the base. Generic
// URN helpers (buildUrn, parseUrn, slugFromUrn) come from the edoxen
// library; this file holds the site-specific bits.

import { buildUrn, type Urn } from '@edoxen/edoxen'

const URN_BASE = 'urn:iso:tc:184:sc:4'

export function buildResolutionUrn(id: string): Urn {
  return buildUrn(`${URN_BASE}:resolution:${id}`)
}

export function buildMeetingUrn(sourceFile: string): Urn {
  return buildUrn(`${URN_BASE}:meeting:${sourceFile}`)
}
