from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
import os
import json
import logging
import Paillier
from models import RestartRequest, LoginRequest, SetVoteInfoRequest
from auth import authenticate_token
from utils import load_users_from_csv
from config import SECRET_KEY
import jwt
from datetime import datetime, timedelta

# 确保在模块的开头配置日志记录
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
router = APIRouter()

users = load_users_from_csv('users.csv')

# 添加通用的 OPTIONS 路由
@router.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str):
    return {"message": "Preflight request handled"}

@router.post("/login")
async def login(request: LoginRequest): 
    username = request.username
    password = request.password

    # 验证用户
    user = next((user for user in users if user["username"] == username and user["password"] == password), None)
    if user:
        expiration = datetime.utcnow() + timedelta(hours=1)  # 设置令牌过期时间为1小时
        token = jwt.encode({"username": username, "isAdmin": user["isAdmin"], "exp": expiration}, SECRET_KEY, algorithm="HS256")
        return JSONResponse(content={'status': 'success', 'token': token, 'code': 200}, status_code=200)
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

# 删除投票会话
@router.post("/restart")
async def restart(request: RestartRequest, token: dict = Depends(authenticate_token)):
    if token["isAdmin"] == "False":
        raise HTTPException(status_code=403, detail="Permission denied")
    vote_obj = request.vote_obj
    try:
        if os.path.exists('vote/' + vote_obj):  # 删除vote文件夹
            file_list = os.listdir('vote/' + vote_obj)
            for file in file_list:
                os.remove('vote/' + vote_obj + '/' + file)
            os.rmdir('vote/' + vote_obj)
            return JSONResponse(content={'status': 'success', 'message': 'Restart success', 'code': 200}, status_code=200)
        else:  # 无投票对象
            raise HTTPException(status_code=404, detail="No vote info")
    except Exception as e:
        return JSONResponse(content={'status': 'error', 'message': str(e), 'code': 500}, status_code=500)

# 获取公钥
@router.get("/get_pubkey")
async def get_pubkey(token: dict = Depends(authenticate_token)):
    # 确保token是合法的，无论是管理员还是普通用户
    print(token)
    try:
        file_list = os.listdir('vote')
        if len(file_list) == 0:  # 无投票对象
            raise HTTPException(status_code=404, detail="No vote info")
        else:
            key = {}
            for file in file_list:
                with open('vote/' + file + "/key.json", 'r') as f:
                    now_key = json.load(f)
                public_key = now_key['public_key']
                public_key = [str(public_key[0]), str(public_key[1])]
                key[file] = public_key
            return JSONResponse(content={'status': 'success', 'message': 'Public key fetched', 'key': key, 'code': 200}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'status': 'error', 'message': str(e), 'code': 500}, status_code=500)

# 设置投票对象信息
@router.post("/set_vote_info")
async def set_vote_info(request: SetVoteInfoRequest, token: dict = Depends(authenticate_token)):
    vote_obj = request.vote_obj
    try:
        # 建立文件夹
        if not os.path.exists("vote/" + vote_obj):
            os.makedirs("vote/" + vote_obj)
        vote_info_path = "vote/" + vote_obj + "/" + "vote_info.json"
        key_path = "vote/" + vote_obj + "/" + "key.json"
        with open(vote_info_path, 'w', encoding="utf-8") as f:
            json.dump(request.dict(), f, ensure_ascii=False)
        Paillier.save_keypair(key_path)
        return JSONResponse(content={'status': 'success', 'message': 'Vote info saved', 'code': 200}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'status': 'error', 'message': str(e), 'code': 500}, status_code=500)

# 获取投票对象信息
@router.get("/get_vote_info")
async def get_vote_info(token: dict = Depends(authenticate_token)):
    try:
        file_list = os.listdir('vote')
        if len(file_list) == 0:
            raise HTTPException(status_code=404, detail="No vote info")
        else:
            data = []
            for file in file_list:
                with open('vote/' + file + "/vote_info.json", 'r', encoding="utf-8") as f:
                    vote_info = json.load(f)
                data.append(vote_info)
            return JSONResponse(content={'status': 'success', 'message': 'Vote info fetched', 'result': data, 'code': 200}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'status': 'error', 'message': str(e), 'code': 500}, status_code=500)

# 获取投票结果
@router.get("/get_vote_result")
async def get_vote_result(token: dict = Depends(authenticate_token)):
    try:
        file_list = os.listdir('vote')
        if len(file_list) == 0:  # 无投票对象
            raise HTTPException(status_code=404, detail="No vote info")
        else:
            data = {}
            for file in file_list:
                if not os.path.exists('vote/' + file + "/sum_dec.json"):  # 无投票结果
                    vote_info = {"result": "No vote result", "vote_people_number": 0}
                else:
                    with open('vote/' + file + "/sum_dec.json", 'r', encoding="utf-8") as f:
                        file_data = json.load(f)
                    vote_info = {"result": file_data['vote_sum'], "vote_people_number": file_data['user_sum_number']}
                data[file] = vote_info
            return JSONResponse(content={'status': 'success', 'message': 'Vote info fetched', 'vote_obj': data, 'code': 200}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'status': 'error', 'message': str(e), 'code': 500}, status_code=500)

# 接收投票结果（三方计算接口）
@router.post("/receive_vote")
async def receive_vote(request: Request):
    data= await request.json()
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

    return JSONResponse(content={'status': 'success', 'message': 'Vote received', 'code': 200}, status_code=200)

