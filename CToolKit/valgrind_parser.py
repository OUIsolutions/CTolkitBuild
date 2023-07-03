

def convert_num(num:str)->str:
    return int(num.replace(',',''))


def parse_in_blocks(text:str)->dict:
    result = {}
    result ['bytes'] = convert_num(text.split(' ')[1])
    in_element_text = text.split('in')[1]
    
    result['blocks'] = convert_num(in_element_text.split(' ')[1])
    return result


def parse_block_line_based_on_key(text:str,key:str)->dict:
    if key not in text:
        return {'bytes':0,'blocks':0}
    
    target = text.split(key)[1]
    text = target.split('\n')[0]
    return parse_in_blocks(text)


def extract_output(text:str):
    target = text.split('Command:')[1]
    return target.split('==')[2]

    
def parse_heap_usage(text:str)->dict:
    target = text.split('total heap usage')[1]
    positions = target.split(' ')
    return {
        'allocs':convert_num(positions[1]),
        'frees':convert_num(positions[3]),
        'bytes allocated': convert_num(positions[5])
    }
    
    
def parse_valgrind_result(text:str)->dict:
    
    result  = {
        'output': extract_output(text),
        'in use at exit':parse_block_line_based_on_key(text,'in use at exit'),
        'definitely lost':parse_block_line_based_on_key(text,'definitely lost'),
        'indirectly lost':parse_block_line_based_on_key(text,'indirectly lost'),
        'possibly lost':parse_block_line_based_on_key(text,'possibly lost'),
        'still reachable':parse_block_line_based_on_key(text,'still reachable'),
        'suppressed':parse_block_line_based_on_key(text,'suppressed'),
        'heap usage': parse_heap_usage(text)
    }
    
    return result

    