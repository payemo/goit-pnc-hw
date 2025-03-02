import numpy as np
import itertools
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "text.txt")

def create_permutation_key(key):
    return sorted(range(len(key)), key=lambda k: key[k])

# Функція шифрування методом перестановки
def transposition_encrypt(text, key):
    columns = len(key)
    text = text.replace(" ", "")  # Видаляємо пробіли для кращої обробки
    rows = -(-len(text) // columns)  # Округлення вгору
    
    # Заповнюємо матрицю символами тексту
    matrix = [[''] * columns for _ in range(rows)]
    index = 0
    for i in range(rows):
        for j in range(columns):
            if index < len(text):
                matrix[i][j] = text[index]
                index += 1
    
    key_order = create_permutation_key(key)
    encrypted_text = ''.join(''.join(matrix[row][i] for row in range(rows) if matrix[row][i]) for i in key_order)
    return encrypted_text

def transposition_decrypt(text, key):
    """Алгоритм дешифрування для перестановочного шифру."""
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

key = "SECRET"
with open(file_path, "r", encoding="utf-8") as file:
    original_text = file.read().strip()

encrypted_text = transposition_encrypt(original_text, key)
decrypted_text = transposition_decrypt(encrypted_text, key)

print("Encrypted:", encrypted_text)
print("Decrypted:", decrypted_text)