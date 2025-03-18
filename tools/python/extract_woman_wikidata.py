import pathlib
import yaml
import re

import epistolae_commons
import wikidata_utils

women_path = epistolae_commons.epistolae_hugo_path.joinpath('content/woman')

sprql = """
SELECT distinct ?item ?itemLabel ?itemDescription WHERE{  
  ?item ?label "%s"@en.  
  ?article schema:about ?item .
  ?article schema:inLanguage "en" .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }    
}
"""
# print(wikidata_utils.wd_query(sprql))

front_matters = {}

for woman_path in women_path.iterdir():
    with woman_path.open(mode='r') as letter:
        front_matter = yaml.load(''.join(epistolae_commons.read_hugo_front_matter(letter)), Loader=yaml.Loader)
        front_matters[woman_path.name] = front_matter

# print(front_matters['1.html.md'])

for woman_file_name, front_matter in front_matters.items():
    print(wikidata_utils.wd_query(sprql % front_matter['title']))
