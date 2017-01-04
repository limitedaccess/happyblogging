# happyblogging

## Install requirements
`pip install -r requirements-local.txt`
`pip install -r requirements-vendor.txt -t lib/`

## Running app locally
`dev_appserver.py --port=9999 .`

## Running unit test
`nosetests --with-gae blog`
or we can just run
`python runner.py ~/google-cloud-sdk` 
or 
`python blog/tests.py`
