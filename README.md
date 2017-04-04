# key-value-store

Provide a RESTful API to the backend metadata.

## Installation

    $ pip install -r requirements.txt

## Instruction:

- First step is to install the requirements as described above.<br />
- Make sure you have a MySQL server up and running with the following credentials<br />
  conf = {'metadata': 'mysql+pymysql://root:password@localhost:3306'}<br />
- Database is being generated via `alembic` so you can easily upgrade and downgrade it. You need to
  go to the root of repository and just run:<br />
  $ alembic upgrade head
- To be able to run some tests you need to run two processes one to handle api requests and one to
  take care of callbacks (separate shells):<br />
  $ python api.py --port 9000<br />
  $ python api.py --port 5000

- Following are some examples:

    curl http://localhost:9000/17
    
    curl -X POST -F 'value=300' http://localhost:9000/17<br />
    curl http://localhost:9000/17/callback<br />
    curl http://localhost:9000/17<br />
    
    curl -X POST -F 'value=400' -F 'url=http://localhost:5000/valuechecker/only_digits_fast' http://localhost:9000/17/callback<br />
    curl http://localhost:9000/17/callback<br />
    curl http://localhost:9000/17<br />
    
    curl -X POST -F 'value=500' -F 'url=http://localhost:5000/valuechecker/only_digits_medium' http://localhost:9000/17/callback<br />
    curl http://localhost:9000/17/callback<br />
    curl http://localhost:9000/17<br />
    
    curl -X POST -F 'value=600' http://localhost:9000/17<br />
    curl http://localhost:9000/17/callback<br />
    curl http://localhost:9000/17<br />
    
    curl -X POST -F 'value=700' -F 'url=http://localhost:5000/valuechecker/only_digits_slow' http://localhost:9000/17/callback<br />
    curl http://localhost:9000/17/callback<br />
    curl http://localhost:9000/17<br />

## Following command will not go through since only_digits_slow is taking more that 5 second.
    curl -X POST -F 'value=800' http://localhost:9000/17
    curl http://localhost:9000/17/callback
    curl http://localhost:9000/17
    
    Missing values and wrong formats:
    curl -X POST -F 'url=http://localhost:5001' http://localhost:9000/12
    curl -X POST -F 'urlurl=http://localhost:5001' http://localhost:9000/12
    curl -X POST -F 'value=aliali' -F 'http://localhost:5000' http://localhost:9000/17/callback


## Callback endpoints:
    curl 'http://localhost:9000/valuechecker/only_digits_fast?key=12'
    curl 'http://localhost:9000/valuechecker/only_digits_medium?key=12'
    curl 'http://localhost:9000/valuechecker/only_digits_slow?key=12'
    curl 'http://localhost:9000/valuechecker/only_digits_fast?key=text'
    curl 'http://localhost:9000/valuechecker/only_digits_medium?key=text'
    curl 'http://localhost:9000/valuechecker/only_digits_slow?key=text'