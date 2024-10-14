import csv

# 从CSV文件中读取用户列表
def load_users_from_csv(file_path: str):
    users = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            users.append({
                "username": row["username"],
                "password": row["password"],
                "isAdmin": row["isAdmin"].lower() == 'true'
            })
    return users