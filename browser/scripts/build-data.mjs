import fs from 'node:fs';
import path from 'node:path';
import yaml from 'js-yaml';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PLENARY_DIR = path.resolve(__dirname, '../../plenary');
const OUTPUT_DIR = path.resolve(__dirname, '../public/data');
const OUTPUT_FILE = path.join(OUTPUT_DIR, 'resolutions.json');

function main() {
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  const files = fs.readdirSync(PLENARY_DIR).filter(f => f.endsWith('.yaml') || f.endsWith('.yml'));
  let allResolutions = [];

  for (const file of files) {
    const filePath = path.join(PLENARY_DIR, file);
    const content = fs.readFileSync(filePath, 'utf8');
    
    let parsed;
    try {
      parsed = yaml.load(content);
    } catch (e) {
      console.error(`Error parsing ${file}:`, e.message);
      continue;
    }

    if (!parsed || !parsed.resolutions) continue;

    const source_file = file.replace(/\.ya?ml$/, '');
    const metadata = parsed.metadata || {};
    const source_title = metadata.title || '';
    const venue = metadata.venue || '';
    const datesInfo = metadata.dates || [];
    const meeting_date = datesInfo.length > 0 ? datesInfo[0].start : '';
    const year = meeting_date ? meeting_date.substring(0, 4) : '';

    for (const res of parsed.resolutions) {
      const identifier = String(res.identifier);
      const isAcclamation = identifier.includes('-acclaim-');

      // Find the first action message for the snippet
      let snippet = '';
      if (res.actions && res.actions.length > 0 && res.actions[0].message) {
        snippet = res.actions[0].message
          // Replace PUA bullet chars (from PDF extraction) with standard bullets
          .replace(/\uf0b7/g, '•')
          .replace(/\uf0be/g, '‣')
          .replace(/\uf0d8/g, '▸')
          .replace(/\uf020/g, ' ')
          // Collapse newlines into spaces for snippet display
          .replace(/\n+/g, ' ')
          // Collapse multiple spaces
          .replace(/  +/g, ' ')
          .trim();
        if (snippet.length > 200) {
          snippet = snippet.substring(0, 197) + '...';
        }
      }

      // For acclamations, derive display_title from the thanks message
      let display_title = res.title || '';
      if (isAcclamation && !display_title && res.actions && res.actions.length > 0) {
        display_title = 'Acclamation';
      }

      allResolutions.push({
        id: identifier,
        title: display_title,
        subject: res.subject || '',
        year: year,
        venue: venue,
        source_file: source_file,
        source_title: source_title,
        meeting_date: meeting_date,
        is_acclamation: isAcclamation,
        actions: res.actions || [],
        considerations: res.considerations || [],
        approvals: res.approvals || [],
        dates: res.dates || [],
        snippet: snippet
      });
    }
  }

  // Sort by meeting_date desc, then identifier desc
  // Acclamations (e.g. "202510-acclaim-01") sort right after their parent
  allResolutions.sort((a, b) => {
    if (a.meeting_date !== b.meeting_date) {
      return (b.meeting_date || '').localeCompare(a.meeting_date || '');
    }
    // Acclamations use YYYYMM-acclaim-NN format — sort by full ID
    const aIsAcc = a.id.includes('-acclaim-');
    const bIsAcc = b.id.includes('-acclaim-');
    if (!aIsAcc && !bIsAcc) {
      // Both regular resolutions — sort by numeric identifier desc
      const aNum = parseFloat(a.id);
      const bNum = parseFloat(b.id);
      if (!isNaN(aNum) && !isNaN(bNum)) return bNum - aNum;
      return (b.id || '').localeCompare(a.id);
    }
    // Regular resolutions before acclamations, then acclamations by NN
    if (aIsAcc !== bIsAcc) return aIsAcc ? 1 : -1;
    return (a.id || '').localeCompare(b.id);
  });

  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(allResolutions), 'utf8');
  console.log(`Successfully built ${allResolutions.length} resolutions to ${OUTPUT_FILE}`);
}

main();
