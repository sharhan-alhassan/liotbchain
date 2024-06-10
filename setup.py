from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name='liotbchain',
    version='0.0.8',
    description='Python Lightweight IOT Blockchain framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sharhan Alhassan',
    author_email='sharhanalhassan@gmail.com',
    url='https://github.com/sharhan-alhassan/liotbchain',
    packages=find_packages(exclude=['tests']),
    install_requires=requirements,
    keywords='blockchain python iot framework',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
