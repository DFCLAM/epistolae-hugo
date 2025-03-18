import pathlib
import yaml
import re

import epistolae_commons

letters_path = epistolae_commons.epistolae_hugo_path.joinpath('content/letter')
date_formats_path = pathlib.Path.home().joinpath('ltr_date_formats.txt')

models = {}

for letter_path in letters_path.iterdir():
    with letter_path.open(mode='r') as letter:
        model = yaml.load(''.join(epistolae_commons.read_hugo_front_matter(letter)), Loader=yaml.Loader)
        for key in model:
            models.setdefault(key, []).append(model[key])

print(models.keys())

number_to_x = re.compile(r"[0-9]")
# print(sorted({number_to_x.sub('x', date) for date in models['ltr_date']}))
with date_formats_path.open(mode='w') as date_formats:
    date_formats.writelines(sorted({number_to_x.sub('x', date).strip() + '\n' for date in models['ltr_date']}))
