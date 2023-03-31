import hashlib
from cryptography.fernet import Fernet
import tkinter as tk

# Функция, которая генерирует ключ SHA-256
def generate_sha256_key(text):
    # Convert text to bytes
    text_bytes = text.encode('utf-8')

    # Generate SHA-256 hash object
    sha256_hash_obj = hashlib.sha256()

    # Update hash object with text bytes
    sha256_hash_obj.update(text_bytes)

    # Generate SHA-256 key
    sha256_key = sha256_hash_obj.digest()

    return sha256_key

# Функция, которая переводит текст в японский двоичный код:
def text_to_japanese_binary(text):
    # Convert text to bytes
    text_bytes = text.encode('utf-8')

    # Convert bytes to binary string
    binary_str = ''.join(format(byte, '08b') for byte in text_bytes)

    # Create dictionary of Japanese 0 and 1 characters
    japanese_dict = {'0': '零', '1': '壱'}

    # Replace 0 and 1 with Japanese characters
    japanese_str = ''.join([japanese_dict[char] for char in binary_str])

    return japanese_str

# Функция, которая шифрует текст с использованием ключа
def encrypt_message(key, plaintext):
    # Create Fernet cipher object with key
    cipher = Fernet(key)

    # Convert plaintext to bytes
    plaintext_bytes = plaintext.encode('utf-8')

    # Encrypt plaintext with cipher
    ciphertext = cipher.encrypt(plaintext_bytes)

    # Convert ciphertext to string representation
    ciphertext_str = ciphertext.decode('utf-8')

    return ciphertext_str

# Функция, которая расшифровывает текст с использованием ключа
def decrypt_message(key, ciphertext_str):
    # Create Fernet cipher object with key
    cipher = Fernet(key)

    # Convert ciphertext string to bytes
    ciphertext_bytes = ciphertext_str.encode('utf-8')

    # Decrypt ciphertext with cipher
    plaintext_bytes = cipher.decrypt(ciphertext_bytes)

    # Convert plaintext bytes to string
    plaintext = plaintext_bytes.decode('utf-8')

    return plaintext


# Создание графического интерфейса с помощью tkinter
def gui():
    # Функция, которая обрабатывает событие нажатия на кнопку "Encrypt"
    def encrypt_callback():
        # Получить текст из поля ввода
        plaintext = plaintext_entry.get()

        # Сгенерировать SHA-256 ключ
        key = generate_sha256_key(plaintext)

        # Перевести текст в японский двоичный код
        japanese_binary = text_to_japanese_binary(plaintext)

        # Зашифровать текст с использованием ключа
        ciphertext = encrypt_message(key, japanese_binary)

        # Вывести зашифрованный текст в текстовое поле
        ciphertext_text.delete(1.0, tk.END)
        ciphertext_text.insert(tk.END, ciphertext)

    # Функция, которая обрабатывает событие нажатия на кнопку "Decrypt"
    def decrypt_callback():
        # Получить текст из поля ввода
        ciphertext = ciphertext_text.get(1.0, tk.END).strip()

        # Получить ключ из введенного зашифрованного текста
        plaintext = plaintext_entry.get()
        key = generate_sha256_key(plaintext)

        # Расшифровать текст с использованием ключа
        japanese_binary = decrypt_message(key, ciphertext)

        # Перевести текст из японского двоичного кода в исходный текст
        japanese_dict = {'零': '0', '壱': '1'}
        binary_str = ''.join([japanese_dict[char] for char in japanese_binary])
        plaintext = bytearray.fromhex(hex(int(binary_str, 2))[2:]).decode()

        # Вывести расшифрованный текст в текстовое поле
        plaintext_text.delete(1.0, tk.END)
        plaintext_text.insert(tk.END, plaintext)

    # Создание главного окна
    window = tk.Tk()
    window.title('Japanese Binary Cipher')

    # Создание метки и поля ввода для исходного текста
    plaintext_label = tk.Label(window, text='Plaintext:')
    plaintext_label.grid(row=0, column=0, padx=5, pady=5)

    plaintext_entry = tk.Entry(window)
    plaintext_entry.grid(row=0, column=1, padx=5, pady=5)

    # Создание метки и текстового поля для зашифрованного текста
    ciphertext_label = tk.Label(window, text='Ciphertext:')
    ciphertext_label.grid(row=1, column=0, padx=5, pady=5)

    ciphertext_text = tk.Text(window, height=10, width=50)
    ciphertext_text.grid(row=1, column=1, padx=5, pady=5)

    # Создание метки и текстового поля для расшифрованного текста
    plaintext_label = tk.Label(window, text='Plaintext:')
    plaintext_label.grid(row=2, column=0, padx=5, pady=5)

    plaintext_text = tk.Text(window, height=10, width=50)
    plaintext_text.grid(row=2, column=1, padx=5, pady=5)

    # Создание кнопок для шифрования и расшифрования
    encrypt_button = tk.Button(window, text='Encrypt', command=encrypt_callback)
    encrypt_button.grid(row=3, column=0, padx=5, pady=5)

    decrypt_button = tk.Button(window, text='Decrypt', command=decrypt_callback)
    decrypt_button.grid(row=3, column=1, padx=5, pady=5)

    # Запуск главного цикла событий tkinter
    window.mainloop()

# Запуск графического интерфейса
gui()
