import os
from data_crypto import generate_key, encrypt_data, decrypt_data
from cryptography.fernet import InvalidToken


# 创建保存文件夹
home_dir = os.path.expanduser('~')
SAVE_DIR = os.path.join(home_dir, 'password_person')
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# 检查并创建passwords.md和passwords.txt文件
md_file_path = os.path.join(SAVE_DIR, 'passwords.md')
txt_file_path = os.path.join(SAVE_DIR, 'passwords.txt')

# 如果文件不存在，则创建它们
if not os.path.exists(md_file_path):
    open(md_file_path, 'w').close()

if not os.path.exists(txt_file_path):
    open(txt_file_path, 'w').close()


# 保存数据
def save_data(master_password, website, username, password):
    key = generate_key(master_password)
    encrypted_password = encrypt_data(password, key)

    if check_existing_entry(key, website, username, password):
        return False

    # 保存到 txt 文件
    with open(txt_file_path, 'a') as file:
        file.write(f'{website},{username},{encrypted_password}\n')

    # 保存到 md 文件
    with open(md_file_path, 'a') as file:
        file.write(f'### {website}\n')
        file.write(f'- **Username**: {username}\n')
        file.write(f'- **Password**: {encrypted_password}\n\n')

    return True


# 检查是否存在相同的条目
def check_existing_entry(key, website, username, password):
    # 检查文件是否为空
    if os.path.getsize(txt_file_path) == 0:
        return False
    
    with open(txt_file_path, 'r') as file:
        for line in file:
            stored_website, stored_username, stored_encrypted_password = line.strip().split(',')
            if stored_website == website and stored_username == username:
                try:
                    stored_password = decrypt_data(stored_encrypted_password, key)
                    if stored_password == password:
                        return True
                except Exception as e:
                    # 解密失败，可能是因为密钥不匹配或数据损坏
                    continue
    return False
        

# 查询数据
def query_data(master_password, website):
    key = generate_key(master_password)
    results = []
    invalid_key_encountered = False
    
    # 拆分输入的 website，使用多种分隔符
    search_terms = set(website.replace('://', '.').replace('/', '.').split('.'))
    if '' in search_terms : search_terms.remove('')
    
    try:
        with open(txt_file_path, 'r') as file:
            for line in file:
                stored_website, stored_username, encrypted_password = line.strip().split(',')
                
                # 检查存储的 website 是否包含任意一个搜索词
                stored_website_parts = set(stored_website.replace('://', '.').replace('/', '.').split('.'))
                if search_terms & stored_website_parts:
                    try:
                        password = decrypt_data(encrypted_password, key)
                        results.append((stored_website, stored_username, password))
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


# 删除数据
def delete_data(master_password, website):
    key = generate_key(master_password)

    try:
        with open(txt_file_path, 'r') as file:
            lines = file.readlines()

        # 尝试解密以验证主密钥
        valid_key = False
        for line in lines:
            stored_website, stored_username, encrypted_password = line.strip().split(',')
            if stored_website == website:
                try:
                    decrypt_data(encrypted_password, key)
                    valid_key = True
                    break
                except InvalidToken:
                    return "Invalid master key"

        if not valid_key:
            return False  # 没有找到匹配的条目

        # 进行删除操作
        new_lines = [line for line in lines if not line.startswith(website + ',')]
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
