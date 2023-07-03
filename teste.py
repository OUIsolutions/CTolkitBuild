
import CToolKit as ct 
try:
    r = ct.execute_test_for_file('gcc','teste.c')
    print(r)
except ct.ValgrindLeak as e:
    print(e.valgrind_status)