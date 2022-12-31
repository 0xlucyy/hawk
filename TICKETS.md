# HAWK

#### Will do
- backend : api limit
- both : ability to add domains to watch from frontend. in a file, or single lined entry.
- backend : Use ENS name on owners if domain is set for an address
- backend : add a highest bid ever stats on each domain, in weth
- backend : add domain mint value to each domain
- backend : add domain sales history to each domain
- backend : search for domains in db with either starts_with or ends_with
- backend : fix backend logger, make info actually useful

- frontend: Home should include stats of total domains tracked, how many in each state (grace,expired,auction,free).
- frontend: pagination

- both: import all ens domains from a wallet, or group of wallets.


#### Doing
- frontend: bulkSearch page.
- backend: update all domains in database.


#### Hold/Backlog
- frontend: toggle between Deck/Cards and Table


#### Done
- backend: look into whether there is a smart contract to give us more info on domains, such as premium on purchase. - DONE
- backend : add `grace` to domains tables. expiration + 3 months. - DONE
- backend: get domain url for all markets for a single domain. - DONE
- backend : ability to refresh domain metadata - DONE
- backend: add graphql
- backend : bulk search. ID domain exists, return metadata. ElseIf domain not in db, validate domain, get metadata from eth, save into db, and return metadata.
  - This includes input validation of strings - DONE
    - https://github.com/adraffy/ensip-norm
    - https://github.com/adraffy/ens-normalize.js