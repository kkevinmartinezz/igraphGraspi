from setuptools import setup

setup(
    name='graspi_igraph',
    version='0.1',
    description='Graspi igraph',
    url='https://github.com/wenqizheng326/graspi_igraph.git',
    author='Kevin Martinez',
    author_email='kem44@buffalo.edu',
    license='Apache License 2.0',
    packages=['graspi_igraph'],
    install_requires=[
        'igraph',
        'matplotlib',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)