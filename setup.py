from distutils.core import setup
import setuptools
import os

# In CI, version is driven by the git tag (e.g. v0.3.2 -> 0.3.2).
# Locally falls back to 0.0.0.dev so the package can still be installed.
version = os.environ.get('GITHUB_REF_NAME', '0.0.0.dev').lstrip('v')

setup(
    name = 'BackTranslation',
    version = version,
    author = "Zhiqiang Wu",
    author_email = "wzq0515@gmail.com",
    license = "MIT",
    url = "https://github.com/hhhwwwuuu/BackTranslation",
    description = "Back translation for Natural Language Processing (NLP) using Google Translate",
    long_description = open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",

    python_requires='>=3',
    packages=setuptools.find_packages(),
    keywords = ['Translation', 'NLP', 'back-translation'],
    classifiers=[
        'Development Status :: 4 - Beta',
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.0",
    ],
    install_requires = ['googletrans==4.0.0rc1', 'nltk']
)