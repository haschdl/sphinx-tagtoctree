# Sphinx Extension: TagTocTree

This is an extension to the documentation engine [Sphinx](http://www.sphinx-doc.org/).
It allows you to include pages in a table-of-contents by using tags assigned to a page.

## How it works

This extension adds a new directive `tagtoctree`, which creates a tree-like
table-of-contents, filtering pages by a tag filter.

Directive    |   Configuration                   | Produces                          |
-------------|-----------------------------------|-----------------------------------|
`toctree` (*)| ![](docs/2019-11-26-17-21-26.png) | ![](docs/2019-11-26-17-21-57.png) |
`tagtoctree` | ![](docs/2019-11-26-17-22-54.png) | ![](docs/2019-11-26-17-22-22.png) |

(*) Sphinx native [`toctree`](https://www.sphinx-doc.org/en/1.8/usage/restructuredtext/directives.html#directive-toctree)

## Usage

The documentation assumes you have a Sphinx project running.

- Install using PIP:

    ```bash
    pip install sphinx-tagtoctree
    ```

- In your Sphinx configuration file (`conf.py`), add a entry for `tagtoctree`:

    ```python
    extensions = [
        'sphinx_tagtoctree'
    ]
    ```

- (Optional) Add configuration value for `tagtoctree_tag`. If none is provided, the default `tagtoctree` will be used.

   ```python
   tagtoctree_tag = 'tagtoctree'
   ```

- For each page, add a header on the top with the values of your tags. See examples [page1](/example/source/page1.rst) and
 [page2](/example/source/page2.rst) in this repo.
     
- Finally, add a `tagtoctree` directive where you want your table-of-contents to be displayed. Example:

  ```rst
    .. tagtoctree::
    :maxdepth: 1
    :glob:
    :caption: Pages with tag "Product"
    :tag: Product

    **
 ```
