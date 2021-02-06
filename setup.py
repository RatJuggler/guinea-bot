from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='guineabot',
    version='0.2.0',
    description='A guinea pig Twitter bot.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='John Chase',
    author_email='ratteal@gmail.com',
    python_requires='>=3.7',
    url='https://github.com/RatJuggler/guinea-bot',
    packages=find_packages(exclude=['tests']),
    package_data={
        'guineabot': ['guinea_pig_sayings.json'],
    },
    entry_points={
        'console_scripts': [
            'guineabot = guineabot.__main__:simulate_guinea_pig',
        ]
    },
    install_requires=[
        # Check latest releases on piwheels: https://www.piwheels.org/
        'click ==7.1.2',
        'environs ==9.3.0',
        'tweepy ==3.10.0',
    ],
    test_suite='tests',
    tests_require=[
        'coverage',
        'flake8',
        'testfixtures',
        'tox'
    ],
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX :: Linux',
        'Topic :: Games/Entertainment :: Simulation'
    ]
)
