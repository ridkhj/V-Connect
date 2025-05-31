from re import purge
from turtle import up, update
from cerberus import Validator

update_schema = {
    'code': {'type': 'string', 'required': True},
    'name': {'type': 'string', 'required': True},
    'status': {'type': 'string', 'required': True},
}

def validate_update(data):
    validator = Validator(update_schema, purge_unknown=True)
    if isinstance(data, list):
        for item in data:
            if not isinstance(item, dict):
                return False
            if not validator.validate(item):
                raise ValueError(f"Validation Error: {Validator.errors}")
        return True
    elif isinstance(data, dict): 
        return validator.validate(data)
    else:
        return False        