# Python-Pinboard

Python module to access Pinboard via its API. This project is a fork from the original work by Paul Mucur on the Python-Delicious API.

## Installation

To install using easy-install:

```bash
    python setup.py install
```

Or (if you have pip installed)

```bash
    pip install -e git://github.com/mgan59/python-pinboard.git@v1.1#egg=python-pinboard
```

## Usage

To get started you must first open a connection to pinboard.in, there are authentication methods


Standard method using `username/password`
```python

import pinboard

# create pinboard connection (using username/password)
pinboard_conn = pinboard.open('username', 'password')
```

A method using your `api token` from the pinboard.in settings
```python
# an alternative method using an api token
pinboard_conn = pinboard.open(token='username:23asdfjlkj')
```

Now how to actual `add` and `delete` bookmarks
```python
# Example of adding a bookmark
# .add('url', 'title', 'description', ('tags', 'as', 'a', 'tuple'))
p.add('https://github.com/mgan59/python-pinboard/',
	'Python-Pinboard',
	'A Python module to access the contents of a Pinboard account via the Pinboard API.',
	('computing', 'python'))

# .add without a description but using a kwarg tags to specify the tuple
p.add('https://github.com/mgan59/python-pinboard',
	'Python-Pinboard',
	tags=('computing', 'python', 'projects'))

# .delete uses the bookmark url since they are unique
p.delete('https://github.com/mgan59/python-pinboard')
```


## Contributors
--
* Original Creator [Paul Mucur](https://github.com/mudge)
* [Morgan Craft](https://github.com/mgan59)


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/mgan59/python-pinboard/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

