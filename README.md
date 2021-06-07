[Freeze](https://docs.python-guide.org/shipping/freezing/#id1) your Python code to distribute a binary.

Install `pyenv` Python version with `enable-shared` option [1][1]:

```fish
PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.9.5
```

Build with PyInstaller:

```shell
make build
```

:( the single-file mode is super slow because it forces PyInstaller to unpack all the files in a temp folder before executing... what a crap..

Trying with Nuitka:

```shell
pip install Nuitka
python -m nuitka --standalone main.py
# Nothing installed, got a linker error
python -m nuitka --jobs=4 --standalone main.py
# Same error
python -m nuitka --jobs=4 --show-scons --follow-imports main.py
# Compiled right, but I forgot to make it 'standalone'
python -m nuitka --jobs=8 --show-scons --standalone --follow-imports main.py
# Same error
PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.9.5
~/.pyenv/versions/3.9.5/bin/python -m venv .venv && . .venv/bin/activate.fish
pip install -r requirements.txt
python -m nuitka --jobs=8 --show-scons --standalone --follow-imports main.py
# No error!
./main.dist/main
# I forgot a dependency (typing.List)
python -m nuitka --jobs=8 --show-scons --standalone --follow-imports main.py
./main.dist/main
# Works, but slow startup time
python -m nuitka --jobs=8 --show-scons --onefile --follow-imports main.py
# FATAL: Error, unsupported OS for onefile 'Darwin'
```

[1]: https://pyinstaller.readthedocs.io/en/stable/development/venv.html "?"