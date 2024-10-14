import json

# 读取 config.json 文件
with open('config.json') as config_file:
    config = json.load(config_file)

SECRET_KEY = config['SECRET_KEY']