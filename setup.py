from setuptools import setup, find_packages

version = __import__('tjango').get_version()


EXCLUDE_FROM_PACKAGES = ['tjango.conf.project_template',
                         'tjango.conf.app_template',
                         ]

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
    url='https://github.com/kidozh/tjango',
    install_requires=['tornado', 'peewee', 'psutil', 'bcrypt', 'peewee_migrate'],

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    # interface to tjango
    entry_points={
        'console_scripts': [
            'tjango-admin = tjango.management.console_command:execute_from_command_line',
        ],
    },
)
