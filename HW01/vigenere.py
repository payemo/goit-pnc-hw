from collections import Counter
from itertools import cycle
import os
import numpy as np

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "text.txt")

def vigenere_encrypt(text: str, key: str):
    text = text.upper()
    key = cycle(key.upper())
    enc_text = ''

    for ch in text:
        if ch in ALPHABET:
            shift = ALPHABET.index(next(key))
            enc_text += ALPHABET[(ALPHABET.index(ch) + shift) % 26]
        else:
            enc_text += ch

    return enc_text

def vigenere_decrypt(text: str, key: str):
    text = text.upper()
    key = cycle(key.upper())
    enc_text = ''

    for ch in text:
        if ch in ALPHABET:
            shift = ALPHABET.index(next(key))
            enc_text += ALPHABET[(ALPHABET.index(ch) - shift) % 26]
        else:
            enc_text += ch

    return enc_text

def kasiski_examination(ciphertext: str):
    """Виявлення довжини ключа методом Касіскі."""
    min_length = 3  # Мінімальна довжина повторюваного фрагмента
    distances = []
    
    for length in range(min_length, 6):  # Шукаємо повтори довжиною 3-5 символів
        substrings = {}
        
        for i in range(len(ciphertext) - length):
            substring = ciphertext[i:i+length]
            if substring in substrings:
                distances.append(i - substrings[substring])
            substrings[substring] = i
    
    if distances:
        key_length = np.gcd.reduce(distances)  # НСД дистанцій між повтореннями
        return key_length if key_length > 1 else None
    
    return None

def friedman_test(ciphertext: str):
    """Оцінка довжини ключа за тестом Фрідмана."""
    n = len(ciphertext)
    freq = Counter(ciphertext)
    ic = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
    expected_ic = 1.73 / (ic - 0.038) if ic > 0.038 else None
    return round(expected_ic) if expected_ic else None

if __name__ == '__main__':
    # Приклад використання
    key = "CRYPTOGRAPHY"

    with open(file_path, 'r', encoding='utf-8') as f:
        plaintext = f.read().strip()

    ciphertext = vigenere_encrypt(plaintext, key)
    decrypted = vigenere_decrypt(ciphertext, key)

    detected_length_kasiski = kasiski_examination(ciphertext)
    detected_length_friedman = friedman_test(ciphertext)

    print("Encrypted:", ciphertext)
    print("Decrypted:", decrypted)
    print("Key length (Kasiski):", detected_length_kasiski)
    print("Key length (Friedman):", detected_length_friedman)