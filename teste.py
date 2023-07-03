from CToolKit.valgrind_parser import parse_valgrind_result



r = parse_valgrind_result(
    open('aaanot_trim.json','r').read()
)
print(r)