
# dHashBreaker - Anti Perceptual Hash Image Modifier

A Python tool to modify images in order to break perceptual hashes (dHash) while preserving visual quality as much as possible.

The script applies controlled image modifications such as:
- High-contrast diagonal lines.
- Smooth brightness gradient.
- Global brightness adjustment.

This can be used for testing the robustness of perceptual hash algorithms, digital forensics research, or educational purposes.

---

## Features

- Batch processing: Modifies all images from a selected folder.
- Prints original and new perceptual hashes (dHash).
- Prints original and new SHA256 hashes.
- Preserves maximum visual similarity when possible.
- Compatible with `.jpg`, `.jpeg`, `.png` formats.

---

## Requirements

- Python 3.x

Install required libraries:

```bash
pip install pillow opencv-python
```

---

## Usage

1. Place your original images inside the `input/` folder.

2. Run the script:

```bash
python dHashChanger.py
```

3. The modified images will be saved in the `output/` folder with the same filename.

---

## Output Example

Example console output for a processed image:

```
Image: photo.jpg
Original perceptual hash: 30cd32b0000
New perceptual hash:      ffff8cd32b3fff
Original SHA256 hash:     95b4303b31...
New SHA256 hash:          e6d096b803...
--------------------------------------------------
```

---

## Project Structure

```
/
├── dHashChanger.py    # Main script
├── input/             # Folder for original images
└── output/            # Folder for modified images
```

---

## Optional: Build a Windows Executable

If you want to create a portable `.exe` file:

Install PyInstaller:

```bash
pip install pyinstaller
```

Build the executable:

```bash
pyinstaller --onefile dHashChanger.py
```

The generated `.exe` file will be in the `dist/` folder.

---

## Disclaimer

This tool is intended for educational and research purposes only.

Do not use it for illegal activities.

---

## License

MIT License.
