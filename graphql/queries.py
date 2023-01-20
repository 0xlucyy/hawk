# import pdb; pdb.set_trace()
# TODO - unittests which validate json


'''
  Returns all domains in auction.

  Params:
  - GREATER_THAN (int): 120 days ago from now(), in unix timestamp.
  - LESS_THAN (int) : 90 days ago from now(), in unix timestamp.
  - SKIP (int): Used to paginate results.
  - FIRST (int): Max results per response.
'''
DOMAINS_IN_AUCTION = '''
{
  registrations(
    where:{
        expiryDate_gte:GREATER_THAN,
        expiryDate_lte:LESS_THAN
    },
    skip:SKIP,
    first:FIRST,
    block: {
        number_gte:9380410
    },
    orderBy:expiryDate,
    orderDirection:asc,
  )
  {
    expiryDate
    domain{
        name
    }
  }
}
'''


'''
  Returns the current owner of a .eth TLD.
  Block 16177964 contains first transaction for
  ETH Registrar Controller contract.

  Params:
  - _NAME (str): labelName of a domain, without .eth part.
'''
DOMAIN_OWNER = '''
{
  registrations(
    where:{
      labelName:"_NAME"
    },
    first:1,
    block:{
      number_gte:16177964
    }
  )
  {
    registrant{
      id
    }
  }
}
'''


'''
  Looks up owners of domains. Query is batched into
  groups of 300, then those batches are added to a list of
  batches, until there are no more domains to include.

  See ethereum/read_ens.py::ens_claw for implementation. 

  Params:
  - _HASH (str): keccak hash of domain, appended at index 0 with H.
  - _NAME (str): labelName of a domain, ie .. without .eth part.
'''
DOMAIN_OWNERS_BATCH = '''
  _HASH: registrations(
    where:{
      labelName:"_NAME"
    }, 
    block:{
      number_gte:9380410
    },
    orderBy:registrationDate
  )
  {
    registrant{
      id
    }
  }
'''


'''
  Returns all ens domains held in an address.

  Params:
  - ETH_ADDRESS (str): full ethereum address, including 0x.
'''
ALL_DOMAINS = '''
{
  registrations(
    where:{
      registrant:"ETH_ADDRESS"
    },
    block:{
      number_gte:9380410
    },
    orderBy:registrationDate,
    orderDirection:asc,
  )
  {
    labelName
  }
}
'''



'''
  Returns total onchain history of a domain.
  Returns from oldest to newest transactions (asc).

  Params:
  - _NAME (str): labelName of a domain, ie .. without .eth part.
'''
DOMAIN_EVENTS = '''
{
  registrations(
    where:{
      labelName:"_NAME"
    },
    block:{
      number_gte:9380410
    }
  )
  {
    registrant{
      id
    }
    events(
      where:{
        blockNumber_gte:9380410
      },
      orderBy:blockNumber,
      orderDirection:asc,
    )
    {
      transactionID
      __typename
    }
  }
}
'''


'''
  Returns domain owner & expiration.

  Params:
  - _NAME (str): labelName of a domain, ie .. without .eth part.
'''
DOMAIN_METADATA_BATCH = '''
  _HASH: registrations(
    where:{
      labelName:"_NAME"
    }, 
    block:{
      number_gte:9380410
    },
    orderBy:registrationDate
  )
  {
    expiryDate
    registrant{
      id
    }
  }
'''


'''
  Returns domain owner & expiration.

  Params:
  - _NAME (str): labelName of a domain, ie .. without .eth part.
'''
DOMAIN_METADATA = '''
{
  _HASH: registrations(
    where:{
      labelName:"_NAME"
    }, 
    block:{
      number_gte:9380410
    },
    orderBy:registrationDate
  )
  {
    expiryDate
    registrant{
      id
    }
  }
}
'''