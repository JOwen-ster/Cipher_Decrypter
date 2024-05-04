# Import the rsa module used to load the private key file and decrypt binary files
import rsa

# Function to decrypt the ciphers
# The function takes in the private key file and the cipher file(s) as arguments
def decryptciphers(PRIVATE_KEY: str, *args: tuple[str]):
    # Open and read the private key file as bytes
    with open(PRIVATE_KEY, "rb") as pk:
        privatekeydata = rsa.PrivateKey.load_pkcs1(pk.read())

    # Loop through all cipher files and decrypt them one by one
    for index, filename in enumerate(args, 1):
        # Open and read the binary cipher file
        # Open a new file to write the decrypted text
        with open(filename, "rb") as cipherfile, open(f'os_plaintxt{index}.txt', 'w') as file:
            # Decrypt the binary cipher file using the private key
            # Decode the decrypted text to a string
            current_cipher = rsa.decrypt(
                                        crypto=cipherfile.read(),
                                        priv_key=privatekeydata
                                        ).decode()
            # Write the decrypted text to the file
            file.write(current_cipher)

# Main function to run the decrypter
if __name__ == "__main__":
    decryptciphers('prv.key', 'cipher1.bin', 'cipher2.bin')