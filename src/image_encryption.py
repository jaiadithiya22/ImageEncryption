from PIL import Image
import numpy as np
import random
import os
import json

def load_image(image_path):
    image = Image.open(image_path)
    image = image.convert('L')  # Convert to grayscale
    image_data = np.array(image)
    return image_data

def save_image(image_data, path):
    image = Image.fromarray(image_data)
    image.save(path)

def divide_into_blocks(image_data, block_size=8):
    height, width = image_data.shape
    blocks = []
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            block = image_data[i:i+block_size, j:j+block_size]
            if block.shape != (block_size, block_size):
                padded_block = np.zeros((block_size, block_size), dtype=np.uint8)
                padded_block[:block.shape[0], :block.shape[1]] = block
                block = padded_block
            blocks.append(block)
    return blocks

def shuffle_blocks(blocks):
    order = list(range(len(blocks)))
    random.shuffle(order)
    shuffled_blocks = [blocks[i] for i in order]
    return shuffled_blocks, order

def reconstruct_image(blocks, block_size, height, width):
    reconstructed_image_data = np.zeros((height, width), dtype=np.uint8)
    index = 0
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            block = blocks[index]
            block_height, block_width = block.shape
            reconstructed_image_data[i:i+block_height, j:j+block_width] = block[:min(block_size, height-i), :min(block_size, width-j)]
            index += 1
    return reconstructed_image_data

def generate_key(block_size=8):
    key = np.random.randint(0, 256, (block_size, block_size), dtype=np.uint8)
    return key

def encrypt_blocks(blocks, key):
    encrypted_blocks = [np.bitwise_xor(block, key) for block in blocks]
    return encrypted_blocks

def decrypt_blocks(blocks, key):
    decrypted_blocks = [np.bitwise_xor(block, key) for block in blocks]
    return decrypted_blocks

def unshuffle_blocks(blocks, order):
    unshuffled_blocks = [None] * len(blocks)
    for original_index, shuffled_index in enumerate(order):
        unshuffled_blocks[shuffled_index] = blocks[original_index]
    return unshuffled_blocks

if __name__ == "__main__":
    action = input("Do you want to (e)ncrypt or (d)ecrypt an image? ")

    if action.lower() not in ['e', 'd']:
        print("Invalid option. Please choose 'e' for encrypt or 'd' for decrypt.")
        exit()

    image_path = input("Enter the full path to the image file (in quotes if it contains spaces): ").strip('"')

    if not os.path.exists(image_path):
        print(f"The file {image_path} does not exist.")
        exit()

    # Load image
    image_data = load_image(image_path)
    print(f"Image loaded with shape: {image_data.shape}")

    # Define block size and output directory
    block_size = 8  # You can change the block size if needed
    output_dir = os.path.join(os.path.expanduser('~'), 'Downloads')

    if action.lower() == 'e':
        # Encrypting
        # Divide the image into blocks
        blocks = divide_into_blocks(image_data, block_size)
        print(f"Divided image into {len(blocks)} blocks of size {block_size}x{block_size}")

        # Shuffle the blocks and save the order
        shuffled_blocks, order = shuffle_blocks(blocks)
        print("Blocks shuffled")

        # Generate encryption key
        key = generate_key(block_size)
        print(f"Generated encryption key:\n{key}")

        # Encrypt the blocks
        encrypted_blocks = encrypt_blocks(shuffled_blocks, key)
        print("Blocks encrypted")

        # Reconstruct the encrypted image
        height, width = image_data.shape
        encrypted_image_data = reconstruct_image(encrypted_blocks, block_size, height, width)
        encrypted_image_path = os.path.join(output_dir, 'encrypted_image.jpg')
        save_image(encrypted_image_data, encrypted_image_path)
        print(f"Encrypted image saved as {encrypted_image_path}")

        # Save the key and order for decryption
        key_path = os.path.join(output_dir, 'encryption_key.npy')
        np.save(key_path, key)
        print(f"Encryption key saved as {key_path}")

        order_path = os.path.join(output_dir, 'block_order.json')
        with open(order_path, 'w') as f:
            json.dump(order, f)
        print(f"Block order saved as {order_path}")

    elif action.lower() == 'd':
        # Decrypting
        key_path = input("Enter the full path to the encryption key file (in quotes if it contains spaces): ").strip('"')

        if not os.path.exists(key_path):
            print(f"The file {key_path} does not exist.")
            exit()

        order_path = input("Enter the full path to the block order file (in quotes if it contains spaces): ").strip('"')

        if not os.path.exists(order_path):
            print(f"The file {order_path} does not exist.")
            exit()

        # Load the encryption key and order
        key = np.load(key_path)
        print(f"Loaded encryption key:\n{key}")

        with open(order_path, 'r') as f:
            order = json.load(f)
        print(f"Loaded block order:\n{order}")

        # Divide the encrypted image into blocks
        encrypted_blocks = divide_into_blocks(image_data, block_size)
        print(f"Divided encrypted image into {len(encrypted_blocks)} blocks of size {block_size}x{block_size}")

        # Decrypt the blocks
        decrypted_blocks = decrypt_blocks(encrypted_blocks, key)
        print("Blocks decrypted")

        # Unshuffle the blocks
        unshuffled_blocks = unshuffle_blocks(decrypted_blocks, order)
        print("Blocks unshuffled")

        # Reconstruct the decrypted image
        height, width = image_data.shape
        decrypted_image_data = reconstruct_image(unshuffled_blocks, block_size, height, width)
        decrypted_image_path = os.path.join(output_dir, 'decrypted_image.jpg')
        save_image(decrypted_image_data, decrypted_image_path)
        print(f"Decrypted image saved as {decrypted_image_path}")
