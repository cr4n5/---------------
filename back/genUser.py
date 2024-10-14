import csv
import random
import string
import argparse

def generate_random_username():
    return 'user' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))

def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(characters, k=length))
    return password

def add_random_users_to_csv(file_path, num_users):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        for _ in range(num_users):
            new_username = generate_random_username()
            new_password = generate_strong_password()
            is_admin = 'False'
            writer.writerow([new_username, new_password, is_admin])
            print(f"Added user: {new_username}, password: {new_password}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random non-admin users and add them to a CSV file.")
    parser.add_argument('-n', '--num_users', type=int, required=True, help="Number of users to generate")
    args = parser.parse_args()

    file_path = 'users.csv'
    add_random_users_to_csv(file_path, args.num_users)