import base64
import json

def encode_base64(string):
    return base64.b64encode(string.encode("utf-8")).decode("utf-8")
