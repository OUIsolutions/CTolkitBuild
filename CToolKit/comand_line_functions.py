from typing import List

from CToolKit.Errors.CopilationError import CopilationError
from CToolKit.Errors.CopilationWarning import CopilationWarning

from CToolKit.Errors.ValgrindError import  ValgrindError
from CToolKit.Errors.ValgrindLeak import  ValgrindLeak
from CToolKit.ComandLineExecution import ComandLineExecution

from platform import system as current_os

from os import listdir,remove

def copile_project_by_command(command: str, raise_errors: bool = True, raise_warnings: bool = True):
    """Compile an project based on the comands passed"""
    result = ComandLineExecution(command)

    if raise_errors and result.status_code != 0:
        raise CopilationError(result.output, result.status_code)


    if raise_warnings and 'warning:' in result.output:
        raise CopilationWarning(result.output)


def copile_project(compiler: str, file: str, output: str = None, flags: List[str] = None, raise_errors: bool = True,
                    raise_warnings: bool = True)->str:

    if flags is None:
        flags = []

    if output is None:
        if current_os() == 'Windows':
            output = file.replace('.c', 'exe').replace('.cpp', '.exe')
        else:
            output = file.replace('.c', '.out').replace('.cpp', '.out')

    command = f'{compiler} {file} -o {output} ' + ' '.join(flags)
    copile_project_by_command(command, raise_errors, raise_warnings)
    return output





def test_binary_with_valgrind(binary_file:str,flags: List[str]= None):

    if flags is None:
        flags = []

    command = f'valgrind  {binary_file} ' + ' '.join(flags)
    result = ComandLineExecution(command)

    if 'ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)' not in result.output:
        raise ValgrindError(result.output)

    if 'All heap blocks were freed -- no leaks are possible' not in result.output:
        raise ValgrindLeak(result.output)


def execute_test_for_file(copiler:str, file: str):
    result = copile_project(
        copiler,
        file,
        raise_errors=True,
        raise_warnings=False
    )
    try:
        test_binary_with_valgrind(result)
        remove(result)
    except Exception as e:
        remove(result)
        raise e


def execute_test_for_folder(copiler:str, folder: str,print_values:bool = True):
    files = listdir(folder)
    for file in files:
        if not file.endswith('.c') or file.endswith('.cpp'):
            continue

        try:
            execute_test_for_file(copiler,f'{folder}/{file}')
            if print_values:
                print('\033[92m'+f'passed: {file}' + '\33[37m')

        except Exception as e:
            if print_values:
                print('\033[91m' + f'fail with file: {file}' + '\33[37m')
                print('\033[0m')
            raise e
