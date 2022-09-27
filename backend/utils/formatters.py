import json


def stringify(attribute: object) -> str:
	'''
	Serializes attribute object into JSON formatted string.
	'''
	try:
		if isinstance(attribute, dict):
			value = json.dumps(attribute)
		elif isinstance(attribute, str):
			value = json.dumps(attribute)
			value = value.replace('"', "")
		return value
	except:
		return attribute

