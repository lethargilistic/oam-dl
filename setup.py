from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='oam-dl',
    version='0.2.0',
    description='Download any or all Ozy and Millie comics',
    long_description=long_description,
    url='https://github.com/lethargilistic/oam-dl',
    author='Mike Overby',
    author_email='mikeoverby@outlook.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords=['cli', 'commandline', 'download', 'api'],
    packages=find_packages(),
    install_requires=['docopt==0.6.2',
                      'progress==1.2',
                      'requests==2.8.1',
                      'wheel==0.26.0'],
    entry_points={
        'console_scripts': [
            'oam-dl=oamdl.__init__:main',
        ],
    },
)
