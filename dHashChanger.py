
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


def hamming_distance(hash1, hash2):
    bin1 = bin(int(hash1, 16))[2:].zfill(64)
    bin2 = bin(int(hash2, 16))[2:].zfill(64)
    return sum(c1 != c2 for c1, c2 in zip(bin1, bin2))


def break_perceptual_hash(input_path, output_path, brightness_factor=0.72, gradiente_factor=100):
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

    
    # 1. Micro líneas cada 30 píxeles (diagonales suaves)
    for i in range(0, min(width, height), 30):
        if 0 <= i < width and 0 <= i < height:
            pixels[i, i] = tuple(min(v ^ 1, 255) for v in pixels[i, i])
        if 0 <= width - i - 1 < width and 0 <= i < height:
            pixels[width - i - 1, i] = tuple(min(v ^ 1, 255) for v in pixels[width - i - 1, i])

    # 2. Cambios en píxeles oscuros
    for x in range(0, width, 40):
        for y in range(0, height, 40):
            r, g, b = pixels[x, y]
            if r < 50 and g < 50 and b < 50:
                pixels[x, y] = (r + 10, g + 10, b + 10)

    # 3. Overlay de textura leve (patrón tipo red)
    for y in range(0, height, 8):
        for x in range(0, width, 8):
            if (x + y) % 16 == 0:
                r, g, b = pixels[x, y]
                pixels[x, y] = (min(r + 2, 255), min(g + 2, 255), min(b + 2, 255))

    image = ImageEnhance.Brightness(image).enhance(brightness_factor)
    image.save(output_path)

    new_phash, new_sha = calculate_hashes(output_path)
    dist = hamming_distance(original_phash, new_phash)

    print(f"Image: {os.path.basename(input_path)}")
    print("Original perceptual hash:", original_phash)
    print("New perceptual hash:     ", new_phash)
    print("Hamming distance:        ", dist)
    if dist < 4:
        print("[!] Warning: Very small distance detected.")
        print("[!] Recommended to apply more aggressive modifications or use stealth/aggressive mode.")
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
