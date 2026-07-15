// UN/LOCODE → { city, country } display-name resolver.
//
// Curated lookup for tc184sc4 meeting venues. Keyed by the UN/LOCODE
// stored in DecisionMetadata.city. The YAML fixtures carry the
// canonical UN/LOCODE; this table resolves it to a human-readable
// venue for the browser.

const UNLOCODE_NAMES = {
  AUMEL: { city: 'Melbourne', country: 'Australia' },
  AUSYD: { city: 'Sydney', country: 'Australia' },
  CAPKS: { city: 'Parksville', country: 'Canada' },
  CATOR: { city: 'Toronto', country: 'Canada' },
  CHDVS: { city: 'Davos', country: 'Switzerland' },
  CNBJS: { city: 'Beijing', country: 'China' },
  CNHGH: { city: 'Hangzhou', country: 'China' },
  CNSZH: { city: 'Suzhou', country: 'China' },
  DEBAI: { city: 'Bad Aibling', country: 'Germany' },
  DEBER: { city: 'Berlin', country: 'Germany' },
  DESTG: { city: 'Stuttgart', country: 'Germany' },
  ESVLC: { city: 'Valencia', country: 'Spain' },
  FRBLF: { city: 'Belfort', country: 'France' },
  FRBOD: { city: 'Bordeaux', country: 'France' },
  FRGNB: { city: 'Grenoble', country: 'France' },
  FRPAR: { city: 'Paris', country: 'France' },
  FRPIS: { city: 'Poitiers', country: 'France' },
  FRSDN: { city: 'Saint-Denis', country: 'France' },
  FRTLS: { city: 'Toulouse', country: 'France' },
  GBBTH: { city: 'Bath', country: 'United Kingdom' },
  ITFLR: { city: 'Florence', country: 'Italy' },
  ITNAP: { city: 'Vico Equense (Naples)', country: 'Italy' },
  ITTOA: { city: 'Turin', country: 'Italy' },
  JPHKT: { city: 'Fukuoka', country: 'Japan' },
  JPHMZ: { city: 'Hamamatsu', country: 'Japan' },
  JPIBK: { city: 'Ibusuki', country: 'Japan' },
  JPNGS: { city: 'Nagasaki', country: 'Japan' },
  JPSPK: { city: 'Sapporo', country: 'Japan' },
  JPTYO: { city: 'Tokyo', country: 'Japan' },
  JPUKB: { city: 'Kobe', country: 'Japan' },
  KRGJU: { city: 'Gyeongju', country: 'Korea' },
  KRJEU: { city: 'Jeju', country: 'Korea' },
  KRPUS: { city: 'Busan', country: 'Korea' },
  KRSEL: { city: 'Seoul', country: 'Korea' },
  NOLLM: { city: 'Lillehammer', country: 'Norway' },
  NOOSL: { city: 'Oslo', country: 'Norway' },
  NOSVG: { city: 'Stavanger', country: 'Norway' },
  NLRTM: { city: 'Rotterdam', country: 'Netherlands' },
  PTFNC: { city: 'Funchal', country: 'Portugal' },
  SEGOT: { city: 'Gothenburg', country: 'Sweden' },
  SESTO: { city: 'Stockholm', country: 'Sweden' },
  USBAL: { city: 'Baltimore', country: 'USA' },
  USBNP: { city: 'Bethlehem, PA', country: 'USA' },
  USCHI: { city: 'Chicago', country: 'USA' },
  USCHS: { city: 'Charleston, SC', country: 'USA' },
  USDAL: { city: 'Dallas, TX', country: 'USA' },
  USFLL: { city: 'Fort Lauderdale, FL', country: 'USA' },
  USGAI: { city: 'Gaithersburg, MD', country: 'USA' },
  USGVL: { city: 'Greenville, SC', country: 'USA' },
  USHEH: { city: 'Hershey, PA', country: 'USA' },
  USLAX: { city: 'Marina del Rey, CA', country: 'USA' },
  USLIT: { city: 'Little Rock, AR', country: 'USA' },
  USLOU: { city: 'Louisville, KY', country: 'USA' },
  USMIA: { city: 'Florida', country: 'USA' },
  USMSY: { city: 'New Orleans, LA', country: 'USA' },
  USMYR: { city: 'Myrtle Beach, SC', country: 'USA' },
  USPDX: { city: 'Portland, OR', country: 'USA' },
  USPHL: { city: 'Philadelphia', country: 'USA' },
  USSAN: { city: 'San Diego, CA', country: 'USA' },
  USSAR: { city: 'Saratoga Springs, NY', country: 'USA' },
  USSEA: { city: 'Seattle', country: 'USA' },
  USSFO: { city: 'San Francisco, CA', country: 'USA' },
  ZASUN: { city: 'Sun City', country: 'South Africa' },
}

// Resolve a UN/LOCODE to a display venue string: "City, Country".
export function venueDisplay(unlocode) {
  if (!unlocode) return 'Virtual'
  const entry = UNLOCODE_NAMES[unlocode]
  if (!entry) return unlocode
  return `${entry.city}, ${entry.country}`
}

// Resolve a UN/LOCODE to the flag emoji for the country.
const COUNTRY_FLAGS = {
  AU: '🇦🇺', CA: '🇨🇦', CH: '🇨🇭', CN: '🇨🇳', DE: '🇩🇪',
  ES: '🇪🇸', FR: '🇫🇷', GB: '🇬🇧', IT: '🇮🇹', JP: '🇯🇵',
  KR: '🇰🇷', NL: '🇳🇱', NO: '🇳🇴', PT: '🇵🇹', SE: '🇸🇪',
  US: '🇺🇸', ZA: '🇿🇦',
}

export function venueFlag(unlocode) {
  if (!unlocode) return '🌐'
  const country = unlocode.substring(0, 2)
  return COUNTRY_FLAGS[country] || ''
}

export { UNLOCODE_NAMES }
