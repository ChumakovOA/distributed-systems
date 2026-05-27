import requests
import json
from cryptography.fernet import Fernet

# Загрузка ключа Fernet
with open("encryption_key.txt", "rb") as f:
    key = f.read()

fernet = Fernet(key)

print("=" * 50)
print("АУТЕНТИФИКАЦИЯ")
print("=" * 50)

# =========================
# ПОЛУЧЕНИЕ ТОКЕНА (ЛОГИН)
# =========================

# Ваш сервер не требует логин/пароль, просто отправляем пустой запрос
try:
    login_resp = requests.post(
        "http://127.0.0.1:8000/login",  # Используем /login, а не /api/auth
        json={},  # Пустой запрос
        timeout=5
    )
    
    if login_resp.status_code != 200:
        print(f"Ошибка аутентификации: {login_resp.status_code}")
        print(login_resp.text)
        exit(1)
    
    token = login_resp.json()["token"]
    print(f"✅ Получен токен: {token}")
    
except Exception as e:
    print(f"Ошибка: {e}")
    exit(1)

# =========================
# ВВОД ДАННЫХ
# =========================

print("\n" + "=" * 50)
print("ОТПРАВКА ДАННЫХ")
print("=" * 50)

user_data = input("\nВведите сообщение: ")

# Шифруем данные (просто строку, не JSON)
encrypted_data = fernet.encrypt(user_data.encode()).decode()

# =========================
# ОТПРАВКА (по формату вашего сервера)
# =========================

try:
    resp = requests.post(
        "http://127.0.0.1:8000/api/data",
        json={"data": encrypted_data},  # Только data, без вложенного JSON
        headers={"Authorization": token},  # Токен в заголовке!
        timeout=5
    )
    
    print("\n" + "=" * 50)
    print("ОТВЕТ СЕРВЕРА")
    print("=" * 50)
    
    if resp.status_code == 200:
        result = resp.json()
        print(f"✅ Статус: {result.get('status')}")
        print(f"📨 Сообщение: {result.get('message')}")
    else:
        print(f"❌ Ошибка: {resp.status_code}")
        print(resp.json())
        
except Exception as e:
    print(f"Ошибка: {e}")