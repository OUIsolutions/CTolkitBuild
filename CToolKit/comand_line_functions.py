from typing import List

from CToolKit.Errors.CopilationError import CopilationError
from CToolKit.Errors.CopilationWarning import CopilationWarning

from CToolKit.Errors.ValgrindError import  ValgrindError
from CToolKit.Errors.ValgrindLeak import  ValgrindLeak
from CToolKit.Errors.NotExpectedResult import NotExpectedResult

from CToolKit.ComandLineExecution import ComandLineExecution
from .valgrind_parser import parse_valgrind_result
from platform import system as current_os
from os.path import isdir
from os import listdir,remove
from .output_formatation import sanitize_value


def compile_project_by_command(command: str, raise_errors: bool = True, raise_warnings: bool = True):
    """execute an copilation with the given comand
    Args:
        command (str): the comand copilation ,ex: 'gcc test.c'
        raise_errors (bool, optional): if its to raise An copilation Error
        raise_warnings (bool, optional): if is to raise an warning Error

    Raises:
        CopilationError: The Copilation Error Exception
        CopilationWarning: The CopilationWarning Exception
    """
    
    result = ComandLineExecution(command)

    if raise_errors and result.status_code != 0:
        raise CopilationError(result.output, result.status_code)


    if raise_warnings and 'warning:' in result.output:
        raise CopilationWarning(result.output)


def compile_project( file: str,compiler ='gcc', output: str = None, flags: List[str] = None, raise_errors: bool = True,
                    raise_warnings: bool = True)->str:
    """Copiles an project file

    Args:
        compiler (str): the current compiler , ex: gcc,clang
        file (str): the file to copile, ex: test.c
        output (str, optional): the file output, ex: test.out ,if were None , it will be
        the file replaced with .out or .exe
        flags (List[str], optional): the optional flags copilatin
        raise_errors (bool, optional): if its to raise An copilation Error
        raise_warnings (bool, optional): if is to raise an warning Error

    Raises:
        CopilationError: The Copilation Error Exception
        CopilationWarning: The CopilationWarning Exception
    """
    if flags is None:
        flags = []

    if output is None:
        if current_os() == 'Windows':
            output = file.replace('.c', 'exe').replace('.cpp', '.exe')
        else:
            output = file.replace('.c', '.out').replace('.cpp', '.out')

    command = f'{compiler} {file} -o {output} ' + ' '.join(flags)
    compile_project_by_command(command, raise_errors, raise_warnings)
    return output





def test_binary_with_valgrind(binary_file:str,flags: List[str]= None)->dict:
    """ will test an binary execution with valgrind
    Args:
        binary_file (str): the binary execution ex: test.out
        flags (List[str], optional): addition flags to the copilation

    Raises:
        ValgrindError: And valgrind Error ex: an buffer overflow
        ValgrindLeak: _An valgrind leak, ex: an non free alocation
    """
    if flags is None:
        flags = []

    command = f'valgrind  ./{binary_file} ' + ' '.join(flags)
    result = ComandLineExecution(command)

    #(result.output)
    parsed_result = parse_valgrind_result(result.output)


    if 'ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)' not in result.output:
        raise ValgrindError(result.output,parsed_result)

    if 'All heap blocks were freed -- no leaks are possible' not in result.output:
        raise ValgrindLeak(result.output,parsed_result)
    
    return parsed_result

    


def execute_test_for_file(file: str,compiler='gcc',use_valgrind=True,raise_warnings=True)->dict or ComandLineExecution:
    """Execute an presset test for the current file
    Args:
        compiler (str): the compiler to use, ex: gcc or clang
        file (str): the file to copile , ex: test.c
        raise_warnings(bool): if its to raise warnings generated
    Raises:
        e: all possible errors
    """
    result = compile_project(
        file,
        compiler,
        raise_errors=True,
        raise_warnings=raise_warnings
    )
    if not use_valgrind:
        return  ComandLineExecution(result)

    try:
        valgrind_test = test_binary_with_valgrind(result)
        remove(result)
    except Exception as e:
        remove(result)
        raise e

    return valgrind_test


