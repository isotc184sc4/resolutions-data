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
      const isAcclamation = identifier.includes('-acclamation-');

      // Find the first action message for the snippet
      let snippet = '';
      if (res.actions && res.actions.length > 0 && res.actions[0].message) {
        snippet = res.actions[0].message;
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
  // Acclamations (e.g. "1195-acclamation-1") sort right after their parent
  allResolutions.sort((a, b) => {
    if (a.meeting_date !== b.meeting_date) {
      return (b.meeting_date || '').localeCompare(a.meeting_date || '');
    }
    // Extract base identifier (numeric part before any "-acclamation-")
    const aBase = a.id.split('-acclamation-')[0];
    const bBase = b.id.split('-acclamation-')[0];
    const aNum = parseFloat(aBase);
    const bNum = parseFloat(bBase);
    if (!isNaN(aNum) && !isNaN(bNum) && aNum !== bNum) {
      return bNum - aNum;
    }
    if (aBase !== bBase) {
      return (bBase || '').localeCompare(aBase || '');
    }
    // Same base — acclamations sort after parent, in order
    const aAcc = a.id.includes('-acclamation-') ? parseInt(a.id.split('-acclamation-')[1]) : 0;
    const bAcc = b.id.includes('-acclamation-') ? parseInt(b.id.split('-acclamation-')[1]) : 0;
    return aAcc - bAcc;
  });

  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(allResolutions), 'utf8');
  console.log(`Successfully built ${allResolutions.length} resolutions to ${OUTPUT_FILE}`);
}

main();
