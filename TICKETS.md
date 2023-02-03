# HAWK

#### Will do
- backend : api limit
- backend : add a highest bid ever stats on each domain, in weth
- backend : display any current bids on doamins
- backend : search for domains in db with either starts_with or ends_with
- backend : automatic backup web3 provider if local node is offline

- eth : explore SIWE
- eth : explore hosting this app on eth.limo
- eth : explore how to reg domains with metamask

- frontend: Home should include stats of total domains tracked, how many in each state (grace,expired,auction,free).
- frontend: pagination

- backend/frontend: import all ens domains from a wallet, or group of wallets.

- investigate whether its faster to get domain metadata from smart contracts or graphql. what conditions must be true to change our primary data source from ens smart contracts to thegraph ens subgraph protocol?


#### Doing
- backend : add domain history, such as mint value, transfers, sells.
  - endpt accepts a string, a domain name.
  - build with graphql first approach
  - user clicks on a domain, all domain info should be dynaimcally loaded from thegraph.
  - frontend takes user input (click on domain name), backend receives domain name and makes call to thegraph. backend respondes with domain history details & relevant metadata.
- frontend : work on individual domain layout
  - https://ens.vision/name/lobo

- front/backends : SIWE
  - Frontend: user can sign a eip-4361 message (https://eips.ethereum.org/EIPS/eip-4361).
  - Frontend: button which triggers SIWE action.
  - Frontend: api call to get nonce from backend.
  - Frontend: signing address much conform to eip-55 (https://eips.ethereum.org/EIPS/eip-55).
  - Frontend: code to connect a wallet, which returns a provider.
  - Frontend: code which creates a `SiweMessage` object, and returns that object.
  - Frontend: code which can sign & verify eip-4361 messages. this endpt will call backend with serialized message + resulting signature data.
  - Backend: GET `nonce` endpt which is called to get a random nonce.
  - Backend: POST `siwe` endpt which takes a serialized string `SiweMessage` object, & signature data. endpt verifies whether the signature/serialized `SiweMessage` is valid.
 
  - TODO Backend: sessions endpoint. brings together nonce & siwe endpoints. figure out how to use siwe to create sessions - mysql
  - TODO Frontend: user can sign out of wallet
  - TODO Frontend: change default wallet info display locations.

#### Hold/Backlog
- frontend: toggle between Deck/Cards and Table
- frontend: bulkSearch file upload. check for file size and type.
  - Check file size on frontend
  - check file type on frontend
  - ISSUE: API recieving file contents, api is returning resp obj, but front end resp object missing resp from api.... weird bug (BUG HAS A SOLUTION. WILL GET TO WHEN SIWE DONE)


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
- backend: update all domains in database. - solved with script `refresh_domains`.
- both: resolve addresses to their ENS domains
- backend : fix backend logger, make info actually useful
- backend : Use ENS name on owners if domain is set for an address
- both : ability to add domains to watch from frontend. in a file, or single lined entry.
- both : bulk search text input and post bulk search display
  - reverse records for addresses
  - mini view 
  - heart button toggled
- backend: bulkSearch file upload endpoint
  - handles text file, single word per line.
  - verifies only text file is being sent
  - ensure that non-ascii is being read correctly
- backend : batch graphql calls
  - max total without subgraph fail is ~300
  - only makes sense to batch calls in `ens_claw` and not in `ens_claw_update_domains`. in  `ens_claw_update_domains` domains are grabed from db, then code goes through each domain 1 by 1, updates the data, and saves the updated domain. There is no persistance of each domain. In `ens_claw` we have all domain data and know which domains failed `ownerOf`. we can batch the calls of only the domains that failed.
