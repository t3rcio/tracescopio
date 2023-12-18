from pathlib import Path
from setuptools import setup, find_packages

VERSION = '2.0.1' 
DESCRIPTION = 'Tracescopio - um capturador simples de tracebacks'
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Setting up
setup(        
    name="tracescopio", 
    version=VERSION,
    author="Tercio A Oliveira",
    author_email="t3rcio@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['django', 'requests'], # adicione outros pacotes que         
    
    keywords=['python', 'traceback'],
    classifiers= [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",            
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)"
    ]
)