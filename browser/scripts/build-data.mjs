import fs from 'node:fs';
import path from 'node:path';
import yaml from 'js-yaml';
import { fileURLToPath } from 'node:url';
import { buildResolutionRecord, sortResolutions } from './lib/transforms.mjs';
import { buildCommitteeRecord } from './lib/committee.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PLENARY_DIR = path.resolve(__dirname, '../../plenary');
const COMMITTEE_YAML = path.resolve(__dirname, '../../_data/committee.yaml');
const OUTPUT_DIR = path.resolve(__dirname, '../public/data');
const RESOLUTIONS_FILE = path.join(OUTPUT_DIR, 'resolutions.json');
const COMMITTEE_FILE = path.join(OUTPUT_DIR, 'committee.json');

function main() {
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  const files = fs.readdirSync(PLENARY_DIR).filter(f => f.endsWith('.yaml') || f.endsWith('.yml'));
  const allResolutions = [];

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

    if (!parsed || !parsed.decisions) continue;

    const source_file = file.replace(/\.ya?ml$/, '');
    const metadata = parsed.metadata || {};

    for (const decision of parsed.decisions) {
      allResolutions.push(buildResolutionRecord(decision, source_file, metadata));
    }
  }

  allResolutions.sort(sortResolutions);

  fs.writeFileSync(RESOLUTIONS_FILE, JSON.stringify(allResolutions), 'utf8');
  console.log(`Successfully built ${allResolutions.length} resolutions to ${RESOLUTIONS_FILE}`);

  // Build committee.json from the MeetingSeries fixture.
  if (!fs.existsSync(COMMITTEE_YAML)) {
    console.error(`Missing ${COMMITTEE_YAML}; cannot build committee.json`);
    process.exit(1);
  }
  const series = yaml.load(fs.readFileSync(COMMITTEE_YAML, 'utf8'));
  const committee = buildCommitteeRecord(series);
  fs.writeFileSync(COMMITTEE_FILE, JSON.stringify(committee), 'utf8');
  console.log(`Successfully built committee to ${COMMITTEE_FILE}`);
}

main();
