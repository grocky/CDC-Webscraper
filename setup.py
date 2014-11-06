from setuptools import setup
import io
import codecs
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')

setup(
        name='cdc_webscraper',
        version='0.0.1',
        url='https://github.com/grocky/CDC-Webscraper/',
        license='Apache Software License',
        author='Rocky Gray',
        install_requires=['requests>=2.4.3',
            'BeautifulSoup4>=4.2.0'],
        author_email='rocky.grayjr@gmail.com',
        description='A tool to validate STD clinic addresses on the CDC website',
        long_description=long_description,
        packages=['cdc_webscraper'],
        include_package_data=True,
        platforms='any',
        classifiers = [
            'Programming Language :: Python',
            'Development Status :: 1 - Beta',
            'Natural Language :: English',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Libraries :: Application Frameworks',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            ],
        extras_require={
            }
        )
