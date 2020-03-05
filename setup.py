from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='guineabot',
    version='0.0.5',
    description='A guinea pig Twitter bot.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='John Chase',
    author_email='ratteal@gmail.com',
    python_requires='>=3.5.3',
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
        'click ==7.0',
        'tweepy ==3.8.0'
    ],
    license='MIT',
)
