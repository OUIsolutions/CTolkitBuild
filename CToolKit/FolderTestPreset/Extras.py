
from .Print import FolderTestPressetPrints
from os import listdir
from os.path import isdir,isfile
from os.path import getmtime
from os import  remove
import hashlib

import zipfile


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

        name = f'{self._side_effect_folder}.zip'
        with zipfile.ZipFile(name, 'w') as zip:
            zip.write(self._side_effect_folder)

        sha256 = hashlib.sha256()
        with open(name, 'rb') as arq:
            sha256.update(arq.read())
        self._original_sha  =sha256.hexdigest()

        print(f'original sha {self._original_sha}')


    def _side_effect_folder_changed(self)->bool:
        if self._side_effect_folder is None:
            return False

        if not isdir(self._side_effect_folder):
            raise FileNotFoundError(f'{self._side_effect_folder} is not present')

        name = f'{self._side_effect_folder}_generated.zip'
        with zipfile.ZipFile(name, 'w') as zip:
            zip.write(self._side_effect_folder)


        sha256 = hashlib.sha256()
        with open(name, 'rb') as arq:
            sha256.update(arq.read())
        novo_sha  =sha256.hexdigest()
        print(f'novo sha {novo_sha}')

        try:
            remove(name)
        except FileNotFoundError:
            pass













