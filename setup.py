__author__ = "Benedict Thompson"
__version__ = "0.1p"

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="automod",
    version=__version__,
    author=__author__,
    author_email="thomp334@uni.coventry.ac.uk",
    description="An auto-moderator chat-bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/4006G2/AutoMod",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
