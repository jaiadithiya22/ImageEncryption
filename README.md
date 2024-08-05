**Image Encryption Project**

Overview
This project provides a way to encrypt and decrypt images using block-wise operations and a simple XOR encryption scheme. The image is divided into smaller blocks, which are then shuffled, encrypted with a key, and reconstructed into an encrypted image. The decryption process involves reversing these steps using the saved key and block order.

Features
Converts the image to grayscale for processing.
Divides the image into blocks of a specified size.
Shuffles the blocks and encrypts them using a generated key.
Saves the encrypted image, the key, and the block order for later decryption.
Decrypts the encrypted image using the saved key and block order.
Requirements
Python 3.x
Pillow library
NumPy library
You can install the required libraries using pip:

bash
Copy code
pip install pillow numpy
Usage
Encrypting an Image
Run the script.
Choose the encrypt option by typing e.
Enter the full path to the image file you want to encrypt.
The script will:
Load the image.
Divide it into blocks.
Shuffle and encrypt the blocks.
Save the encrypted image.
Save the encryption key and block order for decryption.
The encrypted image, key, and block order will be saved in the Downloads directory.

Decrypting an Image
Run the script.
Choose the decrypt option by typing d.
Enter the full path to the encrypted image file.
Enter the full path to the encryption key file.
Enter the full path to the block order file.
The script will:
Load the encrypted image.
Divide it into blocks.
Decrypt the blocks using the key.
Unshuffle the blocks using the block order.
Reconstruct and save the decrypted image.
The decrypted image will be saved in the Downloads directory.

Example
Here is a step-by-step example:

Encrypting
bash
Copy code
python image_encryption.py
Enter e when prompted.
Enter the path to your image file, e.g., C:\images\myimage.jpg.
The encrypted image, key, and block order will be saved in the Downloads directory.

Decrypting
bash
Copy code
python image_encryption.py
Enter d when prompted.
Enter the path to the encrypted image file, e.g., C:\Users\YourUsername\Downloads\encrypted_image.jpg.
Enter the path to the key file, e.g., C:\Users\YourUsername\Downloads\encryption_key.npy.
Enter the path to the block order file, e.g., C:\Users\YourUsername\Downloads\block_order.json.
The decrypted image will be saved in the Downloads directory.

Project Files
image_encryption.py: The main script for encryption and decryption.
README.md: This readme file.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
Pillow library for image processing.
NumPy library for numerical operations.
Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

Contact
For any questions or issues, please contact Jai Adithiya at jaiadithiya11@gmail.com

