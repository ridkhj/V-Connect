import json

def object_to_json(objects ):
    try:
        object_dict = [object.to_dict() for object in objects ]
        json_data = json.dumps(object_dict, indent=4)
        return json_data    
    
    except Exception as e:
        return {"error": str(e)}
