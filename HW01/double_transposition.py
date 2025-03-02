import numpy as np
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "text.txt")

def create_permutation_key(key: str):
    return sorted(range(len(key)), key=lambda k: key[k])

def simple_transposition_encrypt(text: str, key: str):
    columns = len(key)
    text = text.replace(" ", "")
    rows = -(-len(text) // columns)
    matrix = [[''] * columns for _ in range(rows)]

    for i, char in enumerate(text):
        matrix[i // columns][i % columns] = char

    key_order = create_permutation_key(key)
    enc_text = ''.join(''.join(row[i] for row in matrix if row[i]) for i in key_order)
    return enc_text


def simple_transposition_decrypt(text, key):
    """Коригований алгоритм дешифрування для перестановочного шифру."""
    columns = len(key)
    rows = -(-len(text) // columns)
    key_order = create_permutation_key(key)
    
    # Визначаємо довжини стовпців
    num_full_columns = len(text) % columns
    col_lengths = [rows] * num_full_columns + [rows - 1] * (columns - num_full_columns)
    
    # Заповнюємо матрицю для дешифрування
    decrypted_matrix = [[''] * columns for _ in range(rows)]
    index = 0
    for col_idx in key_order:
        col_length = col_lengths[col_idx]
        for row in range(col_length):
            if index < len(text):
                decrypted_matrix[row][col_idx] = text[index]
                index += 1
    
    decrypted_text = ''.join(''.join(row) for row in decrypted_matrix).strip()
    return decrypted_text

def double_transposition_encrypt(text, key1, key2):
    first_pass = simple_transposition_encrypt(text, key1)
    return simple_transposition_encrypt(first_pass, key2)

def double_transposition_decrypt(text, key1, key2):
    first_pass = simple_transposition_decrypt(text, key2)
    return simple_transposition_decrypt(first_pass, key1)

# Приклад використання
key1 = "SECRET"
key2 = "CRYPTO"

with open(file_path, 'r', encoding='utf-8') as f:
    plaintext = f.read().strip()

ciphertext = double_transposition_encrypt(plaintext, key1, key2)
decrypted = double_transposition_decrypt(ciphertext, key1, key2)

print("Encrypted:", ciphertext)
print("Decrypted:", decrypted)