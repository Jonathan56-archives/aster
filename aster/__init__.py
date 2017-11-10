import os
import shutil
dir_path = os.path.dirname(os.path.realpath(__file__))

def new(destination):
    src = os.path.join(dir_path, '..', 'example', 'new_project')
    shutil.copytree(src, destination)
    print('COPIED!')
