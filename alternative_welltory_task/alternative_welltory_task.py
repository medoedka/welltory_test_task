import pandas as pd
import jsonschema
import json
import os

path_to_jsons = 'PATH_TO_DIR_WITH_JSONS'
path_to_scheme = 'PATH_TO_DIR_WITH_SCHEME'
list_of_scheme = []
for schema in os.listdir(path_to_scheme):
    with open(path_to_scheme + r'\\' + schema) as f:
        schema = json.loads(f.read())
        list_of_scheme.append(schema)

errors = {}

json_dirs = os.listdir(path_to_jsons)
for json_file in json_dirs:
    not_valid = False
    with open(path_to_jsons + r'\\' + json_file, 'r') as f:
        instance = json.loads(f.read())
        for schema in list_of_scheme:
            try:
                jsonschema.validate(instance=instance, schema=schema)
            except jsonschema.exceptions.ValidationError as err:
                not_valid = True
                if json_file not in errors:
                    errors[json_file] = [err.message]
                else:
                    errors[json_file].append(err.message)
            if not_valid == False:
                errors[json_file].append(False)
    if all(errors[json_file]):
        errors[json_file].append('Нет')
    else:
        errors[json_file].append('Да')
df = pd.DataFrame(data=errors).T
column_names = ['Ошибки в схеме %d' % i for i in range(1, 5)] + ['Валидный']
df.columns = column_names
print(df)