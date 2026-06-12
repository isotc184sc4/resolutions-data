import Asciidoctor from '@asciidoctor/core'
const asciidoctor = Asciidoctor()

/**
 * Convert PDF-extracted formatting to AsciiDoc syntax:
 * - Unicode bullets (\uf0b7 •) → AsciiDoc unordered list (*)
 * - "o" sub-bullets → AsciiDoc sub-list (**)
 * - Standalone "." lines (PDF artifacts) → stripped
 * - Sequences of short lines (flattened tables) → definition list
 */
function preprocess(text: string): string {
  if (!text) return ''
  
  const lines = text.split('\n')
  const result: string[] = []
  
  // First pass: identify runs of short lines (flattened table content)
  // A "short line run" is 3+ consecutive short lines (< 60 chars)
  // But lines that are continuations of bullet items (preceded by a bullet line) are excluded
  const bulletLines = new Set<number>()
  for (let i = 0; i < lines.length; i++) {
    if (/^\uf0b7|^•/.test(lines[i])) {
      bulletLines.add(i)
      // Also mark the next line as a bullet continuation if it exists
      if (i + 1 < lines.length && lines[i + 1].trim() !== '' && !/^\uf0b7|^•/.test(lines[i + 1])) {
        bulletLines.add(i + 1)
      }
    }
  }

  const inShortRun = new Set<number>()
  let runStart = -1
  let runLen = 0
  for (let i = 0; i < lines.length; i++) {
    const trimmed = lines[i].trim()
    const isShort = trimmed.length > 0 && trimmed.length < 60 && trimmed !== '.' && !bulletLines.has(i)
    if (isShort) {
      if (runStart < 0) runStart = i
      runLen++
    } else {
      if (runLen >= 3) {
        for (let j = runStart; j < runStart + runLen; j++) inShortRun.add(j)
      }
      runStart = -1
      runLen = 0
    }
  }
  if (runLen >= 3) {
    for (let j = runStart; j < runStart + runLen; j++) inShortRun.add(j)
  }

  // Second pass: build output
  let prevWasList = false
  
  for (let i = 0; i < lines.length; i++) {
    let line = lines[i]
    const trimmed = line.trim()
    const hasBullet = /^\uf0b7|^•/.test(line)
    const hasSubBullet = /^o\s/.test(line) && !/^o\s*\n/.test(line)
    
    if (trimmed === '.') {
      continue
    }
    
    if (hasBullet) {
      line = line.replace(/^[\uf0b7•]\s*/, '')
      if (!prevWasList && result.length > 0 && result[result.length - 1].trim() !== '') {
        result.push('')
      }
      result.push('* ' + line)
      prevWasList = true
    } else if (hasSubBullet && result.length > 0) {
      line = line.replace(/^o\s+/, '')
      result.push('** ' + line)
      prevWasList = true
    } else if (inShortRun.has(i)) {
      // Part of a flattened table — render each line as a list item
      if (!prevWasList && result.length > 0 && result[result.length - 1].trim() !== '') {
        result.push('')
      }
      result.push('* ' + trimmed)
      prevWasList = true
    } else {
      result.push(line)
      prevWasList = false
    }
  }
  
  return result.join('\n')
}

export function asciidocify(text: string): string {
  if (!text) return ''
  const preprocessed = preprocess(text)
  return String(asciidoctor.convert(preprocessed, {
    standalone: false,
    safe: 'safe',
    attributes: { showtitle: false }
  }))
}
