from collections import Counter
from itertools import cycle
import os
import numpy as np

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "text.txt")

def kasiski_examination(ciphertext):
    """Метод Касіскі для визначення довжини ключа"""
    min_length = 3
    distances = []
    
    for length in range(min_length, 6):  # Шукаємо повтори довжиною 3-5 символів
        substrings = {}
        
        for i in range(len(ciphertext) - length):
            substring = ciphertext[i:i+length]
            if substring in substrings:
                distances.append(i - substrings[substring])
            substrings[substring] = i
    
    if distances:
        key_length = np.gcd.reduce(distances)  # Знаходимо НСД відстаней
        return key_length if key_length > 1 else None
    return None

def friedman_test(ciphertext):
    """Тест Фрідмана для оцінки довжини ключа"""
    n = len(ciphertext)
    freq = Counter(ciphertext)
    ic = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
    
    if ic > 0.038:
        expected_key_length = round(1.73 / (ic - 0.038))
        return expected_key_length if expected_key_length > 1 else None
    return None

def split_by_key_length(ciphertext, key_length):
    """Розбиває шифртекст на групи за довжиною ключа"""
    return [ciphertext[i::key_length] for i in range(key_length)]

def frequency_analysis(group):
    """Проводить частотний аналіз та припускає, що найчастотніша літера - 'E'"""
    group = [char for char in group if char in ALPHABET]  # Фільтруємо лише літери
    if not group:
        return 'A'  # Якщо немає літер, повертаємо 'A' (нейтральний варіант)

    freq = Counter(group)
    most_common_letter, _ = freq.most_common(1)[0]
    
    if most_common_letter not in ALPHABET:
        return 'A'  # Якщо символ не знайдено, повертаємо 'A'

    shift = (ALPHABET.index(most_common_letter) - ALPHABET.index('E')) % 26
    return ALPHABET[shift]

def recover_vigenere_key(ciphertext, key_length):
    """Відновлює ключ за частотним аналізом кожної групи"""
    groups = split_by_key_length(ciphertext, key_length)
    key = ''.join(frequency_analysis(group) for group in groups)
    return key

def vigenere_encrypt(text, key):
    text = text.upper()
    key = cycle(key.upper())
    encrypted_text = ''
    
    for char in text:
        if char in ALPHABET:
            shift = ALPHABET.index(next(key))
            encrypted_text += ALPHABET[(ALPHABET.index(char) + shift) % 26]
        else:
            encrypted_text += char
    
    return encrypted_text

def vigenere_decrypt(ciphertext, key):
    """Дешифрування тексту шифром Віженера"""
    key = cycle(key.upper())
    decrypted_text = ''
    
    for char in ciphertext:
        if char in ALPHABET:
            shift = ALPHABET.index(next(key))
            decrypted_text += ALPHABET[(ALPHABET.index(char) - shift) % 26]
        else:
            decrypted_text += char
    
    return decrypted_text

if __name__ == '__main__':
    # Приклад використання
    key = "CRYPTOGRAPHY"

    with open(file_path, 'r', encoding='utf-8') as f:
        plaintext = f.read().strip()

    ciphertext = vigenere_encrypt(plaintext, key)
    key_len = kasiski_examination(ciphertext)

    if key_len is None:
        key_len = friedman_test(ciphertext)

    if key_len:
        print(f"Ймовірна довжина ключа: {key_len}")
        key = recover_vigenere_key(ciphertext, key_len)
        print(f"Відновлений ключ: {key}")
        decrypted_text = vigenere_decrypt(ciphertext, key)
        print(f"Розшифрований текст: {decrypted_text}")
    else:
        print("Не вдалося визначити довжину ключа")

    # decrypted = vigenere_decrypt(ciphertext, key)

    # detected_length_kasiski = kasiski_examination(ciphertext)
    # detected_length_friedman = friedman_test(ciphertext)

    # print("Encrypted:", ciphertext)
    # print("Decrypted:", decrypted)
    # print("Key length (Kasiski):", detected_length_kasiski)
    # print("Key length (Friedman):", detected_length_friedman)