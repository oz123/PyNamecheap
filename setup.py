
import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='PyNamecheap',
    version='0.0.3',
    url='https://github.com/Bemmu/PyNamecheap',
    license='MIT',
    author='Bemmu Sepponen',
    author_email='me@bemmu.com',
    description='Namecheap API client in Python',
    package_dir={"": "src"},
    platforms='any',
    install_requires=['requests'],
    entry_points={
        "console_scripts": ["namecheap = namecheap.cli:main"]},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
