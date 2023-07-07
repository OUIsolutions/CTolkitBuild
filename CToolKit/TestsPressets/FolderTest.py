
from os import listdir,remove
from os.path import isdir

from ..ComandLineExecution import ComandLineExecution
from ..output_formatation import sanitize_value
from ..comand_line_functions import execute_test_for_file
from ..Errors.NotExpectedResult import NotExpectedResult

class FolderTest:

    def __init__(
            self,
            target_folder:str,
            side_effect_folder:str = None,
            compiler='gcc',
            print_values=True,
            use_valgrind=True,
            raise_warnings=True,
            code_flag='exe.c',
            expected_flag='expected'
    ):

        self._target_folder = target_folder
        self._side_effect_folder = side_effect_folder
        self._compiler = compiler
        self._print_values = True
        self._use_valgrind = use_valgrind
        self._raise_warnings = raise_warnings
        self._code_flags = code_flag
        self._expected_flag = expected_flag



    def _get_expected_file(self,foldername: str) -> str or None:
        for file in listdir(foldername):
            if file.startswith(self._expected_flag):
                return f'{foldername}/{file}'



    def _test_folder_presset(self,folderpath:str,foldername:str) -> dict or ComandLineExecution:


            files = listdir(folderpath)

            target = f'{folderpath}/exec.c'


            if 'exec.c' not in files:
                raise FileNotFoundError(folderpath)


            expected_file_name = self._get_expected_file(folderpath)

            if expected_file_name is None:
                raise FileNotFoundError(
                    self._expected_flag
                )
            with open(expected_file_name, 'r') as arq:
                expected = sanitize_value(expected_file_name, arq.read())


            if self._use_valgrind:
                r: dict = execute_test_for_file(target, self._compiler, True, self._raise_warnings)
                saninitzed_result = sanitize_value(expected_file_name, r['output'])
            else:
                r: ComandLineExecution = execute_test_for_file(target, self._compiler, False, self._raise_warnings)
                saninitzed_result = sanitize_value(expected_file_name, r.output)

            if expected != saninitzed_result:
                raise NotExpectedResult(saninitzed_result, expected)

            return r



    def execute_test_for_folder(self,folder: str=None):
        """execute tests for all .c or cpp files in the given folder
        Args:
            compiler (str): the compiler, ex: gcc , or clang
            folder (str): the folder to copile
            print_values (bool, optional): if is to print errors and sucess
            raise_warnings(bool): if its to raise warnings generated
        Raises:
            e: if happen some error
        """
        if folder is None:
            folder = self._target_folder

        print('\033[92m' + f'folder: {folder}')

        elements = listdir(folder)
        for element in elements:
            current_path = f'{folder}/{element}'

            if isdir(current_path):
                current_folder = current_path
                if element.startswith('R_') or element.startswith('WR_'):
                    try:
                        self._test_folder_presset(current_folder)
                        print('\033[92m' + f'\tpassed: {element}' + '\33[37m')
                    except Exception as e:
                        print('\033[91m' + f'fail with folder: {element}' + '\33[37m')
                        raise e

                else:
                    self.execute_test_for_folder(current_folder)
                continue

            if not element.endswith('.c') or element.endswith('.cpp'):
                continue

            try:
                execute_test_for_file(current_path, self._compiler, self._use_valgrind, self._raise_warnings)
                if self._print_values:
                    print('\033[92m' + f'\tpassed: {element}' + '\33[37m')
            except Exception as e:
                if self._print_values:
                    print('\033[91m' + f'fail with file: {element}' + '\33[37m')
                    print('\033[0m')
                raise e

    def _create_code_presset(self,folder_path:str):
        files = listdir(folder_path)

        target = f'{folder_path}/exec.c'

        if 'exec.c' not in files:
            raise FileNotFoundError(folder)

        expected_file_name = get_expected_file(folder)

        if expected_file_name is not None:
            return


        if use_valgrind:
            r: dict = execute_test_for_file( target,compiler, True, raise_warnings)
            output = r['output']
        else:
            r: ComandLineExecution = execute_test_for_file( target,compiler, False, raise_warnings)
            output = r.output

        with open(f'{folder}/expected.txt','w') as arq:
            arq.write(output)


    def generate_output_of_execution(self,folder:str=None):
        if folder is None:
            folder = self._target_folder

        files = listdir(folder)
        for file in files:
            file_path = f'{folder}/{file}'
            if isdir(file_path):
                if file.startswith('R_') or file.startswith('WR_'):
                    create_code_presset(compiler,use_valgrind,file_path,raise_warnings)
                    continue
                self.generate_output_of_execution(file_path)

