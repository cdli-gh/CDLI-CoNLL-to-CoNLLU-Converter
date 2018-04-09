from setuptools import find_packages, setup

dependencies = ['click']

setup(
    name='cdliconll2conllu',
    version='2.0.8',
    url='https://github.com/cdli-gh/CDLI-CoNLL-to-CoNLLU-Converter',
    license='BSD',
    author='Anoosha Sagar',
    author_email='anooshasagar@gmail.com',
    description='CDLI CoNLL to CoNLL-U Converter',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,

    entry_points={

        'console_scripts': [
            'cdliconll2conllu = cdliconll2conllu.cli:main'
        ]
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)