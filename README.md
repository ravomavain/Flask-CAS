Flask-CAS
=========

[![Build Status](https://travis-ci.org/cameronbwhite/Flask-CAS.png?branch=master)](https://travis-ci.org/cameronbwhite/Flask-CAS)

Flask extension for CAS

## Installation ##

### PyPI ###

Flask-CAS is available on PyPI! You can install it with pip.

```sh
pip install Flask-CAS
```

### Manual ###

If you want to do it the hard way you can clone the repository and
install Flask-CAS in a virtualenv. 

1. Clone it `git clone git@github.com:cameronbwhite/Flask-CAS.git`
2. Enter it `cd Flask-CAS`
3. Create a virtualenv and enter it (Optional) `virtualenv venv && source venv/bin/activate`
4. Install it `python setup.py install`

## Instructions ##

After Flask-CAS is installed you will be able to import the `flask_cas`
packages. There is only one thing you care about inside the package
which is the `CAS` class.

```python
from flask_cas import CAS
```

There are two ways to use the `CAS` class.

1. Add the application object at construction time

    ```python
    app = Flask(__name__)
    CAS(app)
    ```

2. Or initialize the application with `CAS.init_app`

    ```python
    cas = CAS()
    app = Flask(__name__)
    cas.init_app(app)
    ```

The `CAS` class will add two routes `/login/` and `/logout/`. You can
prefix these routes if you pass a second argument to the `CAS`
constructor or `init_app` depending on the method you choose.

The `/login/` route will redirect the user to the CAS specified by the
`CAS_SERVER` configuration value. If login is successful the user will
be redirect to the endpoint specified by the `CAS_AFTER_LOGIN`
configuration value, and the logged in user's `username` will be store 
in the session under the key specified by the `CAS_USERNAME_SESSION_KEY` 
configuration value.

The `/logout/` route will redirect the user to the CAS logout page and
the `username` will be removed from the session.

### Configuration ###

#### Required Configs ####

|Key             | Description                              | Example              |
|----------------|------------------------------------------|----------------------|
|CAS_SERVER      | URL of CAS                               | 'http://sso.pdx.edu' |  
|CAS_AFTER_LOGIN | Endpoint to go to after successful login | 'root'               |

#### Optional Configs ####

|Key                      | Default        |
|-------------------------|----------------|
|CAS_TOKEN_SESSION_KEY    | '_CAS_TOKEN'   |
|CAS_USERNAME_SESSION_KEY | 'CAS_USERNAME' |

## Example ##

```python
import flask
from flask import Flask

import flask_cas

app = Flask(__name__)
flask_cas.CAS(app, '/cas')
app.config['CAS_SERVER'] = 'https://sso.pdx.edu' 
app.config['CAS_AFTER_LOGIN'] = 'route_root'

@app.route('/')
def route_root():
    return flask.render_template(
        'layout.html',
        username = flask.session.get(app.config['CAS_USERNAME_SESSION_KEY'], None),
    )
```
