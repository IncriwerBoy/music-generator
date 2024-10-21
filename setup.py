from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = '-e .'
def get_requirements(file_path)->List[str]:
    requirements = []
    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [r.replace('\n', '') for r in requirements]
        
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    
    return requirements

setup(
    name='Music Generator',
    version='0.0.1',
    description='A pipeline for extracting midi files by crawling through website and training LSTM model to generate music.',
    author='labhesh',
    author_email='labheshmundhada23@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)