def get_expected_file(folder:str)->str or None:
    for file in listdir(folder):
        if file.startswith('expected'):
            return f'{folder}/{file}'


def execute_folder_presset(compiler:str,use_valgrind:bool, folder: str,raise_warnings:bool)->dict or ComandLineExecution:
    files = listdir(folder)

    target = f'{folder}/exec.c'

    if 'exec.c' not in files:
        raise FileNotFoundError(folder)


    expected_file_name = get_expected_file(folder)


    if expected_file_name is None:
        raise FileNotFoundError(
            'expected.txt'
        )

    with open(expected_file_name,'r') as arq:
        expected = sanitize_value(expected_file_name,arq.read())
        

    if use_valgrind:
        r:dict = execute_test_for_file( target, compiler,True, raise_warnings)
        saninitzed_result = sanitize_value(expected_file_name,r['output'])
    else:
        r:ComandLineExecution = execute_test_for_file( target,compiler, False, raise_warnings)
        saninitzed_result = sanitize_value(expected_file_name,r.output)

    if expected != saninitzed_result:
        raise NotExpectedResult(saninitzed_result,expected)


    return r

    
    
          
    
def execute_test_for_folder(folder: str,compiler='gcc' ,print_values = True,use_valgrind=True, raise_warnings=True):
    """execute tests for all .c or cpp files in the given folder
    Args:
        compiler (str): the compiler, ex: gcc , or clang
        folder (str): the folder to copile
        print_values (bool, optional): if is to print errors and sucess
        raise_warnings(bool): if its to raise warnings generated
    Raises:
        e: if happen some error
    """
    
    print('\033[92m'+f'folder: {folder}')
    
    elements = listdir(folder)
    for element in elements:
        current_path = f'{folder}/{element}'
        
        if isdir(current_path):
            current_folder = current_path
            if element.startswith('##'):
                try:
                    execute_folder_presset(compiler,use_valgrind, current_folder, raise_warnings)
                    print('\033[92m' + f'\tpassed: {element}' + '\33[37m')
                except Exception as e:
                    print('\033[91m' + f'fail with folder: {element}' + '\33[37m')
                    raise e

            else:
                execute_test_for_folder(current_folder,compiler,print_values,use_valgrind,raise_warnings)
            continue


        if not element.endswith('.c') or element.endswith('.cpp'):
            continue
            
        try:
            execute_test_for_file( current_path,compiler,use_valgrind,raise_warnings)
            if print_values:
                print('\033[92m'+f'\tpassed: {element}' + '\33[37m')
        except Exception as e:
            if print_values:
                print('\033[91m' + f'fail with file: {element}' + '\33[37m')
                print('\033[0m')
            raise e



def create_code_presset(compiler:str,use_valgrind:bool, folder: str,raise_warnings:bool):
    files = listdir(folder)

    target = f'{folder}/exec.c'

    if 'exec.c' not in files:
        raise FileNotFoundError(folder)

    expected_file_name = get_expected_file(folder)

    if expected_file_name is not None:
        return


    if use_valgrind:
        r: dict = execute_test_for_file( target,compiler, True, raise_warnings)
        saninitzed_result = sanitize_value('expected.txt', r['output'])
    else:
        r: ComandLineExecution = execute_test_for_file( target,compiler, False, raise_warnings)
        saninitzed_result = sanitize_value('expected.txt', r.output)

    with open(f'{folder}/expected.txt','w') as arq:
        arq.write(saninitzed_result)


def generate_output_of_execution(folder:str,compiler='gcc',use_valgrind=True,raise_warnings=True):
    files = listdir(folder)
    for file in files:
        file_path = f'{folder}/{file}'
        if isdir(file_path):
            if file.startswith('##'):
                create_code_presset(compiler,use_valgrind,file_path,raise_warnings)
                continue
            generate_output_of_execution(file_path,compiler)

