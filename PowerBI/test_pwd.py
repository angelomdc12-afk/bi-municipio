from auth_utils import verify_password

hash_val = "pbkdf2_sha256$260000$bb8d2e08966ae3f0158d4bd2dc53b7c9$f0d59c4ef37ab0af7644ecfba1d17a6efd18bcddb6b22510f609c5c07b7a1c89"
test_passwords = ["admin", "123456", "password", "12345678", "admin123", "patris", "123", ""]

for pwd in test_passwords:
    result = verify_password(pwd, hash_val)
    print(f"{pwd}: {result}")
