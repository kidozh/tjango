from setuptools import setup, find_packages

version = __import__('tjango').get_version()

# setup for tjango
setup(
    name='tjango',
    version=version,
    keywords='admin',
    description='A package to develop tornado in django style',
    license='MIT License',
    author='Kido Zhang',
    author_email='kidozh@kidozh.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=['tornado', 'peewee', 'psutil', 'bcrypt', 'peewee_migrate'],

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
