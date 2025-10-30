"""
Setup configuration for YourAIDetector package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='youraidetector',
    version='1.0.0',
    author='YourAIDetector Team',
    author_email='contact@youraidetector.com',
    description='A comprehensive AI content detection tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bf20162/YourAIDetector',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Text Processing :: Linguistic',
    ],
    python_requires='>=3.8',
    install_requires=[
        'transformers>=4.30.0',
        'torch>=2.0.0',
        'numpy>=1.24.0',
        'scipy>=1.10.0',
        'pypdf>=3.15.0',
        'python-docx>=0.8.11',
        'pytesseract>=0.3.10',
        'Pillow>=9.5.0',
        'nltk>=3.8.0',
        'spacy>=3.5.0',
        'click>=8.1.0',
        'colorama>=0.4.6',
        'tqdm>=4.65.0',
        'pyyaml>=6.0',
        'loguru>=0.7.0',
    ],
    entry_points={
        'console_scripts': [
            'aidetector=aidetector.cli:main',
        ],
    },
    keywords='ai detection content-analysis machine-learning nlp',
    project_urls={
        'Bug Reports': 'https://github.com/bf20162/YourAIDetector/issues',
        'Source': 'https://github.com/bf20162/YourAIDetector',
    },
)
