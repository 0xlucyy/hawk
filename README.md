# hawk
domain watcher

#### Instructions
- Clone to local workspace.
- Run `brew install mysql` if mysql not already installed.
- Run `python3 -m venv venv`.
- Run `. venv/bin/activate`.
- Run `pip install -r requirements.txt`
- Run `alembic init alembic`
- Run `mysql.server start`.
- Run `mysql -h localhost -u root` & insert password.
- Run `create database hawk;`.
- Run `SET GLOBAL sql_mode = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION,ALLOW_INVALID_DATES';`.
- Exit mysql & run `mysql.server restart`.
- Run `python app.py` to start server on port 5000.
- Run `curl http://127.0.0.1:5000/api/v1/health` to check server status.

### Init DB with data
- Copy/Paste ens words into `watchlists/watch.txt`, one word per line.
- Run `clean watch` to clean domain names, creates `watchlists/watch_clean.txt`.
- Run `node ethereum/normalize.js >> watchlists/watch_clean.csv`.
- Run `build_watchlist` to get human readable metadata about domains in `ethereum/watch_clean.json`.

### To upgrade DB
- Modify any table in `backend/models/models.py` file.
- Run `alembic revision --autogenerate -m "describe model changes"`.
- Inspect newly created `alembic/versions/*.py` file to ensure changes have been captured accurately.
- Run `alembic upgrade head` to update db to latest version.

# Trouble shooting
#### Database/alembic
- If alembic revisions are failing with `FAILED: Target database is not up to date.`, run `alembic stamp head`, then continue with upgrading head. [stackoverflow](https://stackoverflow.com/questions/17768940/target-database-is-not-up-to-date)
- If previous versions of the database are needed, read this thread, [stackoverflow](https://stackoverflow.com/questions/48242324/undo-last-alembic-migration)

#### Dependency Requirement Issues
- Run `pip install --use-feature=2020-resolver py-evm`.
- Run `pip install -r requirements.txt`.


# NOTES BELOW

### To use scripts
- Run `python install -e .`.

### To auto installed
- Run `npm run setup`.

### Testing
- Run `clean test` to clean `ethereum/test.txt`.

### MYSQL
/usr/local/opt/mysql/bin/mysqld_safe --datadir=/usr/local/var/mysql
brew services restart mysql
mysql -uroot
mysql.server stop
mysql.server start
mysql -u root -h localhost -p
mysql -h sqlite:////Users/ancientevil/0x/hawk/ENS.db -u root

mysql -h localhost -u root -p hawk


#
EXTRA_OPTIONS = --http.api eth,engine,net,web3,txpool