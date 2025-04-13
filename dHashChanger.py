import os
from PIL import Image, ImageEnhance
import cv2
import numpy as np
import hashlib

def calculate_hashes(image_path):
    image_cv_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image_resized = cv2.resize(image_cv_gray, (8, 8), interpolation=cv2.INTER_AREA)
    diff = image_resized[:, 1:] > image_resized[:, :-1]
    perceptual_hash = ''.join(['1' if v else '0' for v in diff.flatten()])
    perceptual_hash_hex = '{:0x}'.format(int(perceptual_hash, 2))

    with open(image_path, 'rb') as f:
        bytes_data = f.read()
        sha256_hash = hashlib.sha256(bytes_data).hexdigest()

    return perceptual_hash_hex, sha256_hash


def break_perceptual_hash(input_path, output_path, brightness_factor=0.85, gradiente_factor=50):
    original_phash, original_sha = calculate_hashes(input_path)

    image = Image.open(input_path).convert('RGB')
    pixels = image.load()
    width, height = image.size

    for i in range(0, min(width, height), 10):
        for offset in range(-1, 2):
            if 0 <= i + offset < width and 0 <= i < height:
                pixels[i + offset, i] = (255, 255, 255)
            if 0 <= i - offset < width and 0 <= i < height:
                pixels[i - offset, i] = (0, 0, 0)

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            factor = int((x + y) / (width + height) * gradiente_factor)
            pixels[x, y] = (min(r + factor, 255), min(g + factor, 255), min(b + factor, 255))

    image = ImageEnhance.Brightness(image).enhance(brightness_factor)
    image.save(output_path)

    new_phash, new_sha = calculate_hashes(output_path)

    print(f"Image: {os.path.basename(input_path)}")
    print("Original perceptual hash:", original_phash)
    print("New perceptual hash:     ", new_phash)
    print("Original SHA256 hash:    ", original_sha)
    print("New SHA256 hash:         ", new_sha)
    print("-" * 50)


input_folder = "input"
output_folder = "output"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        break_perceptual_hash(input_path, output_path)
