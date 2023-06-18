
def get_code_reference(line:str):
    test = ''
    TARGET  = '<!--codeof:'
    found = True
    for letter in line:
        if letter == ' ':
            continue

        if not TARGET.startswith(test):
            return None

        test+=letter



def parse_readme(text :str )->list:
    constructed = []
    for line in text:
        pass