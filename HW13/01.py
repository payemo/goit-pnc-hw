import string
from collections import Counter

original_text = (
    "The quick brown fox jumps over the lazy dog. This sentence contains every letter of the English alphabet."
)

# Перший крок: Шифрування Цезаря зі зсувом 3
def caesar_cipher(text, shift):
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)

ciphered_text = caesar_cipher(original_text, 3)
print("\n[Зашифрований текст]:\n", ciphered_text)

# Другий крок: Частотний аналіз

def frequency_analysis(text):
    letters_only = [char.lower() for char in text if char.isalpha()]
    return Counter(letters_only)

cipher_freq = frequency_analysis(ciphered_text)
print("\n[Частотний аналіз зашифрованого тексту]:")
for letter, freq in cipher_freq.most_common():
    print(f"{letter}: {freq}")

# Третій крок: Визначення зсуву за допомогою частотного аналізу

def find_caesar_shift(cipher_freq):
    most_common_letter = cipher_freq.most_common(1)[0][0]
    assumed_plaintext_letter = 'e'  # Найпоширеніша літера англійської мови
    shift = (ord(most_common_letter) - ord(assumed_plaintext_letter)) % 26
    return shift

estimated_shift = find_caesar_shift(cipher_freq)
print(f"\n[Оцінений зсув]: {estimated_shift}")

# Дешифруємо текст, знаючи зсув

def caesar_decipher(text, shift):
    return caesar_cipher(text, -shift)

recovered_text = caesar_decipher(ciphered_text, estimated_shift)
print("\n[Відновлений текст]:\n", recovered_text)

# Для перевірки: чи відповідає оригінальному
print("\n[Перевірка]: Текст відновлений правильно?", recovered_text.lower() == original_text.lower())