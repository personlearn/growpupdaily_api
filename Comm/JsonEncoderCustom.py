from datetime import datetime
import json
from bson import ObjectId

class JsonEncoderCustom(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj,datetime):
            return str(obj)
        return super(JsonEncoderCustom, self).default(obj)