
def get_code_reference(line:str)->str or None:
    test = ''
    TARGET  = '<!--codeof:'
    inclusion = ''
    found_start = False
    for letter in line:


        if found_start == False:

            if letter == ' ':
                continue

            if not TARGET.startswith(test):
                return None

            test+=letter

            if test == TARGET:
                found_start = True
                continue

        if found_start:

            if letter == ' ' or letter == '-':
                return inclusion

            inclusion+=letter

    return None


def parse_readme_lexer(text:str)->list:
    constructed = []
    block = ''

    inside_block = False
    first_line_inside_block = False
    lines = text.split('\n')
    for line in lines:
        if inside_block:
            if first_line_inside_block:
                if line.startswith('~~~') or line .startswith('´´´'):
                    first_line_inside_block = False
                    continue
                else:
                    inside_block = False
                    first_line_inside_block = False
                    continue
            if line.startswith('~~~') or line.startswith('´´´'):
                inside_block = False
                first_line_inside_block = False
                continue
            continue

        ref = get_code_reference(line)

        if ref:
            constructed.append({'type':'block','text':block})

            extension = None
            divided_ref = ref.split('.')
            if len(divided_ref) > 1:
                extension = divided_ref[-1]

            constructed.append({'type':'ref','ref':ref,'extension':extension})
            block =''
            inside_block = True
            first_line_inside_block = True

        if ref is None:
            block+=line

    constructed.append({'type': 'block', 'text': block})
    return constructed