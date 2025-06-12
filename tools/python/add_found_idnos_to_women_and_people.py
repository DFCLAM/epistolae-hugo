import json

import epistolae_commons

women_path = epistolae_commons.epistolae_hugo_path.joinpath('content/woman')
people_path = epistolae_commons.epistolae_hugo_path.joinpath('content/people')
wikidata_result_path = epistolae_commons.epistolae_hugo_path.joinpath('tools/data/output/wikidata/content')

for path in (women_path, people_path):
    for person_path in path.iterdir():
        result_path = wikidata_result_path.joinpath(path.name).joinpath(person_path.name + '.wikidata.json')
        if result_path.exists():
            with result_path.open('r') as result_file:
                result_obj = json.load(result_file)
            [wd, viaf, isni] = [None, None, None]
            if 'results' in result_obj:
                results = result_obj['results']
                if 'bindings' in results:
                    bindings = results['bindings']
                    if len(bindings) == 1:
                        [binding] = bindings
                        wd = str(binding['item']['value']).rsplit('/',1)[1]
                        if 'viaf' in binding:
                            viaf = binding['viaf']['value']
                        if 'isni' in binding:
                            isni = binding['isni']['value']
            if wd:
                with person_path.open('r') as person_file:
                    contents = person_file.readlines()
                insertion_point = -1
                for index, content in enumerate(contents):
                    if content.startswith('---'):
                        for index, content in enumerate(contents):
                            if content.startswith('woman_id:') or content.startswith('people_id:'):
                                insertion_point = index + 1
                                break
                        break
                if insertion_point > -1:
                    contents.insert(insertion_point, 'idno:\n')
                    insertion_point += 1
                    contents.insert(insertion_point, '  - type: "Wikidata"\n')
                    insertion_point += 1
                    contents.insert(insertion_point, '    value: "%s"\n' % wd)
                    if viaf:
                        insertion_point += 1
                        contents.insert(insertion_point, '  - type: "viaf"\n')
                        insertion_point += 1
                        contents.insert(insertion_point, '    value: "%s"\n' % viaf)
                    if isni:
                        insertion_point += 1
                        contents.insert(insertion_point, '  - type: "isni"\n')
                        insertion_point += 1
                        contents.insert(insertion_point, '    value: "%s"\n' % isni)
                    with person_path.open('w') as person_file:
                        person_file.writelines(contents)

