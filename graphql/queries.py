# import pdb; pdb.set_trace()
# TODO - unittests which validate json


'''
  Returns all domains in auction.

  Params:
  - GREATER_THAN: 120 days ago from now(), in unix timestamp.
  - LESS_THAN: 90 days ago from now(), in unix timestamp.
  - SKIP: Used to paginate results.
  - FIRST: Max results per response.
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
  Returns the current owner of a domain.

  Params:
  - _NAME: labelName of a domain, without .eth part.
'''
DOMAIN_OWNER = '''
{
  registrations(
    where:{
      labelName:"_NAME",
      registrationDate_gte:1580409416
    },
    first:1,
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
}
'''


'''
  Looks up owners of a group of domains. Query is batched into
  groups of 300, then those batches are added to a list of
  batches, until there are no more domains to include.

  See ethereum/read_ens.py::ens_claw for implementation. 

  Params:
  - _NAME: labelName of a domain, without .eth part.
'''
DOMAIN_OWNER_BATCH = '''
  _HASH: registrations(
    where:{
      labelName:"_NAME",
      registrationDate_gte:1580409416
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


# DOMAIN = """
# {
#   domains(where:{labelName:"_NAME"},first:1,block:{number_gte:9380410})
#   {
#     createdAt
#     labelhash
#     owner {
#       id
#     }
#     events {
#       blockNumber
#       transactionID
#       __typename
#     }
#     resolver {
#       id
#       address
#       contentHash
#       addr{
#         id
#       }
#     }
#     resolvedAddress{
#       id
#     }
#   }
# }
# """

REGISTRATIONS = '''
{
  registrations(where:{labelName:"_NAME", registrationDate_gte: 1580409416}, block: {number_gte: 9380410}, orderBy: registrationDate)
  {
    expiryDate
    registrationDate
    cost
    registrant{
      id
    }
    events(orderBy:blockNumber){
      transactionID
      __typename
    }
  }
}
'''