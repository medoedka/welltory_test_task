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
    with open(path_to_jsons + r'\\' + json_file, 'r') as f:
        instance = json.loads(f.read())
        for schema in list_of_scheme:
            try:
                jsonschema.validate(instance=instance, schema=schema)
            except jsonschema.exceptions.ValidationError as err:
                if json_file not in errors:
                    errors[json_file] = [err.message]
                else:
                    errors[json_file].append(err.message)
    if len(errors[json_file]) < len(list_of_scheme):
        errors[json_file] = 'Файл валидный'
for file in errors:
    print(file + ': ' + ', '.join(errors[file]).rstrip())
