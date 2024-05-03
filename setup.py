import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

__version__ = '0.0.0'

REPO_NAME = 'text-summarization'
AUTHOR_USER_NAME = 'trunglam2002'
SRC_REPO = 'text summerizer'
AUTHOR_EMAIL = 'trunglam2002@gmail.com'

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description='python package for text summerizer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/trunglam2002/text-summarization',
    project_urls={
        'Bug Tracker': 'https://github.com/trunglam2002/text-summarization/issues',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src')
)
