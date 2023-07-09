
from os import listdir
from os.path import  isdir
from typing import List
from ..comand_line_functions import execute_test_for_file
from ..Errors.NotExpectedResult import NotExpectedResult
from .output_formatation import  sanitize_value
from ..ComandLineExecution import ComandLineExecution
from .Creation import FolderTestPressetCreation
class FolderTestPressetExecution(FolderTestPressetCreation):


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




    def _execute_loop_test(self,folder:str):
        self._print_if_seetted_to_print_folder(folder)

        elements:List[str] = listdir(folder)
        for e in elements:
            path = f'{folder}/{e}'

            if isdir(path):

                if e.startswith('R_') or e.startswith('WR_'):
                    try:
                        self._execute_test_presset(path)
                        self._print_if_setted_to_print_test(e, True)
                    except Exception as ex:
                        self._print_if_setted_to_print_test(e, False)
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
                    self._print_if_setted_to_print_test(e, True)


                except Exception as ex:
                    self._print_if_setted_to_print_test(e, False)
                    raise ex




    def start_test(self):
        self._create_copy_side_effect_folder()
        self._execute_loop_test(self._folder)


