import json
import requests
from flask import Flask, request, send_file, jsonify
import Paillier
import os

app = Flask(__name__)

@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    data = request.json
    # 保存在vote文件夹下
    path_name = 'vote/' + data['username'] + '.json'
    with open(path_name, 'w') as f:
        f.write(json.dumps(data))
    # 加密结果求和
    pubkey = data['pubkey']
    # 判断是否存在sum.json
    if os.path.exists('sum.json'):
        with open('sum.json', 'r') as f:
            sum_data = json.load(f)
        vote_sum = sum_data['vote_sum']
        user_sum = sum_data['user_sum']
        # 判断是否已经投票
        if data['username'] not in user_sum:
            for vote_obj in data['vote']:
                vote_sum[vote_obj] = Paillier.homomorphic_addition(pubkey, data['vote'][vote_obj], vote_sum[vote_obj])
            user_sum.append(data['username'])
            with open('sum.json', 'w') as f:
                json.dump({'vote_sum': vote_sum, 'user_sum': user_sum}, f)
        else:# 已经投票,更新投票结果
            vote_sum = data['vote']# 重新初始化
            user_sum = [data["username"]]
            file_list = os.listdir('vote')
            for file in file_list:# 遍历所有投票文件,更新投票结果
                if file == data['username'] + '.json':# 除去初始化时所使用的当前投票者结果
                    continue
                else:
                    with open('vote/' + file, 'r') as f:
                        vote_data = json.load(f)
                    for vote_obj in vote_data['vote']:
                        vote_sum[vote_obj] = Paillier.homomorphic_addition(pubkey, vote_data['vote'][vote_obj], vote_sum[vote_obj])
                    user_sum.append(vote_data['username'])
            with open('sum.json', 'w') as f:
                json.dump({'vote_sum': vote_sum, 'user_sum': user_sum}, f)
    else:
        # 第一次投票
        vote_sum = data['vote']
        user_sum = [data["username"]]
        with open('sum.json', 'w') as f:
            json.dump({'vote_sum': vote_sum, 'user_sum': user_sum}, f)

    # 将加密结果发送给数据需求方
    url="http://127.0.0.1:5000/receive_vote"
    response = requests.post(url, json={'vote_sum': vote_sum, 'user_sum': user_sum})

    return jsonify({'status': 'success', 'message': 'Vote submitted'})

@app.route('/restart', methods=['POST'])
def restart():
    # 删除vote文件夹下所有文件
    file_list = os.listdir('vote')
    for file in file_list:
        os.remove('vote/' + file)

    # 删除sum.json
    if os.path.exists('sum.json'):
        os.remove('sum.json')

    return jsonify({'status': 'success', 'message': 'Restart success'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
    