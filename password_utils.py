import random
import string

# 生成随机密码
def generate_password(length, use_upper, use_lower, use_digits, use_special):
    characters = ''
    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    if characters == '':
        return ''

    return ''.join(random.choice(characters) for _ in range(length))
