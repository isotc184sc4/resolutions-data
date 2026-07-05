require 'yaml'
y = YAML.load_file("plenary/plenary-2004-10-seattle-wa-usa.yaml")
puts "res 5 action 1: #{y['resolutions'][5]['actions'][1]['type']}"
puts "res 7 action 3: #{y['resolutions'][7]['actions'][3]['type']}"
