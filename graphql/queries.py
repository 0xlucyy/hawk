# import pdb; pdb.set_trace()


# TODO - unittests which validate json

DOMAIN = """
{
  domains(where:{labelName:"_NAME"},first:1,block:{number_gte:9380410})
  {
    createdAt
    owner {
      id
    }
    events {
      blockNumber
      transactionID
      __typename
    }
    resolver {
      id
      address
      contentHash
      addr{
        id
      }
    }
    resolvedAddress{
      id
    }
  }
}
"""

DOMAIN_ECO = """
{
  domains(where:{labelName:"_NAME"},first:1,block:{number_gte:9380410})
  {
    labelhash
    events(orderBy: blockNumber) {
      transactionID
      __typename
    }
  }
}
"""

DOMAIN_RESOLVER = '''
{
  domains(where:{labelName:"_NAME"},first:1,block:{number_gte:9380410})
  {
    resolver {
      id
      address
      contentHash
      addr{
        id
      }
    }
    resolvedAddress{
      id
    }
  }
}
'''

DOMAIN_EVENTS = '''
{
  domains(where:{labelName:"_NAME"},first:1,block:{number_gte:9380410})
  {
    events {
      transactionID
      __typename
    }
  }
}
'''

DOMAIN_OWNER = '''
{
  registrations(where:{labelName:"_NAME", registrationDate_gte: 1580409416}, block: {number_gte: 9380410}, orderBy: registrationDate)
  {
    registrant{
      id
    }
  }
}
'''
# {'data': {'domains': [{'owner': {'id': '0x30321484937c8a5595a05fae7a698e2a2fc3e510'}}]}}

DOMAIN_OWNER_BATCH = '''
registrations(where:{labelName:"_NAME", registrationDate_gte: 1580409416}, block: {number_gte: 9380410}, orderBy: registrationDate)
{
  registrant{
    id
  }
}
'''

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

REGISTRATION_EVENTS = '''
  registrations(where:{labelName:"_NAME", registrationDate_gte: 1580409416}, block: {number_gte: 9380410}, orderBy: registrationDate)
  {
    events(orderBy: blockNumber) {
      blockNumber
      transactionID
      __typename
    }
  }
'''

REGISTRATION_META = '''
  registrations(where: {labelName:"_NAME", registrationDate_gte: 1580409416}, block: {number_gte: 9380410}, orderBy: registrationDate)
  {
    expiryDate
    registrationDate
    cost
    registrant {
      id
    }
  }
'''