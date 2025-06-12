import yaml
import time

import epistolae_commons
import wikidata_utils

women_path = epistolae_commons.epistolae_hugo_path.joinpath('content/woman')
people_path = epistolae_commons.epistolae_hugo_path.joinpath('content/people')
wikidata_result_path = epistolae_commons.epistolae_hugo_path.joinpath('tools/data/output/wikidata/content')

sprql = """
SELECT distinct ?item ?itemLabel ?itemDescription ?viaf ?isni WHERE{  
  ?item ?label "%s"@en .  
  ?item wdt:P31 wd:Q5 . # instance of human
  ?article schema:about ?item .
  ?article schema:inLanguage "en" .
  OPTIONAL { ?item wdt:P214 ?viaf . }
  OPTIONAL { ?item wdt:P213 ?isni . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }    
}
"""
def find_wikidata_unique_result(title: str):
    response = wikidata_utils.wd_query(sprql % title)
    if (response.status_code == 200):
        responseObj = response.json()
        if ('results' in responseObj):
            results = responseObj['results']
            if ('bindings' in results):
                bindings = results['bindings']
                # avoid multiple, ambiguous results
                if len(bindings) == 1: 
                    if 'itemDescription' in bindings[0] and not 'disambiguation' in bindings[0]['itemDescription']['value']:
                      return response
                comma_index = title.find(',')
                if comma_index > -1:
                    return find_wikidata_unique_result(title[0:comma_index])
    return None

front_matters = {}

for path in (women_path, people_path):
    for person_path in path.iterdir():
        with person_path.open('r') as person_file:
            front_matter = yaml.load(''.join(epistolae_commons.read_hugo_front_matter(person_file)), Loader=yaml.Loader)
            wikidata_response = find_wikidata_unique_result(front_matter['title'])
            if wikidata_response:
                result_path = wikidata_result_path.joinpath(path.name).joinpath(person_path.name + '.wikidata.json')
                with result_path.open('w') as result_file:
                    result_file.write(wikidata_response.text)
        time.sleep(1) # to avoid HTTP 429 Too Many Requests from wikidata
