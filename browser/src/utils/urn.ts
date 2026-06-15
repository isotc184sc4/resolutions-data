/**
 * URN construction for archive resources.
 *
 * Per RFC 5141, ISO TC-level resources manage their own URN namespace.
 * The committee has chosen `urn:iso:tc:184:sc:4` as the base.
 */

const URN_BASE = 'urn:iso:tc:184:sc:4'

export function buildResolutionUrn(id: string): string {
  return `${URN_BASE}:resolution:${id}`
}

export function buildMeetingUrn(sourceFile: string): string {
  return `${URN_BASE}:meeting:${sourceFile}`
}
