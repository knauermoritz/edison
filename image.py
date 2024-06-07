import requests
from bs4 import BeautifulSoup
import random
import os
from PIL import Image
from io import BytesIO


def open_image(image_path):
    try:
        img = Image.open(image_path)
        img.show()
        print("Image opened successfully.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", e)


def get_unique_filename(directory, base_filename):
    filename, file_extension = os.path.splitext(base_filename)
    counter = 1
    unique_filename = base_filename

    while os.path.exists(os.path.join(directory, unique_filename)):
        unique_filename = f"{filename}_{counter}{file_extension}"
        counter += 1

    return unique_filename

def get_image_path(keyword, path='/Users/moritzknauer/Documents/Code/voice_assistant/images'):
    images_directory = os.path.join(path, 'images')
    if not os.path.exists(images_directory):
        os.makedirs(images_directory)

    search_url = "https://www.google.com/search?tbm=isch&q=" + keyword

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    response = requests.get(search_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    image_elements = soup.find_all("img")
    image_urls = [img["src"] for img in image_elements if "src" in img.attrs]

    if not image_urls:
        print("no images found")
        return None

    image_url = random.choice(image_urls)
    if not image_url.startswith('http'):
        image_url = 'https:' + image_url

    image_response = requests.get(image_url)
    image_response.raise_for_status()

    image = Image.open(BytesIO(image_response.content))
    image = image.convert('RGB')  # In RGB-Modus konvertieren
    base_filename = f"{keyword.replace(' ', '_')}.jpg"
    unique_filename = get_unique_filename(images_directory, base_filename)
    image_path = os.path.join(images_directory, unique_filename)
    image.save(image_path, quality=95)  # Qualität auf 95 setzen

    abs_image_path = os.path.abspath(image_path)
    print(f"image saved at {abs_image_path}")

    return abs_image_path