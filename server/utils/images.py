import requests


def get_image(path):
    for extension in [".png", ".svg", ".jpg", ".jpeg"]:
        if requests.get(path + extension).status_code == 200:
            return path + extension
    return
