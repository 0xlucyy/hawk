# hawk
Full Stack application which tracks ens domains. User can keep a list of domains they wish to track by ammending `watchlsits/watch.txt` file.

## Demonstration
https://github.com/0xlucyy/hawk/assets/109987865/c7546048-541e-4795-9a7b-196c37efad48






## Getting started
- Start mysql server. Run `mysql.server start`
- Run `python3 -m venv venv`
- Run `. venv/bin/activate`
- Run `pip install -e .`
- Run `clean_slate`
- Run `python app.py`
- Run `cd frontend/`
- Run `npm run start`


## Upgrade MySQL Database
- Modify any table in `backend/models/*.py` file.
- Run `alembic revision --autogenerate -m "describe model change(s)"`.
- Inspect newly created `alembic/versions/*.py` file to ensure changes have been captured accurately.
- Run `alembic upgrade head` to update db to latest version.


### To use scripts
- Run `python install -e .`.

### To auto installed
- Run `npm run setup`.


#### MY_NOTES MYSQL
/usr/local/opt/mysql/bin/mysqld_safe --datadir=/usr/local/var/mysql
brew services restart mysql
mysql.server stop
mysql.server start
mysql -u root -h localhost -p hawk
mysql -h sqlite:////Users/ancientevil/0x/hawk/ENS.db -u root

#### MY_NOTES DappNode
EXTRA_OPTIONS = --http.api eth,engine,net,web3,txpool

#### TODO Front end - LEGACY
- Run `npx create-react-app frontend`
- Add `"proxy": "http://localhost:5000",` to `frontend/package.json`.
- Run `npm run build`.

#### TODO UPDATE Instructions - LEGACY
- Clone to local workspace.
- Run `brew install mysql` if mysql not already installed.
- Run `python3 -m venv venv`
- Run `. venv/bin/activate`
- Run `pip install -e .`
- Run `alembic init alembic`
- Run `mysql.server start`
- Run `mysql -h localhost -u root -p` & insert password.
- Run `create database hawk;`
- Run `python app.py` to start server on port 5000.
- Run `curl http://127.0.0.1:5000/api/v1/health` to check server status.
