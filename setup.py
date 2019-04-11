from distutils.core import setup
setup(
    name='versescraper',
    packages=['versescraper'],
    version='1.0',
    license='MIT',
    description='Fetch lyrics for an artist split into individual verses',
    author='Robert Firstman',
    author_email='firstmanrobert@gmail.com',
    url='https://github.com/RFirstman/versescraper',
    download_url='https://github.com/RFirstman/versescraper/archive/v1.0.tar.gz',
    keywords=["lyrics", "genius", "verse", "verses"],
    install_requires=['lyricsgenius'],
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
