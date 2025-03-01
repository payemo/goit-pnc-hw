from vigenere import vigenere_encrypt, vigenere_decrypt
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "text.txt")

def create_table_key(key):
    return sorted(range(len(key)), key=lambda k:key[k])

def table_encrypt(text: str, key: str):
    text = text.replace(" ", "").upper()
    columns = len(key)
    rows = -(-len(text) // columns)
    matrix = [[''] * columns for _ in range(rows)]

    index = 0
    for i in range(rows):
        for j in range(columns):
            if index < len(text):
                matrix[i][j] = text[index]
                index += 1

    key_order = create_table_key(key)
    encrypted_text = ''.join(''.join(matrix[row][i] for row in range(rows) if matrix[row][i]) for i in key_order)
    return encrypted_text

def table_decrypt(text, key):
    columns = len(key)
    rows = -(-len(text) // columns)
    key_order = create_table_key(key)
    
    decrypted_matrix = [[''] * columns for _ in range(rows)]
    index = 0
    for i in key_order:
        for row in range(rows):
            if index < len(text):
                decrypted_matrix[row][i] = text[index]
                index += 1
    
    return ''.join(''.join(row) for row in decrypted_matrix).strip()

def double_encrypt(text, vigenere_key, table_key):
    first_pass = vigenere_encrypt(text, vigenere_key)
    return table_encrypt(first_pass, table_key)

def double_decrypt(text, vigenere_key, table_key):
    first_pass = table_decrypt(text, table_key)
    return vigenere_decrypt(first_pass, vigenere_key)

if __name__ == '__main__':
    # Приклад використання
    key1 = "MATRIX"
    key2 = "CRYPTO"
    vigenere_key = "VIGENERE"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        plaintext = f.read().strip()

    ciphertext1 = table_encrypt(plaintext, key1)
    decrypted1 = table_decrypt(ciphertext1, key1)

    ciphertext2 = double_encrypt(plaintext, vigenere_key, key2)
    decrypted2 = double_decrypt(ciphertext2, vigenere_key, key2)

    print("Table Cipher Encrypted:", ciphertext1)
    print("Table Cipher Decrypted:", decrypted1)
    print("Double Encryption Encrypted:", ciphertext2)
    print("Double Encryption Decrypted:", decrypted2)