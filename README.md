# hawk
domain watcher

#### TODO UPDATE Instructions
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

## Getting started
- Copy/Paste domain names into `watchlists/watch.txt`, one name per line.
- Run `clean_file watch` to clean domain names; creates `watchlists/watch_clean.txt`.
- Run `node ethereum/normalize.js >> watchlists/watch_clean.csv`; creates `watchlists/watch_clean.csv`.
- Run `build_watchlist` to grab metadata of domain names by querying the Ethereum network; creates `watchlists/watch_clean.json`.
- Run `create_database` to create `hawk` mysql database.
- Run `python app.py` to create database tables. `TODO` Make this a script function + combine with create_database.
- Run `populate_domains` to populate database with `watchlists/watch_clean.json` data.
- Run `populate_markets` to populate database with `backend/utils/markets.json` data.

## Upgrade MySQL Database
- Modify any table in `backend/models/*.py` file.
- Run `alembic revision --autogenerate -m "describe model change(s)"`.
- Inspect newly created `alembic/versions/*.py` file to ensure changes have been captured accurately.
- Run `alembic upgrade head` to update db to latest version.

# Trouble shooting
#### Database/alembic
- If alembic revisions are failing with `FAILED: Target database is not up to date.`, run `alembic stamp head`, then continue with upgrading head. [stackoverflow](https://stackoverflow.com/questions/17768940/target-database-is-not-up-to-date)
- If previous versions of the database are needed, read this thread, [stackoverflow](https://stackoverflow.com/questions/48242324/undo-last-alembic-migration)

#### Dependency Requirement Issues
- Run `pip install --use-feature=2020-resolver py-evm`.
- Run `pip install -r requirements.txt`.



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


#### TODO Front end - legacy - 
- Run `npx create-react-app frontend`
- Add `"proxy": "http://localhost:5000",` to `frontend/package.json`.
- Run `npm run build`.

##### TODO Frontend
- Run ``