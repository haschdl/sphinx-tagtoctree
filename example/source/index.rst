TagTocTree (Sphinx extension)
=============================

Built-int TocTree
~~~~~~~~~~~~~~~~~
A standard TocTree is generated with the `toctree` directive. 

.. code-block::

    .. toctree::
        :maxdepth: 2
        :caption: All pages (using built-in toc tree):
        :glob:

        **

.. toctree::
   :maxdepth: 2
   :caption: All pages (using built-in toc tree):
   :glob:

   **

Tag TocTree: Tag filter
~~~~~~~~~~~~~~~~~~~~~~~~

This extension allows you to filter pages by tags.
In your content pages, include a ``:tag:`` followed by list of tags, comma-separated. 
For example ``:tag: Product`` will include pages with `Product`.  ``:tag: Customer, Product`` 
will include pages with tags "Customer" and pages with the tag "Product". 
For more examples, check the pages under `/example/source`.

Showing only pages with tag "Product" 

.. code-block::

    .. tagtoctree::
        :maxdepth: 1
        :glob:
        :caption: Pages with tag "Product"
        :tag: Product

        **

.. tagtoctree::
   :maxdepth: 1
   :glob:
   :caption: Pages with tag "Product"
   :tag: Product

   **

.. tagtoctree::
   :maxdepth: 1
   :glob:
   :caption: Pages with tag "Sales"
   :tag: Sales

   **
   

.. tagtoctree::
   :maxdepth: 1
   :glob:
   :caption: Pages with tag "Customer" or "Product"
   :tag: Customer, Product

   **


Tag TocTree: Tag expression
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can specify a more complex filter using boolean expressions.
Examples of valid expressions are:

    * ``(Customer AND Product)`` Include pages with tags Customer and Product. 
    * ``(Customer OR Product) AND NOT(Sales)`` Include pages that have tags Customer or Product, but which do not have tag Sales. Equivalent to ``(Customer OR Product) AND ~ Sales``
    * ``(NOT Customer) AND NOT(Sales)`` Include pages that do have neither Customer nor Product.
    

.. tagtoctree::
   :maxdepth: 1
   :glob:
   :caption: Pages filtered with an expression: (Customer AND Product)
   :tag_expr: Customer AND Product

   **

.. tagtoctree::
   :maxdepth: 1
   :glob:
   :caption: Pages filtered with an expression: (Customer OR Product) AND Sales
   :tag_expr: (Customer OR Product) AND Sales

   **


.. tagtoctree::
   :maxdepth: 1
   :glob:
   :caption: Pages filtered with an expression: (Customer OR Product) AND NOT Sales
   :tag_expr: (Customer OR Product) AND NOT Sales

   **


.. tagtoctree::
   :maxdepth: 1
   :glob:
   :caption: Pages filtered with an expression: (NOT Customer) AND NOT(Sales)
   :tag_expr: (NOT Customer) AND NOT(Sales)

   **


Tag TocTree: Tags with hyphens
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The boolean expressions use the library [boolean.py](https://github.com/bastikr/boolean.py)
By default the characters ".:_" are allowed in tags. 
You can include `tagtoctree_allowed_in_token` in `conf.py`
with the list of additional characters allowed in tokens. 

See `/example/source/conf.py` for an example.

.. tagtoctree::
   :maxdepth: 1
   :glob:
   :caption: Pages with tag "funky-tag-with-hyphens" or "funk:24-23"
   :tag: funky-tag-with-hyphens OR funk:24-23

   **