
import setuptools
with open("../README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='sphinx-tagtoctree',
    version='0.9.0',
    author="Half Scheidl",
    author_email="noreply@hscheidl.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['sphinx'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
