from typing import List
from os import listdir
from os.path import  isdir
from .Extras import FolderTestPresetExtras
from ..ComandLineExecution import ComandLineExecution
from ..comand_line_functions import execute_test_for_file
class FolderTestPressetCreation(FolderTestPresetExtras):

    def _execute_test_presset_creating_output(self, folder: str):
        execution_file = self._get_file_to_execute(folder)
        expected_file = self._get_expected_file(folder)

        if expected_file is not None:
            self._print_if_setted_to_print_creation(execution_file, False)
            return

        modification_time = self._get_side_effect_last_modification()

        try:
            generated_result: dict or ComandLineExecution = execute_test_for_file(
                file=execution_file,
                compiler=self._compiler,
                copilation_flags=self._compilation_flags,
                execution_flags=self._execution_flags,
                use_valgrind=self._use_valgrind,
                raise_warnings=self._raise_warnings
            )
        except Exception as e:
            new_modification = self._get_side_effect_last_modification()
            print(modification_time)
            print(new_modification)


        if isinstance(generated_result, ComandLineExecution):
            output = generated_result.output
        else:
            output = generated_result['output']

        with open(f'{folder}/expected.txt', 'w') as arq:
            self._print_if_setted_to_print_creation(execution_file, True)
            arq.write(output)

    def _execute_loop_creating_expected(self, folder: str):
        self._print_if_seetted_to_print_folder(folder)

        elements: List[str] = listdir(folder)
        for e in elements:
            path = f'{folder}/{e}'

            if not isdir(path):
                continue

            if e.startswith('R_') or e.startswith('WR_'):
                try:
                    self._execute_test_presset_creating_output(path)
                except Exception as ex:
                    self._print_if_setted_to_print_test(e, False)
                    raise ex
            else:
                self._execute_loop_creating_expected(path)

    def generate_ouptut(self):
        #deleting old zips
        self._create_side_effect_zip()
        self._execute_loop_creating_expected(self._folder)
