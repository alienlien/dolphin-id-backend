# Dolphin ID Backend

It provides the disk IO for the frontend.
It basically provides the following functions:

- List the folder contents (images and label files) for the path input.
- Load label files from local disk.
- Load image from local dist.
- Save label file to local disk.

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

## Test 

Try to get file list for some folder at local:

```
curl -X GET 'http://localhost:5000/dir?root_path=[root_path]'
```

Example:

```
$ curl -X GET 'http://localhost:5000/dir?root_path=/Users/Alien/workspace/project/private/dolphin-id-backend/data/'
{
  "contents": {
    "dirs": [],
    "files": [
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (80).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (81).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (82).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (83).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (84).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (85).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (86).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (87).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (88).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (89).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (90).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (91).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (92).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (93).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (94).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (95).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (96).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (97).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (98).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (99).JPG",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01via_region_data_ID.json",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/test.json",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/via_region_data HL20100702_01.json",
      "/Users/Alien/workspace/project/private/dolphin-id/data/test/via_region_data_2.json"
    ]
  },
  "root_dir": "/Users/Alien/workspace/project/private/dolphin-id/data/test"
}
```
