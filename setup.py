import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zerorest",
    version="1.0.0",
    author="SecNex",
    author_email="dev@secnex.io",
    description="A simple http client with zero dependencies and modern features like modern authentication.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.serverify.de/SecNex/zerorest",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)
