#run python setup.py install

import os
import sys
from distutils.command.install_data import install_data
from distutils.command.install import INSTALL_SCHEMES

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

class osx_install_data(install_data):

    def finalize_options(self):
        #install.install_lib set to fixed directory
        self.set_undefined_options('install', ('install_lib', 'install_dir'))
        install_data.finalize_options(self)

if sys.platform == "darwin":
    cmdclasses = {'install_data': osx_install_data}
else:
    cmdclasses = {'install_data': install_data}


def fullsplit(path, result=None):
    #Split a pathname into components
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

#Put data_files in installabtion location
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# Compile the list of packages available
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
caya_dir = 'caya'

for dirpath, dirnames, filenames in os.walk(caya_dir):
    if os.path.basename(dirpath).startswith("."):
        continue
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

setup(
    name='caya',
    version='0.1',
    url="https://github.com/",
    author='Elkington',
    author_email='elkingtowa@gmail.com',
    license='MIT License',
    platforms=['any'],
    packages = packages,
    data_files=data_files,
    zip_safe=True,
)