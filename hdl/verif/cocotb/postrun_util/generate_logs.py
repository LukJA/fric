import json
import os

with open("../logs/pytest.log") as logfile:
    for line in logfile:
        data = json.loads(line)
        if 'when' not in data or data['when'] != 'call':
            continue

        module_name = data['nodeid'].removeprefix('tests/')
        py_idx = module_name.index('.py')
        slash_idx = module_name.rindex('/')

        filename = f"../logs/generated/{module_name[:slash_idx]}/{module_name[py_idx+5:]}.log"

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            for s in data['sections']:
                f.write(f"--- {s[0]} ---\n")
                f.write(s[1])
                f.write(f"\n\n")
    