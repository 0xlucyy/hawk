import requests
from graphql.queries import (
  DOMAIN_ECO,
  REGISTRATIONS,
  DOMAIN_OWNER,
)
from backend.utils.utils import (
  # apply_hashes_to_payload,
  # tilde_identifier,
  # remove_accents,
  # post_to_db,
  app,
  # db
)
from backend.utils.exceptions import (
  GraphQLRequestError,
  # ProviderMissing,
  # ProviderOffline,
  # DataBaseOffline,
  # DatabaseError,
  # log_error,
)
# import pdb; pdb.set_trace()


def make_graphql_request(query_target: str = None, domain_name: str = None):
  '''
    Makes a request to

    Parameters:
        query_target - either 'domain' or 'history' queries.
        domain_name - 'labelName' value of a domain.
    Returns:
        Returns 
  '''
  app.logger.info(f'Querying graphql...\n' \
                  f'Target: {query_target}\n' \
                  f'LableName: {domain_name} ...')
  try:

    if query_target == "DOMAIN_ECO":
      url = DOMAIN_ECO.replace('labelName:"_NAME"', f'labelName:"{domain_name}"')
      response = requests.post(url=app.config["GRAPHQL_ENS_URL"], json={"query": url})
    elif query_target == "REGISTRATIONS":
      url = REGISTRATIONS.replace('labelName:"_NAME"', f'labelName:"{domain_name}"')
      response = requests.post(url=app.config["GRAPHQL_ENS_URL"], json={"query": url})
    elif query_target == "DOMAIN_OWNER":
      url = DOMAIN_OWNER.replace('labelName:"_NAME"', f'labelName:"{domain_name}"')
      response = requests.post(url=app.config["GRAPHQL_ENS_URL"], json={"query": url})
    else:
      valid_values = ['DOMAIN_ECO', 'REGISTRATIONS','DOMAIN_OWNER']
      return {'msg':'invalid query_target value', 'valid_values':valid_values, 'type':'str', 'optional':False}

    app.logger.info(f'Query status code {response.status_code}...')
    return {'status_code': response.status_code, 'data': response.json()}
  except requests.exceptions.RequestException as err:
    raise GraphQLRequestError(msg="Error requesting graphql.") from err

# make_graphql_request(query_target='DOMAIN_ECO', domain_name='lobo')
# make_graphql_request(query_target='REGISTRATIONS', domain_name='lobo')
# make_graphql_request(query_target='DOMAIN_OWNER', domain_name='lobo')