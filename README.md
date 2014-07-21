# statement2db

statement2db is Flask application that reads bank statements in a csv format and returns
a JOSON object with the extracted information.

## Development Environment

At the bare minimum you'll need the following for your development environment:

1. [Python](http://www.python.org/)
2. [MySQL](http://www.mysql.com/)

It is strongly recommended to also install and use the following tools:

1. [virtualenv](https://python-guide.readthedocs.org/en/latest/dev/virtualenvs/#virtualenv)
2. [virtualenvwrapper](https://python-guide.readthedocs.org/en/latest/dev/virtualenvs/#virtualenvwrapper)

### Local Setup

The following assumes you have all of the recommended tools listed above installed.

#### 1. Clone the project:

    $ git clone git@github.com:tmusy/statement2db.git
    $ cd statement2db

#### 2. Create and initialize virtualenv for the project:

    $ mkvirtualenv [path to your virtualenv directory]/statement2db
    $ pip install -r requirements.txt

### Development

If all went well in the setup above you will be ready to start hacking away on
the application.

#### Tests

To run the tests use the following command:

    $ nosetests
