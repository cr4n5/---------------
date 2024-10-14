import json
import requests
from flask import Flask, request, send_file, jsonify
import Paillier
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    data = request.json
    vote_obj = data['vote_obj']
    # 保存在文件夹下
    path_head='vote/'+vote_obj
    if not os.path.exists(path_head):
        os.makedirs(path_head)
    
    path_name = 'vote/' + vote_obj+ "/" + data['username'] + '.json'
    with open(path_name, 'w',encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    # 加密结果求和
    pubkey = data['pubkey']
    # 判断是否存在sum.json
    if os.path.exists(path_head+'/sum.json'):
        with open(path_head+'/sum.json', 'r',encoding="utf-8") as f:
            sum_data = json.load(f)
        vote_sum = sum_data['vote_sum']
        user_sum = sum_data['user_sum']
        # 判断是否已经投票
        if data['username'] not in user_sum:
            for vote_obj in data['vote']:
                vote_sum[vote_obj] = Paillier.homomorphic_addition(pubkey, data['vote'][vote_obj], vote_sum[vote_obj])
            user_sum.append(data['username'])
            with open(path_head+'/sum.json', 'w',encoding="utf-8") as f:
                json.dump({'vote_sum': vote_sum, 'user_sum': user_sum}, f, ensure_ascii=False)
        else:# 已经投票,更新投票结果
            vote_sum = data['vote']# 重新初始化
            user_sum = [data["username"]]
            file_list = os.listdir(path_head)
            for file in file_list:# 遍历所有投票文件,更新投票结果
                if file == data['username'] + '.json':# 除去初始化时所使用的当前投票者结果
                    continue
                if file == 'sum.json':
                    continue
                else:
                    with open(path_head+"/"+file, 'r',encoding="utf-8") as f:
                        vote_data = json.load(f)
                    for vote_obj in vote_data['vote']:
                        vote_sum[vote_obj] = Paillier.homomorphic_addition(pubkey, vote_data['vote'][vote_obj], vote_sum[vote_obj])
                    user_sum.append(vote_data['username'])
            with open(path_head+'/sum.json', 'w',encoding="utf-8") as f:
                json.dump({'vote_sum': vote_sum, 'user_sum': user_sum}, f, ensure_ascii=False)
    else:
        # 第一次投票
        vote_sum = data['vote']
        user_sum = [data["username"]]
        with open(path_head+'/sum.json', 'w',encoding="utf-8") as f:
            json.dump({'vote_sum': vote_sum, 'user_sum': user_sum}, f, ensure_ascii=False)

    # 将加密结果发送给数据需求方
    url="http://192.168.0.118:5000/receive_vote"
    requests.post(url, json={'vote_obj':data["vote_obj"], 'vote_sum': vote_sum, 'user_sum': user_sum})

    return jsonify({'status': 'success', 'message': 'Vote submitted'})

@app.route('/restart', methods=['POST'])
def restart():
    
    data=request.json
    vote_obj=data["vote_obj"]
    if os.path.exists('vote/'+vote_obj):
        file_list = os.listdir('vote/'+vote_obj)
        for file in file_list:
            os.remove('vote/'+vote_obj+'/'+file)
        os.rmdir('vote/'+vote_obj)
        return jsonify({'status': 'success', 'message': 'Restart success'})
    else:
        return jsonify({'status': 'error', 'message': 'No vote info'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
    