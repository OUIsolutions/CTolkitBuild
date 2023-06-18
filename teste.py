from CToolKit.readme_converter import  parse_readme_lexer
from CToolKit.readme_converter import  get_code_reference


with open('README.md','r') as arq:
    r = parse_readme_lexer(arq.read())
    print(r)