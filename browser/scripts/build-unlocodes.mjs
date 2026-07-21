#!/usr/bin/env node
// Regenerate _data/unlocodes.yaml: scans ../plenary/*.yaml for
// `metadata.city` UN/LOCODEs, resolves English names from the
// `unlocodes` gem dataset (UNCEFACT 2025-1 JSON-LD), and merges with
// the existing output file. Curated values ALWAYS win: any en/fr
// already in the file is preserved — re-running only adds new codes.
// (Several source-data codes resolve to the wrong place in the
// official dataset — airport codes, retired entries, nearby towns —
// so the display name is curated per meeting; see the file header.)
//
// Usage:
//   node scripts/build-unlocodes.mjs [path-to-locode.jsonld]
// Default dataset path: ~/src/mn/unlocodes/lib/unlocodes/data/locode.jsonld

import { readFileSync, writeFileSync, readdirSync, existsSync } from 'node:fs'
import { homedir } from 'node:os'
import { join } from 'node:path'

const root = new URL('..', import.meta.url).pathname
const plenaryDir = join(root, '..', 'plenary')
const outPath = join(root, '..', '_data', 'unlocodes.yaml')
const datasetPath =
  process.argv[2] ?? join(homedir(), 'src/mn/unlocodes/lib/unlocodes/data/locode.jsonld')

// 1. Collect the codes actually used by the data.
const codes = new Set()
for (const file of readdirSync(plenaryDir)) {
  if (!file.endsWith('.yaml')) continue
  const text = readFileSync(join(plenaryDir, file), 'utf8')
  for (const match of text.matchAll(/^ {2}city:\s*([A-Z]{5})\s*$/gm)) {
    codes.add(match[1])
  }
}

// 2. Resolve English names from the JSON-LD vocabulary.
const doc = JSON.parse(readFileSync(datasetPath, 'utf8'))
const graph = doc['@graph'] ?? []
const en = new Map()
for (const node of graph) {
  const code = node['rdf:value']
  if (typeof code !== 'string' || !codes.has(code.toUpperCase())) continue
  const labels = Array.isArray(node['rdfs:label']) ? node['rdfs:label'] : [node['rdfs:label']]
  const tagged = labels.find((l) => l && l['@language'] === 'en')
  const untagged = labels.find((l) => l && !l['@language'])
  const name = tagged?.['@value'] ?? untagged?.['@value']
  if (name) en.set(code.toUpperCase(), name)
}

// 3. Preserve curated names from the existing file (curation wins).
const existing = new Map()
if (existsSync(outPath)) {
  const current = readFileSync(outPath, 'utf8')
  let code = null
  for (const line of current.split('\n')) {
    const codeMatch = line.match(/^([A-Z]{5}):/)
    if (codeMatch) code = codeMatch[1]
    const enMatch = line.match(/^\s+en:\s*"?(.+?)"?\s*$/)
    const frMatch = line.match(/^\s+fr:\s*"?(.+?)"?\s*$/)
    if (code && (enMatch || frMatch)) {
      const entry = existing.get(code) ?? {}
      if (enMatch) entry.en = enMatch[1]
      if (frMatch) entry.fr = frMatch[1]
      existing.set(code, entry)
    }
  }
}

// 4. Emit.
const quote = (s) => `"${s.replace(/"/g, '\\"')}"`
const lines = [
  '# UN/LOCODE → localized place names for meeting `city` codes.',
  '# en/fr: curated display names per meeting city. New codes are seeded',
  '# from UNCEFACT 2025-1 (unlocodes gem) by scripts/build-unlocodes.mjs;',
  '# curated entries are never overwritten — delete one to re-resolve it.',
]
const missing = []
for (const code of [...codes].sort()) {
  const curated = existing.get(code)
  const nameEn = curated?.en ?? en.get(code)
  if (!nameEn) {
    missing.push(code)
    continue
  }
  lines.push(`${code}:`)
  lines.push(`  en: ${quote(nameEn)}`)
  lines.push(`  fr: ${quote(curated?.fr ?? nameEn)}`)
}
writeFileSync(outPath, `${lines.join('\n')}\n`)

console.log(`Wrote ${[...codes].length - missing.length} codes to ${outPath} (${existing.size} curated kept)`)
if (missing.length > 0) console.warn(`No dataset entry for: ${missing.join(', ')}`)
