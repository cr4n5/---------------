from flask import Flask, request, send_file, jsonify
import Paillier
import json
import os

app = Flask(__name__)

# 重启投票系统
@app.route('/restart', methods=['POST'])
def restart():

    if os.path.exists('key.json'):
        os.remove('key.json')
    if os.path.exists('vote_info.json'):
        os.remove('vote_info.json')
    if os.path.exists('sum_enc.json'):
        os.remove('sum_enc.json')
    if os.path.exists('sum_dec.json'):
        os.remove('sum_dec.json')
        
    return jsonify({'status': 'success', 'message': 'Restart success'})

# 获取公钥
@app.route('/get_pubkey', methods=['GET'])
def get_pubkey():
    # 判断是否存在key.json
    if os.path.exists('key.json'):
        with open('key.json', 'r') as f:
            key = json.load(f)
        return jsonify({'status': 'success', 'message': 'Public key fetched', 'key': key['public_key']})
    else:
        Paillier.save_keypair()
        with open('key.json', 'r') as f:
            key = json.load(f)
        return jsonify({'status': 'success', 'message': 'Public key generated', 'key': key['public_key']})

# 设置投票对象信息
@app.route('/set_vote_info', methods=['POST'])
def set_vote_info():
    data = request.json
    with open('vote_info.json', 'w') as f:
        json.dump(data, f)
    return jsonify({'status': 'success', 'message': 'Vote info saved'})

# 获取投票对象信息
@app.route('/get_vote_info', methods=['GET'])
def get_vote_info():
    if os.path.exists('vote_info.json'):
        with open('vote_info.json', 'r') as f:
            data = json.load(f)
        return jsonify({'status': 'success', 'message': 'Vote info fetched', 'list': data['list']})
    else:
        return jsonify({'status': 'error', 'message': 'No vote info'})

# 获取投票结果
@app.route('/get_vote_result', methods=['GET'])
def get_vote_result():
    if os.path.exists('sum_dec.json'):
        with open('sum_dec.json', 'r') as f:
            data = json.load(f)
        return jsonify({'status': 'success', 'message': 'Vote result fetched', 'result': data['vote_sum'], 'vote_people_number': data['user_sum_number']})
    else:
        return jsonify({'status': 'error', 'message': 'No vote result'})


# 接收投票结果（三方计算接口）
@app.route('/receive_vote', methods=['POST'])
def receive_vote():
    data=request.json
    # 保存加密投票结果
    with open("sum_enc.json", "w") as f:
        json.dump(data, f)
    user_sum = data['user_sum']
    # 计算投票总人数
    user_sum_number = len(user_sum)
    vote_sum = data['vote_sum']
    with open('key.json', 'r') as f:
        key = json.load(f)
    # 投票结果解密
    for vote_obj in vote_sum:
        vote_sum[vote_obj] = Paillier.decrypt(key['private_key'], key['public_key'], vote_sum[vote_obj])
    # 保存解密投票结果
    with open("sum_dec.json", "w") as f:
        json.dump({"vote_sum":vote_sum,"user_sum_number":user_sum_number}, f)

    return jsonify({'status': 'success', 'message': 'Vote received'})
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    
