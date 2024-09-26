# 基于同态加密的隐私保护投票系统

## 框架图

![框架图](img/基于同态加密的隐私保护投票系统/image.png)

## 密码学安全逻辑

![密码学安全逻辑](img/基于同态加密的隐私保护投票系统/image1.png)

## 后端接口文档

### 数据需求方 `端口号：5000`

1. **获取公钥**：

- URL: /get_pubkey
- method: GET
- response:

```json
{
    "status": "success",
    "message": "Public key fetched",
    "key": {
        "班干部":[123,123],
        "学习委员":[123,123]
    }
}
```

2. **删除投票会话（删除密钥对,删除投票对象信息,删除投票结果）**：

- URL: /restart
- method: POST
- request:

```json
{
    "vote_obj": "班干部",
}
```

- response:

```json
{
    "status": "success",
    "message": "Restart success"
}
```

Error:

```json
{
    "status": "error",
    "message": "No vote info"
}
```

3. **设置投票信息**：

- URL: /set_vote_info
- method: POST
- request:

```json
{
    "vote_obj": "班干部",
    "list": ["teacher1", "teacher2", "teacher3"]
}
```

- response:

```json
{
    "status": "success",
    "message": "Vote info saved"
}
```

4. **获取投票信息**：

- URL: /get_vote_info
- method: GET
- response:

```json
{
    "status": "success",
    "message": "Vote info fetched",
    "result":[
        {
            "vote_obj": "班干部",
            "list": ["teacher1", "teacher2", "teacher3"]
        },
        {
            "vote_obj": "学习委员",
            "list": ["student1", "student2", "student3"]
        }
    ]
}
```

Error:

```json
{
    "status": "error",
    "message": "No vote info"
} 
```

5. **获取投票结果**：

- URL: /get_vote_result
- method: GET
- response:

分数为总分
正常包含投票结果

```json
{
    "status": "success",
    "message": "Vote result fetched",
    "vote_obj":{
        "班干部":{
            "result": {
                "teacher1": 123,
                "teacher2": 123,
                "teacher3": 123
            },
            "vote_people_number":123
        },
        "学习委员":{
            "result": {
                "student1": 123,
                "student2": 123,
                "student3": 123
            },
            "vote_people_number":123
        },
    }
}
```

有投票会话未有人投票

```json
{
    "status": "success",
    "message": "Vote result fetched",
    "vote_obj":{
        "班干部":{
            "result": "No vote result", 
            "vote_people_number":0
        },
        "学习委员":{
            "result": {
                "student1": 123,
                "student2": 123,
                "student3": 123
            },
            "vote_people_number":123
        },
    }
}
```

6. **接收加密投票**：`三方计算接口`

- URL: /receive_vote
- method: POST
- request:

```json
{
    "vote_obj": "班干部",
    "vote_sum":{
        "teacher1":123,
        "teacher2":123,
        "teacher3":123
    },
    "user_sum":["userA","userB"]
}
```

- response:

```json
{
    "status": "success",
    "message": "Vote received"
}
```

### 三方计算 `端口号：5001`

1. **删除投票会话（删除加密投票信息）**：

- URL: /restart
- method: POST
- request:

```json
{
    "vote_obj": "班干部",
}
```

- response:

```json
{
    "status": "success",
    "message": "Restart success"
}
```

Error:

```json
{
    "status": "error",
    "message": "No vote info"
}
```

2. **提交加密投票**：

- URL: /submit_vote
- method: POST
- request:

```json
{
    "username": "userA",
    "vote_obj": "班干部",
    "vote": {
        "teacher1":123,
        "teacher2":123,
        "teacher3":123
    },
    "pubkey": [123, 123]
}
```

- response:

```json
{
    "status": "success",
    "message": "Vote submitted"
}
```
