from setuptools import setup, find_packages

HYPEN_E_DOT = '-e .'

def get_requirements(file_path:str):

    with open(file_path, 'r') as file_obj:
        packages = file_obj.readlines()

        required_packages = [package.strip() for package in packages]

    if HYPEN_E_DOT in required_packages:
        required_packages.remove(HYPEN_E_DOT)

    return required_packages

setup(
    name='mlproject',
    version='0.0.1',
    author='Bonny'
    packages=find_packages(),
    install_requires=get_requirememts()
)