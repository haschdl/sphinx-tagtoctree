# Contributing

PRs are welcome!


## Notes to developer

1. Generating a new distribution for PyPi

Run `python setup.py sdist` from your source folder `src` to generate a source distribution.

## Debugging

To debug the Sphinx extension, add the following code to where you wish to wait for debugger
to be attached:

```python
    print("Waiting for debugger attach (run)")
    # 5678 is the default attach port in the VS Code debug configurations    
    import ptvsd
    ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
    ptvsd.wait_for_attach()
    breakpoint()
```