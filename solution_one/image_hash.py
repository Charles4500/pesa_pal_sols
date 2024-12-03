import sys
import hashlib
from PIL import Image
from PIL.PngImagePlugin import PngInfo


def calculate_hash(file_path, hash_algorithm="sha512"):
    """Calculate the hash of a file."""
    hash_func = hashlib.new(hash_algorithm)
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def add_metadata(image_path, output_path, metadata):
    """Add metadata to an image."""
    image = Image.open(image_path).convert("RGB")  # Ensure compatibility

    # Convert to PNG if not already
    if not output_path.lower().endswith(".png"):
        output_path = output_path.rsplit(".", 1)[0] + ".png"

    # Add metadata
    meta = PngInfo()
    for key, value in metadata.items():
        meta.add_text(key, value)

    # Save the image as PNG with new metadata
    image.save(output_path, "PNG", pnginfo=meta)
    return output_path


def modify_image_to_match_hash(target_prefix, original_path, altered_path, hash_algorithm="sha512"):
    """Modify the metadata of an image to produce a desired hash prefix."""
    metadata_index = 0

    # Convert altered_path to PNG format if necessary
    if not altered_path.lower().endswith(".png"):
        altered_path = altered_path.rsplit(".", 1)[0] + ".png"

    while True:
        # Add incremental metadata
        metadata = {"comment": f"hash-adjust-{metadata_index}"}
        modified_path = add_metadata(original_path, altered_path, metadata)

        # Calculate the hash of the altered file
        current_hash = calculate_hash(modified_path, hash_algorithm)

        # Check if the hash matches the desired prefix
        if current_hash.startswith(target_prefix.lstrip("0x")):
            print(f"Match found! Hash: {current_hash}")
            break

        
        metadata_index += 1


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python spoof.py <hexstring> <original_image> <altered_image>")
        sys.exit(1)

    target_hex = sys.argv[1]
    original_image_path = sys.argv[2]
    altered_image_path = sys.argv[3]

    print(f"Target hash prefix: {target_hex}")
    print(f"Original image: {original_image_path}")
    print(f"Altered image will be saved as: {altered_image_path}")

    modify_image_to_match_hash(target_hex, original_image_path, altered_image_path)

 