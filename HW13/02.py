import string
from collections import Counter
import re

# Оригінальний текст для шифру Віженера
original_text = (
    "Cryptography is the practice and study of techniques for secure communication in the presence of adversarial behavior."
)

# Шифрування Віженера з ключем 'KEY'
def vigenere_cipher(text, key):
    result = []
    key = key.lower()
    key_length = len(key)
    key_indices = [ord(k) - ord('a') for k in key]
    key_pos = 0

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = key_indices[key_pos % key_length]
            result.append(chr((ord(char) - base + shift) % 26 + base))
            key_pos += 1
        else:
            result.append(char)
    return ''.join(result)

ciphered_text = vigenere_cipher(original_text, "KEY")
print("\n[Зашифрований текст]:\n", ciphered_text)

# Частотний аналіз шифротексту
def frequency_analysis(text):
    letters_only = [char.lower() for char in text if char.isalpha()]
    return Counter(letters_only)

cipher_freq = frequency_analysis(ciphered_text)
print("\n[Частотний аналіз шифротексту]:")
for letter, freq in cipher_freq.most_common():
    print(f"{letter}: {freq}")

# Пошук повторюваних підрядків (Метод Касіскі)
def find_repeated_sequences_spacings(text):
    sequence_spacings = {}
    for seq_len in range(3, 6):  # Довжина послідовності 3..5
        sequences = {}
        for i in range(len(text) - seq_len):
            seq = text[i:i + seq_len]
            if seq in sequences:
                prev_index = sequences[seq]
                spacing = i - prev_index
                sequence_spacings.setdefault(seq, []).append(spacing)
            sequences[seq] = i
    return sequence_spacings

repeats = find_repeated_sequences_spacings(ciphered_text)
print("\n[Повторювані підрядки і відстані між ними]:")
for seq, spacings in repeats.items():
    if len(spacings) > 1:
        print(f"{seq}: {spacings}")

# Тест Фрідмана для оцінки довжини ключа
def friedman_test(text):
    letters_only = [char.lower() for char in text if char.isalpha()]
    N = len(letters_only)
    freqs = Counter(letters_only)
    numerator = sum(f * (f - 1) for f in freqs.values())
    denominator = N * (N - 1)
    IC = numerator / denominator if denominator != 0 else 0
    if IC == 0:
        return 0
    return round((0.027 * N) / ((N - 1) * IC - 0.038 * N + 0.065), 2)

estimated_key_length = friedman_test(ciphered_text)
print(f"\n[Оцінена довжина ключа за тестом Фрідмана]: {estimated_key_length}")

# Розбиття на сегменти за довжиною ключа і частотний аналіз по кожному сегменту
def split_text_into_segments(text, key_length):
    segments = ['' for _ in range(key_length)]
    index = 0
    for char in text:
        if char.isalpha():
            segments[index % key_length] += char
            index += 1
    return segments

segments = split_text_into_segments(ciphered_text, int(estimated_key_length))
print("\n[Частотний аналіз по сегментах]:")
for i, segment in enumerate(segments):
    segment_freq = frequency_analysis(segment)
    print(f"\nСегмент {i + 1}:")
    for letter, freq in segment_freq.most_common():
        print(f"{letter}: {freq}")

# Відновлення ключа за частотним аналізом сегментів
def recover_key(segments):
    key = ''
    for segment in segments:
        segment_freq = frequency_analysis(segment)
        if segment_freq:
            most_common_letter = segment_freq.most_common(1)[0][0]
            shift = (ord(most_common_letter) - ord('e')) % 26  # припускаємо, що 'e' найпоширеніша
            key += chr((26 - shift) % 26 + ord('a'))
        else:
            key += '?'
    return key

recovered_key = recover_key(segments)
print(f"\n[Відновлений ключ]: {recovered_key}")

# Розшифрування тексту за допомогою відновленого ключа
def vigenere_decipher(text, key):
    result = []
    key = key.lower()
    key_length = len(key)
    key_indices = [ord(k) - ord('a') for k in key]
    key_pos = 0

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = key_indices[key_pos % key_length]
            result.append(chr((ord(char) - base - shift) % 26 + base))
            key_pos += 1
        else:
            result.append(char)
    return ''.join(result)

recovered_text = vigenere_decipher(ciphered_text, recovered_key)
print("\n[Відновлений текст]:\n", recovered_text)

print("\n[Перевірка]: Текст відновлений правильно?", recovered_text.lower() == original_text.lower())
