import yaml

with open('/Users/mulgogi/src/isotc184sc4/resolutions/plenary/plenary-2002-03-myrtle-beach-sc-usa.yaml') as f:
    data = yaml.safe_load(f)

# we will manually construct the new yaml string because we want block scalars for strings.
