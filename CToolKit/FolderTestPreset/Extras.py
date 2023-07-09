
from .Print import FolderTestPressetPrints
from os import listdir
from os.path import isdir,isfile
from os.path import getmtime
from os import  remove
from os.path import  dirname
import zipfile
from shutil import rmtree,make_archive
import hashlib



class FolderTestPresetExtras(FolderTestPressetPrints):

    def _get_expected_file(self, folder: str):
        elements = listdir(folder)
        for e in elements:
            if isdir(e):
                continue

            if e.startswith('expected'):
                return f'{folder}/{e}'


    def _get_file_to_execute(self, folder: str):
        c_file = f'{folder}/exec.c'
        cpp_file = f'{folder}/exec.cpp'

        if isfile(c_file):
            return c_file

        if isfile(cpp_file):
            return cpp_file

        raise FileNotFoundError(f'could not locate an exec.c or exec.cpp in {folder}')


    def _create_side_effect_zip(self):
        if self._side_effect_folder is None:
            return

        make_archive(self._side_effect_folder,'zip',self._side_effect_folder)
        name = f'{self._side_effect_folder}.zip'

        with open(name, 'rb') as arq:
            sha256 = hashlib.sha256()
            sha256.update(arq.read())
            self._original_sha  =sha256.hexdigest()


    def _side_effect_folder_changed(self)->bool:


        if self._side_effect_folder is None:
            return False

        if not isdir(self._side_effect_folder):
            raise FileNotFoundError(f'{self._side_effect_folder} is not present')

        name = f'{self._side_effect_folder}_generated'
        make_archive(name,'zip',self._side_effect_folder)

        sha256 = hashlib.sha256()
        with open(name + '.zip', 'rb') as arq:
            sha256.update(arq.read())
        novo_sha = sha256.hexdigest()

        try:
            remove(name + '.zip')
        except FileNotFoundError:
            pass

        return novo_sha != self._original_sha



    def _rebase_side_effect_folder(self):

        name = f'{self._side_effect_folder}.zip'
        rmtree(self._side_effect_folder,ignore_errors=True)
        with zipfile.ZipFile(name, 'r') as zip_ref:
            zip_ref.extractall(self._side_effect_folder)


    def __del__(self):
        '''if self._side_effect_folder is None:
            return False
        name = f'{self._side_effect_folder}.zip'
        try:
            remove(name)
        except FileNotFoundError:
            pass'''











