Contributing
---

To set up a development version of the project:

- Clone this project;
- Build a virtual environment;
- Install requirements;
- Run the tests.

```
% git clone https://github.com/ehmatthes/py-image-border.git
$ cd py-image-border 
$ python -m venv .venv
$ source .venv/bin/activate
(.venv)$ pip install --upgrade pip
(.venv)$ pip install -r requirements.txt 
(.venv)$ pytest 
```

If all of the tests pass, you're ready to start working on the project.

Pushing changes
---

To push changes, make sure you've bumped the version number. Then remove any existing distribution files, build the project, and upload to PyPI:

```
(.venv)$ rm -rf dist/
(.venv)$ python -m build
(.venv)$ python -m twine upload dist/*
```
