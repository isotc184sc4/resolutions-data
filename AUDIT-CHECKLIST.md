# Resolution Data Audit Checklist

## Scope

- 86 YAML files in `plenary/`
- 1304 resolutions (1178 numbered + 126 acclamations)
- 3112 total actions
- Source: PDF extraction (column-major, multi-page)

## Known Failure Patterns

### PATTERN A: Empty `resolves` as paragraph separators (343 instances, 236 resolutions)

The PDF has paragraph breaks that were extracted as separate `resolves` actions with message `.`.

**Symptom**: A resolution has multiple actions, one or more being:
```yaml
- type: resolves
  message: .
```

**Expected**: These `.` actions should be removed. The text before and after should be ONE action with a blank line between paragraphs.

**Example**: Resolution 355 has 8 actions. Some are real (instructs, asks) but several are `resolves: .` serving as paragraph breaks.

**Audit method**: For each resolution with empty resolves, read the FULL resolution and determine:
1. Is the `.` a paragraph break within one logical action? → Merge into the preceding action
2. Is the `.` a separator between genuinely distinct actions? → Remove (the next action already has its own type)
3. Is the `.` truly meaningless? → Remove

---

### PATTERN B: Split actions — single content split across multiple actions (51+ instances)

A resolution body that is one continuous text was split into 2-3 actions because the PDF had column breaks or page breaks.

**Symptom**: 
- An action message ends mid-sentence (e.g., "...for the associated", "...requests")
- The next action message starts with continuation text (e.g., "SC 4 projects:", "the SC 4 handbook...")

**Expected**: The split actions should be merged into ONE action with the complete text.

**Audit method**: For each resolution with multiple actions, check:
1. Does the first action's message end mid-sentence?
2. Does the next action's message start with continuation content (not "SC 4 resolves/instructs/...")?
3. If both: merge into one action, preserve the FIRST action's type

---

### PATTERN C: Column-major table data flattened as plain text (~129 instances)

Multi-column PDF tables were extracted column-by-column into a flat list of lines. Row structure is lost.

**Symptom**: Action message contains a sequence of short lines that look like table cells (names, project numbers, identifiers) with no table markup.

**Expected**: Either:
- Reconstruct the table as AsciiDoc `|===` table (if column structure can be determined)
- OR leave as-is (honest flat text) if reconstruction is impossible without the original PDF

**Known example**: Resolution 354 was this pattern (now fixed with correct AsciiDoc table).

**Audit method**: For each action with PUA bullet characters or sequences of short numbered lines:
1. Read the original PDF intent (from meeting minutes context)
2. Determine if the data was tabular
3. If tabular: identify column headers and row boundaries
4. If reconstructable: write AsciiDoc table
5. If not: leave as plain text (DO NOT GUESS)

---

### PATTERN D: Bullet list encoding issues (133 instances with PUA chars, 14 with sub-bullets)

PDF bullet characters (Wingdings PUA U+E000-U+F8FF) may not be properly captured or may have been lost.

**Symptom**: 
- Action message contains PUA characters (●, •, ▪, etc.) at line starts
- Sub-bullets marked with `o ` (lowercase o + space)
- Missing bullet markers where content looks like a list

**Expected**: Each bullet item should be on its own line, with the bullet character preserved. Sub-bullets should be indented or marked distinctly.

**Audit method**: For each action with bullet characters:
1. Verify each bullet item is a complete thought (not split across lines)
2. Verify sub-bullets are correctly nested under their parent bullet
3. Verify no bullet items were merged or lost during extraction
4. Compare bullet count against expected content

---

### PATTERN E: Line wrapping artifacts

PDF text extraction often wraps lines at column boundaries, breaking words mid-sentence.

**Symptom**: A line ends without punctuation and the next line continues the same sentence.

**Example**: `TR: "Parametric representation and` / `Exchange"` — should be one line.

**Expected**: Wrapped lines should be joined into continuous text.

**Audit method**: For each multi-line message:
1. Check each line break — does it split a sentence?
2. If yes: join the lines
3. If no (genuine paragraph break): keep separate

---

### PATTERN F: Missing or incorrect action types

The Edoxen schema defines specific action types (approves, resolves, instructs, etc.). The PDF may not always clearly indicate the type.

**Symptom**: 
- Action type doesn't match the verb in the message
- Action type `request` vs `requests` inconsistency
- Action type `recognises` vs `recognizes` spelling variation

**Expected**: Action type should match the verb in the message text.

**Audit method**: For each action, verify the type matches the leading verb.

---

### PATTERN G: Date and metadata fidelity

**Symptom**: 
- Missing `dates` entries
- Wrong `kind` values
- Missing `subject` or `title` fields

**Audit method**: Spot-check against the PDF meeting minutes.

---

## File-by-File Audit Plan

### Phase 1: Automated Pre-Screen (script-assisted, not replacement for manual reading)

