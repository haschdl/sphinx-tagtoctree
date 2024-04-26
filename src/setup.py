
import setuptools
from sphinx_tagtoctree import _version
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='sphinx-tagtoctree',
    version=_version.__version__,
    author="Half Scheidl",
    author_email="noreply@hscheidl.com",
    url="https://github.com/haschdl/sphinx-tagtoctree",
    description="Sphinx table-of-contents with super powers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['sphinx','boolean.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
