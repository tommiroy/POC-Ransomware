from cryptography.fernet import Fernet


def encrypt_file (path):
    key = Fernet.generate_key()
    f = Fernet(key)
    with open(path, 'rb') as file:
        unencrypted_data = file.read()
    encrypted_data = f.encrypt(unencrypted_data)
    with open(path +'.encrypted', 'wb') as file:
        file.write(encrypted_data)
    return key

def decrypt_file (path, key):
    with open(path, 'rb') as file:
        encrypted_data = file.read()
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    with open(path.rsplit('.', 1)[0] + '.decrypted', 'wb') as file:
        file.write(decrypted_data)

path = 'target/test.txt'

key = encrypt_file(path)
print(f'Key: {key}')

decrypt_file(path + '.encrypted', key)