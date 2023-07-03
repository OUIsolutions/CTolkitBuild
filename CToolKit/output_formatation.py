import json
from typing import List
def trim_lines(text:str)->List[str]:
    lines = text.split('\n')
    return list(map(lambda x: x.strip(),lines))

def sanitize_value(filename:str)->dict or str or List[str]:

    with open(filename,'r') as arq:
        content = arq.read()

    if filename.endswith('.json'):
        return json.loads(content)

    if 'not_trim' in filename:
        return content

    return trim_lines(content)

