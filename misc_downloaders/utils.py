import requests


def download_image(url, image):
    with open(image, "wb") as file:
        response = requests.get(url)

        if response.status_code is requests.codes.ok:
            file.write(response.content)
