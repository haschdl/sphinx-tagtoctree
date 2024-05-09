# Contributing

PRs are welcome!


## Notes to developer

1. Make sure you have the latest `build` installed
`pip3 install --upgrade build`

2. Commit and push changes

3. Generate and push a new signed (`-s`) tag . A signed tag is required.

<<<<<<< HEAD
`git tag -s v0.9.5 -m "Release of filter expressions"`

=======
>>>>>>> 13febda (Build tools)
`git tag -s v0.9.5b -m "Release of filter expressions"`
`git push origin --tags`

4. Build and package with `python3 -m build`
Github action will then publish to PyPi on a new release.

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