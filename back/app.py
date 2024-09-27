from flask import Flask, request, send_file, jsonify
import Paillier
import json
import os

app = Flask(__name__)

# 删除投票会话
@app.route('/restart', methods=['POST'])
def restart():

    data=request.json
    vote_obj=data["vote_obj"]
    if os.path.exists('vote/'+vote_obj):# 删除vote文件夹
        file_list = os.listdir('vote/'+vote_obj)
        for file in file_list:
            os.remove('vote/'+vote_obj+'/'+file)
        os.rmdir('vote/'+vote_obj)
        return jsonify({'status': 'success', 'message': 'Restart success'})
    else:# 无投票对象
        return jsonify({'status': 'error', 'message': 'No vote info'})

# 获取公钥
@app.route('/get_pubkey', methods=['GET'])
def get_pubkey():

    file_list = os.listdir('vote')
    if len(file_list)==0:# 无投票对象
        return jsonify({'status': 'error', 'message': 'No vote info'})
    else:
        key={}
        for file in file_list:
            with open('vote/' + file+"/key.json", 'r') as f:
                now_key = json.load(f)
            public_key = now_key['public_key']
            key[file]=public_key
        return jsonify({'status': 'success', 'message': 'Public key fetched', 'key': key})


# 设置投票对象信息
@app.route('/set_vote_info', methods=['POST'])
def set_vote_info():
    data = request.json
    vote_obj=data["vote_obj"]
    # 建立文件夹
    if not os.path.exists("vote/"+vote_obj):
        os.makedirs("vote/"+vote_obj)
    vote_info_path="vote/"+vote_obj+"/"+"vote_info.json"
    key_path="vote/"+vote_obj+"/"+"key.json"
    with open(vote_info_path, 'w',encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    Paillier.save_keypair(key_path)
    return jsonify({'status': 'success', 'message': 'Vote info saved'})

# 获取投票对象信息
@app.route('/get_vote_info', methods=['GET'])
def get_vote_info():
   
    file_list = os.listdir('vote')
    if len(file_list)==0:
        return jsonify({'status': 'error', 'message': 'No vote info'})
    else:
        data = []
        for file in file_list:
            with open('vote/' + file+"/vote_info.json", 'r',encoding="utf-8") as f:
                vote_info = json.load(f)
            data.append(vote_info)
        return jsonify({'status': 'success', 'message': 'Vote info fetched', 'result': data})

# 获取投票结果
@app.route('/get_vote_result', methods=['GET'])
def get_vote_result():

    file_list = os.listdir('vote')
    if len(file_list)==0:# 无投票对象
        return jsonify({'status': 'error', 'message': 'No vote info'})
    else:
        data = {}
        for file in file_list:
            if not os.path.exists('vote/' + file+"/sum_dec.json"):# 无投票结果
                vote_info = {"result":"No vote result","vote_people_number":0}
            else:
                with open('vote/' + file+"/sum_dec.json", 'r',encoding="utf-8") as f:
                    file_data = json.load(f)
                vote_info = {"result":file_data['vote_sum'],"vote_people_number":file_data['user_sum_number']}
            data[file]=vote_info
        return jsonify({'status': 'success', 'message': 'Vote info fetched', 'vote_obj': data})


# 接收投票结果（三方计算接口）
@app.route('/receive_vote', methods=['POST'])
def receive_vote():
    data=request.json
    vote_obj = data['vote_obj']
    path_head='vote/'+vote_obj
    # 保存加密投票结果
    with open(path_head+"/sum_enc.json", "w",encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    user_sum = data['user_sum']
    # 计算投票总人数
    user_sum_number = len(user_sum)
    vote_sum = data['vote_sum']
    with open(path_head+'/key.json', 'r') as f:
        key = json.load(f)
    # 投票结果解密
    for vote_obj in vote_sum:
        vote_sum[vote_obj] = Paillier.decrypt(key['private_key'], key['public_key'], vote_sum[vote_obj])
    # 保存解密投票结果
    with open(path_head+"/sum_dec.json", "w",encoding="utf-8") as f:
        json.dump({"vote_sum":vote_sum,"user_sum_number":user_sum_number}, f, ensure_ascii=False)

    return jsonify({'status': 'success', 'message': 'Vote received'})
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=15000, debug=True)
    
