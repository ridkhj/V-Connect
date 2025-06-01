import json

def object_to_json(objects):
    try:
        return [object.to_dict() for object in objects]
    except Exception as e:
        return {"error": str(e)}
