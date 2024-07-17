import os
from crypto_utils import generate_key, encrypt_data, decrypt_data
from cryptography.fernet import InvalidToken

# 创建保存文件夹
home_dir = os.path.expanduser('~')
SAVE_DIR = os.path.join(home_dir, 'password_person')
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def save_data(master_password, website, username, password):
    key = generate_key(master_password)
    encrypted_password = encrypt_data(password, key)

    # 保存到 txt 文件
    with open(os.path.join(SAVE_DIR, 'passwords.txt'), 'a') as file:
        file.write(f'{website},{username},{encrypted_password}\n')

    # 保存到 md 文件
    with open(os.path.join(SAVE_DIR, 'passwords.md'), 'a') as file:
        file.write(f'### {website}\n')
        file.write(f'- **Username**: {username}\n')
        file.write(f'- **Password**: {encrypted_password}\n\n')
        
def query_data(master_password, website):
    key = generate_key(master_password)
    results = []
    invalid_key_encountered = False
    try:
        with open(os.path.join(SAVE_DIR, 'passwords.txt'), 'r') as file:
            for line in file:
                stored_website, stored_username, encrypted_password = line.strip().split(',')
                if stored_website == website:
                    try:
                        password = decrypt_data(encrypted_password, key)
                        results.append((stored_username, password))
                    except InvalidToken:
                        invalid_key_encountered = True
                        continue
    except FileNotFoundError:
        return None, None

    if results:
        return results
    elif invalid_key_encountered:
        return "Invalid master key"
    else:
        return None

def delete_data(master_password, website):
    key = generate_key(master_password)
    txt_file_path = os.path.join(SAVE_DIR, 'passwords.txt')
    md_file_path = os.path.join(SAVE_DIR, 'passwords.md')

    try:
        with open(txt_file_path, 'r') as file:
            lines = file.readlines()

        new_lines = [line for line in lines if not line.startswith(website + ',')]
        
        if len(new_lines) == len(lines):
            return False  # 没有找到匹配的条目

        with open(txt_file_path, 'w') as file:
            file.writelines(new_lines)

        with open(md_file_path, 'r') as file:
            md_lines = file.readlines()

        new_md_lines = []
        skip = False
        for line in md_lines:
            if line.startswith(f'### {website}'):
                skip = True
            elif skip and line.startswith('### '):
                skip = False
                new_md_lines.append(line)
            elif not skip:
                new_md_lines.append(line)

        with open(md_file_path, 'w') as file:
            file.writelines(new_md_lines)

        return True
    except FileNotFoundError:
        return False