Generate a report per file listing:
- [ ] Resolutions with empty resolves (PATTERN A)
- [ ] Resolutions with split actions (PATTERN B)
- [ ] Resolutions with structured/tabular data (PATTERN C)
- [ ] Resolutions with bullet content (PATTERN D)
- [ ] Resolutions with potential line wrapping (PATTERN E)
- [ ] Action type inconsistencies (PATTERN F)

### Phase 2: Manual File-by-File Review

For each of the 86 files, open the YAML and READ EVERY RESOLUTION:

- [ ] **plenary-1984-07-gaithersburg-washington-dc-usa.yaml** — 4 resolutions
- [ ] **plenary-1985-03-paris-france.yaml** — 9 resolutions
- [ ] **plenary-1985-11-tokyo-japan.yaml** — 6 resolutions
- [ ] **plenary-1986-06-sydney-australia.yaml** — 4 resolutions
- [ ] **plenary-1987-03-berlin-germany.yaml** — 10 resolutions
- [ ] **plenary-1988-01-rotterdam-netherlands.yaml** — 7 resolutions
- [ ] **plenary-1988-12-tokyo-japan.yaml** — 10 resolutions
- [ ] **plenary-1989-06-san-diego-usa.yaml** — 14 resolutions
- [ ] **plenary-1989-12-hanover-germany.yaml** — 5 resolutions
- [ ] **plenary-1990-01-paris-france.yaml** — 14 resolutions
- [ ] **plenary-1990-06-gothenburg-sweden.yaml** — 18 resolutions
- [ ] **plenary-1991-02-brighton-united-kingdom.yaml** — 12 resolutions
- [ ] **plenary-1991-07-sapporo-japan.yaml** — 26 resolutions
- [ ] **plenary-1992-02-oslo-norway.yaml** — 13 resolutions
- [ ] **plenary-1992-10-dallas-tx-usa.yaml** — 32 resolutions
- [ ] **plenary-1993-02-turin-italy.yaml** — 16 resolutions
- [ ] **plenary-1993-10-berlin-germany.yaml** — 22 resolutions
- [ ] **plenary-1994-05-davos-switzerland.yaml** — 16 resolutions
- [ ] **plenary-1994-10-greenville-sc-usa.yaml** — 18 resolutions
- [ ] **plenary-1995-06-brisbane-australia.yaml** — 18 resolutions
- [ ] **plenary-1996-06-kobe-japan.yaml** — 46 resolutions
- [ ] **plenary-1996-10-toronto-canada.yaml** — 22 resolutions
- [ ] **plenary-1997-06-san-diego-ca-usa.yaml** — 33 resolutions
- [ ] **plenary-1998-06-bad-aibling-germany.yaml** — 23 resolutions ← **354 FIXED, others pending**
- [ ] **plenary-1998-10-beijing-china.yaml** — 7 resolutions
- [ ] **plenary-1999-01-san-francisco-ca-usa.yaml** — 18 resolutions
- [ ] **plenary-1999-06-lillehammer-norway.yaml** — 10 resolutions
- [ ] **plenary-1999-11-new-orleans-la-usa.yaml** — 21 resolutions
- [ ] **plenary-2000-02-melbourne-australia.yaml** — 22 resolutions
- [ ] **plenary-2000-06-bordeaux-france.yaml** — 20 resolutions
- [ ] **plenary-2000-10-charleston-sc-usa.yaml** — 13 resolutions
- [ ] **plenary-2001-02-funchal-portugal.yaml** — 21 resolutions
- [ ] **plenary-2001-06-san-francisco-usa.yaml** — 11 resolutions
- [ ] **plenary-2001-10-fukuoka-japan.yaml** — 16 resolutions
- [ ] **plenary-2002-03-myrtle-beach-sc-usa.yaml** — 10 resolutions
- [ ] **plenary-2002-06-stockholm-sweden.yaml** — 17 resolutions
- [ ] **plenary-2002-11-seoul-korea.yaml** — 17 resolutions
- [ ] **plenary-2003-03-san-diego-ca-usa.yaml** — 16 resolutions
- [ ] **plenary-2003-06-stuttgart-germany.yaml** — 18 resolutions
- [ ] **plenary-2003-10-poitiers-france.yaml** — 17 resolutions
- [ ] **plenary-2004-03-ft-lauderdale-fl-usa.yaml** — 12 resolutions
- [ ] **plenary-2004-07-bath-united-kingdom.yaml** — 18 resolutions
- [ ] **plenary-2004-10-seattle-wa-usa.yaml** — 21 resolutions
- [ ] **plenary-2005-03-lillehammer-norway.yaml** — 15 resolutions
- [ ] **plenary-2005-06-valencia-spain.yaml** — 15 resolutions
- [ ] **plenary-2005-10-hangzhou-china.yaml** — 14 resolutions
- [ ] **plenary-2006-03-vico-equense-italy.yaml** — 21 resolutions
- [ ] **plenary-2006-06-toulouse-france.yaml** — 16 resolutions
- [ ] **plenary-2006-10-hershey-pa-usa.yaml** — 15 resolutions
- [ ] **plenary-2007-03-funchal-madeira-island-portugal.yaml** — 23 resolutions
- [ ] **plenary-2007-07-ibusuki-japan.yaml** — 14 resolutions
- [ ] **plenary-2007-11-irving-dallas-tx-usa.yaml** — 10 resolutions
- [ ] **plenary-2008-03-louisville-ky-usa.yaml** — 16 resolutions
- [ ] **plenary-2008-06-sun-city-south-africa.yaml** — 12 resolutions
- [ ] **plenary-2008-11-busan-korea.yaml** — 17 resolutions
- [ ] **plenary-2009-05-parksville-british-columbia-canada.yaml** — 23 resolutions
- [ ] **plenary-2009-11-rotterdam-the-netherlands.yaml** — 20 resolutions
- [ ] **plenary-2010-06-bethlehem-pennsylvania-usa.yaml** — 15 resolutions
- [ ] **plenary-2010-10-vico-equense-italy.yaml** — 6 resolutions
- [ ] **plenary-2011-05-portland-oregon-usa.yaml** — 15 resolutions
- [ ] **plenary-2011-10-suzhou-china.yaml** — 7 resolutions
- [ ] **plenary-2012-06-stockholm-sweden.yaml** — 15 resolutions
- [ ] **plenary-2012-11-florida-usa.yaml** — 11 resolutions
- [ ] **plenary-2013-06-st-denis-france.yaml** — 13 resolutions
- [ ] **plenary-2013-11-gyeongju-korea.yaml** — 8 resolutions
- [ ] **plenary-2014-05-philadelphia-usa.yaml** — 8 resolutions
- [ ] **plenary-2014-11-belfort-france.yaml** — 13 resolutions
- [ ] **plenary-2015-04-vico-equense-italy.yaml** — 13 resolutions
- [ ] **plenary-2015-10-baltimore-usa.yaml** — 9 resolutions
- [ ] **plenary-2016-05-sapporo-japan.yaml** — 13 resolutions
- [ ] **plenary-2016-10-seattle-usa.yaml** — 9 resolutions
- [ ] **plenary-2017-05-oslo-sandvika-norway.yaml** — 17 resolutions
- [ ] **plenary-2017-11-jeju-korea.yaml** — 12 resolutions
- [ ] **plenary-2018-05-beijing-china.yaml** — 21 resolutions
- [ ] **plenary-2018-11-chicago-usa.yaml** — 18 resolutions
- [ ] **plenary-2019-05-toulouse-france.yaml** — 20 resolutions
- [ ] **plenary-2019-11-marina-del-rey-usa.yaml** — 22 resolutions
- [ ] **plenary-2020-05-virtual.yaml** — 19 resolutions
- [ ] **plenary-2020-11-virtual.yaml** — 12 resolutions
- [ ] **plenary-2021-05-virtual.yaml** — 17 resolutions
- [ ] **plenary-2021-11-virtual.yaml** — 12 resolutions
- [ ] **plenary-2022-05-virtual.yaml** — 11 resolutions
- [ ] **plenary-2022-11-hamamatsu-japan.yaml** — 12 resolutions
- [ ] **plenary-2023-06-paris-france.yaml** — 14 resolutions
- [ ] **plenary-2023-10-saratoga-springs-usa.yaml** — 12 resolutions
- [ ] **plenary-2024-05-seoul-korea.yaml** — 14 resolutions
- [ ] **plenary-2024-10-stavanger-norway.yaml** — 10 resolutions
- [ ] **plenary-2025-05-little-rock-arkansas-usa.yaml** — 16 resolutions
- [ ] **plenary-2026-05-virtual.yaml** — 10 resolutions

For EACH resolution, verify:
1. [ ] Actions are not incorrectly split (PATTERN A/B)
2. [ ] Table/structured data is correctly encoded (PATTERN C)
3. [ ] Bullet lists are complete and properly formatted (PATTERN D)
4. [ ] No line wrapping artifacts (PATTERN E)
5. [ ] Action type matches verb (PATTERN F)
6. [ ] Dates and metadata are correct (PATTERN G)

### Phase 3: Cross-Validation

- [ ] Rebuild browser and verify all fixes render correctly
- [ ] Run `bundle exec edoxen validate` on all files
- [ ] Spot-check 10+ resolutions in browser for visual correctness
- [ ] Verify total resolution count stays at 1304 (or changes are intentional)

---

## Priority Order

1. **PATTERN A** (empty resolves) — 343 instances, highest volume, easiest to detect
2. **PATTERN B** (split actions) — 51+ instances, directly affects content fidelity
3. **PATTERN C** (table data) — ~129 instances, requires manual PDF comparison
4. **PATTERN D** (bullets) — 133 instances, affects readability
5. **PATTERN E** (line wrapping) — Unknown count, requires reading each message
6. **PATTERN F** (action types) — Low count, easy fixes
7. **PATTERN G** (metadata) — Spot-check only
