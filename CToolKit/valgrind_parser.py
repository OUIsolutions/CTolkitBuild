
def parse_in_blocks(text:str)->dict:
    result = {}
    result ['bytes'] = int(text.split(' ')[1])
    in_element_text = text.split('in')[1]
    
    result['blocks'] = int(in_element_text.split(' ')[1])
    return result


def parse_block_line_based_on_key(text:str,key:str)->dict:
    target = text.split(key)[1]
    text = target.split('\n')[0]
    return parse_in_blocks(text)



def parse_valgrind_result(text:str)->dict:
    
    result  = {
        'in use at exit':parse_block_line_based_on_key(text,'in use at exit')
    }
    return result

    