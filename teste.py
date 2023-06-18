

def get_code_reference(line:str):
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




r  = get_code_reference('<!-- codeof:exemples/sql.c -->')

print(r)