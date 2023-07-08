
from os import listdir
from os.path import  isdir,isfile
from typing import List
from .comand_line_functions import execute_test_for_file
from .Errors.NotExpectedResult import NotExpectedResult
from .output_formatation import  sanitize_value
from .ComandLineExecution import ComandLineExecution


class FolderTestPresset:

    def __init__(
            self,
            folder:str,
            side_effect_folder:str =None,
            compiler='gcc',
            print_values=True,
            use_valgrind=True,
            raise_warnings=True
    ):
        self._folder = folder
        self._side_effect_folder = side_effect_folder
        self._compiler =compiler
        self._print_values = print_values
        self._use_valgrind = use_valgrind
        self._raise_warnings=raise_warnings




    def _get_expected_file(self,folder:str):
        elements = listdir(folder)
        for e in elements:
            if isdir(e):
                continue

            if e.startswith('expected'):
                return f'{folder}/{e}'


    def _get_file_to_execute(self,folder:str):
        c_file = f'{folder}/exec.c'
        cpp_file = f'{folder}/exec.cpp'

        if isfile(c_file):
            return c_file

        if isfile(cpp_file):
            return cpp_file

        raise FileNotFoundError(f'could not locate an exec.c or exec.cpp in {folder}')

    def _execute_test_presset(self,folder:str):
        pass

        execution_file = self._get_file_to_execute(folder)
        expected_file = self._get_expected_file(folder)

        if expected_file is None:
            raise FileNotFoundError(f'could not locate an expected.* in {folder}')

        with open(expected_file,'r') as arq:
            expected_content = arq.read()

        sanitized_expected :dict or List[str] = sanitize_value(expected_file,expected_content)

        generated_result:dict or ComandLineExecution = execute_test_for_file(
            file=execution_file,
            compiler=self._compiler,
            use_valgrind=self._use_valgrind,
            raise_warnings=self._raise_warnings
        )
        if isinstance(generated_result,ComandLineExecution):
            output = generated_result.output
        else:
            output = generated_result['output']


        sanitized_result = sanitize_value(expected_file,output)


        if sanitized_expected != sanitized_result:
            raise NotExpectedResult(sanitized_expected,sanitized_result)



    def _print_if_setted_to_print(self,element:str , passed:bool):
        if not self._print_values:
            return
        if passed:
            print('\033[92m' + f'\tpassed : {element}')
        else:
            print('\033[91m' + f'\tfail : {element}')

    def _execute_loop_test(self,folder:str):
        print(f'testing: {folder}')

        elements:List[str] = listdir(folder)
        for e in elements:
            path = f'{folder}/{e}'

            if isdir(path):

                if e.startswith('R_') or e.startswith('WR_'):
                    try:
                        self._execute_test_presset(path)
                        self._print_if_setted_to_print(e,True)
                    except Exception as ex:
                        self._print_if_setted_to_print(e,False)
                        raise ex
                else:
                    self._execute_loop_test(path)

            else:
                try:
                    if e.endswith('c') or e.endswith('cpp'):
                        execute_test_for_file(
                            file=path,
                            compiler=self._compiler,
                            use_valgrind=self._use_valgrind,
                            raise_warnings=self._use_valgrind
                        )
                    self._print_if_setted_to_print(e, True)


                except Exception as ex:
                    self._print_if_setted_to_print(e, False)
                    raise ex

    def start_test(self):
        self._execute_loop_test(self._folder)



