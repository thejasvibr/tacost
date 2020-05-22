"""Setup for the chocobo package."""
import tacost
import setuptools

version_number = tacost.__version__

setuptools.setup(
    author="Thejasvi Beleyur",
    author_email="thejasvib@gmail.com",
    name='tacost',
    license="MIT",
    description='tact: Test ACoustic Tracking: Create simulated sound sources/ trajectories to test the accuracy of an acoustic tracking system',
    version=version_number,
    long_description='docs/source/index.rst',
    url='https://github.com/thejasvibr/test_acoustictracking.git',
    packages=setuptools.find_packages(),
	install_requires=['numpy','pandas','pyyaml','scipy'],
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