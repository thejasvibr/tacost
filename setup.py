"""Setup for the chocobo package."""

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Thejasvi Beleyur",
    author_email="thejasvib@gmail.com",
    name='testacoustictracking',
    license="MIT",
    description='A package to create simulated sound sources/ trajectories to test accuracy of an acoustic tracking system',
    version='v0.0.0',
    long_description=README,
    url='https://github.com/thejasvibr/test_acoustictracking.git',
    packages=setuptools.find_packages(),
	install_requires=['numpy', 'matplotlib','pandas','soundfile','scipy'],
    python_requires=">=3.5",
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Science/Research',
    ],
)