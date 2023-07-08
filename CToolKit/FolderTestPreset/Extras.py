
from .Print import FolderTestPressetPrints
from os import listdir
from os.path import isdir,isfile
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



