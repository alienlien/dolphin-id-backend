## Setup

- Install `pyenv` to manage different versions of python. [Reference](https://github.com/pyenv/pyenv)

```
$ brew install pyenv
```

- Use pyenv to install `python 3.6.x`.

```
$ pyenv install 3.6.11
```

- Install `pipenv` to manage the python virtual environments. [Reference](https://pipenv.pypa.io/en/latest/)

```
$ pip3 install pipenv
```

- Use `pipenv` to create virtual env for `python 3.6.x`. 
    - Note that one can point the python3 binary file (installed through `pyenv`) directly rather than switching by pyenv. 

```
$ pipenv --python /Users/Alien/.pyenv/versions/3.6.9/bin/python3.6
$ pipenv install 
$ pipenv shell
```

- Start the api server for disk IO.

```
$ python3 -m script.run
```
