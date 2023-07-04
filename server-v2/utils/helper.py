import base64

def encode_base64(string):
    return base64.b64encode(string.encode("utf-8")).decode("utf-8")