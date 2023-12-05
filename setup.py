from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = '-e .'

def get_package_requirements(file_path:str) -> List[str]:
    """
    Read package requirement text file, and output list of package names.
    """
    with open(file_path, 'r') as file_obj:
        packages = file_obj.readlines()
        required_packages = [ package.strip() for package in packages ]

    if HYPHEN_E_DOT in required_packages:
        required_packages.remove(HYPHEN_E_DOT)

    return required_packages

setup(
    name='mlproject',
    version='0.0.1',
    author='Bonny',
    packages=find_packages(),
    install_requires=get_package_requirements('requirements.txt')
)