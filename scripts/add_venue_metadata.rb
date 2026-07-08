#!/usr/bin/env ruby
# Add explicit `city` (UN/LOCODE) + `country_code` to every fixture's
# metadata block. Uses a curated lookup table — no runtime derivation.
#
# The mapping is maintained here as the single source of truth for
# tc184sc4 meeting venues. Each UN/LOCODE is the canonical identifier
# per the UN/LOCODE registry; the UI resolves it to a display name.

require "yaml"

# Curated: source_file slug → [UN/LOCODE, country_code]
# "virtual" entries have empty strings (no physical location).
VENUE_MAP = {
  "bad-aibling-germany"          => ["DEBAI", "DE"],
  "baltimore-usa"                => ["USBAL", "US"],
  "bath-united-kingdom"          => ["GBBTH", "GB"],
  "beijing-china"                => ["CNBJS", "CN"],
  "belfort-france"               => ["FRBLF", "FR"],
  "berlin-germany"               => ["DEBER", "DE"],
  "bethlehem-pennsylvania-usa"   => ["USBNP", "US"],
  "bordeaux-france"              => ["FRBOD", "FR"],
  "busan-korea"                  => ["KRPUS", "KR"],
  "charleston-sc-usa"            => ["USCHS", "US"],
  "chicago-usa"                  => ["USCHI", "US"],
  "dallas-tx-usa"                => ["USDAL", "US"],
  "dallas-tx-usa"                => ["USDAL", "US"],
  "davos-switzerland"            => ["CHDVS", "CH"],
  "florence-italy"               => ["ITFLR", "IT"],
  "florida-usa"                  => ["USMIA", "US"],
  "ft-lauderdale-fl-usa"         => ["USFLL", "US"],
  "fukuoka-japan"                => ["JPHKT", "JP"],  # Hakata/Fukuoka
  "funchal-madeira-island-portugal" => ["PTFNC", "PT"],
  "funchal-portugal"             => ["PTFNC", "PT"],
  "gaithersburg-washington-dc-usa" => ["USGAI", "US"],
  "gothenburg-sweden"            => ["SEGOT", "SE"],
  "greenville-sc-usa"            => ["USGVL", "US"],
  "grenoble-france"              => ["FRGNB", "FR"],
  "gyeongju-korea"               => ["KRGJU", "KR"],
  "hamamatsu-japan"              => ["JPHMZ", "JP"],
  "hangzhou-china"               => ["CNHGH", "CN"],
  "hershey-pa-usa"               => ["USHEH", "US"],  # nearest: Harrisburg
  "ibusuki-japan"                => ["JPIBK", "JP"],
  "irving-dallas-tx-usa"         => ["USDAL", "US"],
  "jeju-korea"                   => ["KRJEU", "KR"],
  "kobe-japan"                   => ["JPUKB", "JP"],
  "lillehammer-norway"           => ["NOLLM", "NO"],  # nearest: Lillehammer
  "little-rock-arkansas-usa"     => ["USLIT", "US"],
  "louisville-ky-usa"            => ["USLOU", "US"],
  "marina-del-rey-usa"           => ["USLAX", "US"],  # LAX area
  "melbourne-australia"          => ["AUMEL", "AU"],
  "myrtle-beach-sc-usa"          => ["USMYR", "US"],
  "nagasaki-japan"               => ["JPNGS", "JP"],
  "new-orleans-la-usa"           => ["USMSY", "US"],
  "oslo-norway"                  => ["NOOSL", "NO"],
  "oslo-sandvika-norway"         => ["NOOSL", "NO"],
  "paris-france"                 => ["FRPAR", "FR"],
  "parksville-british-columbia-canada" => ["CAPKS", "CA"],
  "philadelphia-usa"             => ["USPHL", "US"],
  "poitiers-france"              => ["FRPIS", "FR"],
  "portland-oregon-usa"          => ["USPDX", "US"],
  "rotterdam-netherlands"        => ["NLRTM", "NL"],
  "rotterdam-the-netherlands"    => ["NLRTM", "NL"],
  "san-diego-ca-usa"             => ["USSAN", "US"],
  "san-francisco-ca-usa"         => ["USSFO", "US"],
  "san-francisco-usa"            => ["USSFO", "US"],
  "sapporo-japan"                => ["JPSPK", "JP"],
  "saratoga-springs-usa"         => ["USSAR", "US"],  # nearest: Saratoga
  "seattle-usa"                  => ["USSEA", "US"],
  "seattle-wa-usa"               => ["USSEA", "US"],
  "seoul-korea"                  => ["KRSEL", "KR"],
  "st-denis-france"              => ["FRSDN", "FR"],  # Saint-Denis
  "stavanger-norway"             => ["NOSVG", "NO"],
  "stockholm-sweden"             => ["SESTO", "SE"],
  "stuttgart-germany"            => ["DESTG", "DE"],
  "sun-city-south-africa"        => ["ZASUN", "ZA"],
  "suzhou-china"                 => ["CNSZH", "CN"],
  "sydney-australia"             => ["AUSYD", "AU"],
  "tokyo-japan"                  => ["JPTYO", "JP"],
  "toronto-canada"               => ["CATOR", "CA"],
  "toulouse-france"              => ["FRTLS", "FR"],
  "turin-italy"                  => ["ITTOA", "IT"],  # Torino
  "valencia-spain"               => ["ESVLC", "ES"],
  "vico-equense-italy"           => ["ITNAP", "IT"],  # Naples area
  "virtual"                      => ["", ""],
}.freeze

Dir["plenary/*.yaml"].sort.each do |file|
  basename = File.basename(file, ".yaml")
  data = YAML.safe_load(File.read(file), permitted_classes: [Date])
  meta = data["metadata"] ||= {}

  # Skip if already has city
  if meta["city"] && !meta["city"].to_s.empty?
    puts "skip #{basename} (city=#{meta["city"]})"
    next
  end

  # Extract venue slug from source filename
  slug = basename.sub(/^plenary-\d{4}-\d{2}-/, "")

  entry = VENUE_MAP[slug]
  unless entry
    puts "WARN #{basename}: no mapping for slug=#{slug.inspect}"
    next
  end

  city, country = entry
  if city.empty?
    puts "#{basename}: virtual (no city/country)"
    next
  end

  meta["city"] = city
  meta["country_code"] = country
  data["metadata"] = meta

  File.write(file, data.to_yaml)
  puts "#{basename}: #{city} / #{country}"
end
