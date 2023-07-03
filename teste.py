

from types import List
def trim_lines(text:str)->List[str]:
    lines = text.split('\n')
    return list(map(lambda x:x.trim(),lines))

def sanitize_value(filename:str, content:str)->dict or str or List[str]:
    
    if filename.endswith('.json'):
        pass 
    
    pass 
