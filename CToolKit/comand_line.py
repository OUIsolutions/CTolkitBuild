from typing import List

from CToolKit.Errors.CopilerError import CompilationError
from CToolKit.Errors.ExecutionError import ExecutionError

import subprocess
from platform import system as current_os



def copile_project_by_command(command: str, raise_errors: bool = True, raise_warnings: bool = True):
    """Compile an project based on the comands passed"""
    status_code, output = subprocess.getstatusoutput(command)

    if raise_errors and status_code != 0:
        raise CompilationError(output, status_code,'Copilation Error')

    if raise_warnings and 'warning:' in output:
        raise CompilationError(output, status_code,'Warning')


def copile_project(compiler: str, file: str, output: str = None, flags: List[str] = None, raise_errors: bool = True,
                    raise_warnings: bool = True):

    if flags is None:
        flags = []

    if output is None:
        if current_os() == 'Windows':
            output = file.replace('.c', 'exe').replace('.cpp', '.exe')
        else:
            output = file.replace('.c', '.out').replace('.cpp', '.out')

    command = f'{compiler} {file} -o {output} ' + ' '.join(flags)
    copile_project_by_command(command, raise_errors, raise_warnings)



def test_binary_with_valgrind(binary_file:str,flags: List[str]= None):
    if flags is None:
        flags = []
    command = f'valgrind  {binary_file} ' + ' '.join(flags)

    status_code, output = subprocess.getstatusoutput(command)

    if status_code != 0:
        raise ExecutionError(output,status_code)

    


    print('status' ,status_code)
    print('comand',output)
