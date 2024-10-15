const BackendApiUrl = import.meta.env.VITE_BACKEND_DATA_CONSUMER_API_URL

// 本部分为interface定义

/**
 * 投票信息
 * @property {string} vote_obj 投票对象
 * @property {string[]} list 投票列表
 */
export interface VoteInfo {
  vote_obj: string
  list: string[]
}

/**
 * 获取公钥响应
 * @property {string} status 状态
 * @property {string} message 消息
 * @property {{[key: string]: [string, string]}} key 公钥
 * @property {number} code 代码
 */
export interface getPublicKeyResponse {
  status: string
  message: string
  key: {
    [vote_obj: string]: [string, string]
  }
  code: number
}
/**
 * 投票信息响应
 * @property {string} status 状态
 * @property {string} message 消息
 * @property {VoteInfo[]} result 结果
 * @property {number} code 代码
 */
export interface VoteInfoResponse {
  status: string
  message: string
  result: VoteInfo[]
  code: number
}

/**
 * 重启投票
 * @property {string} vote_obj 投票对象
 */
export interface restartVoteObj {
  vote_obj: string
}
/**
 * 设置投票信息响应
 * @property {string} status 状态
 * @property {string} message 消息
 */
interface setVoteInfoResponse {
  status: string
  message: string
}
/**
 * 获取投票结果响应
 * @property {string} status 状态
 * @property {string} message 消息
 * @property {object} vote_obj 投票对象
 */
export interface VoteResultResponse {
  code: number
  status: string
  message: string
  vote_obj: {
    [key: string]: {
      result:
        | string
        | {
            [key: string]: number
          }
      vote_people_number: number
    }
  }
}
// 本部分为函数定义

/**
 * 登录
 * @param username 用户名
 * @param password 密码
 * @returns 登录成功后返回的 token
 */
export async function login(username: string, password: string) {
  const response = await fetch(`${BackendApiUrl}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username,
      password
    })
  })

  if (!response.ok) {
    throw new Error('登录失败')
  }

  const data = await response.json()
  return data.token
}

/**
 * 获取投票信息
 * @param jwtToken token
 * @returns 投票信息
 */
export async function getVoteInfo(jwtToken: string): Promise<VoteInfoResponse> {
  try {
    const response = await fetch(`${BackendApiUrl}/get_vote_info`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${jwtToken}`,
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error('Network response was not ok')
    }

    const data: VoteInfoResponse = await response.json()
    return data
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error)
    return {
      message: 'Error',
      result: [],
      code: 500,
      status: 'failed'
    } as VoteInfoResponse // 返回一个默认的 VoteInfoResponse 对象
  }
}

/**
 * 设置投票信息
 * @param jwtToken token
 * @param voteInfo 投票信息
 * @returns 设置投票信息响应
 */
export async function setVoteInfo(
  jwtToken: string,
  voteInfo: VoteInfo
): Promise<setVoteInfoResponse> {
  try {
    const response = await fetch(`${BackendApiUrl}/set_vote_info`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${jwtToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(voteInfo)
    })

    if (!response.ok) {
      throw new Error('Network response was not ok')
    }

    const data = await response.json()

    return data
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error)
    return {
      message: 'Error',
      status: 'failed'
    }
  }
}

export async function restartVote(jwtToken: string, voteObj: restartVoteObj) {
  try {
    const response = await fetch(`${BackendApiUrl}/restart`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${jwtToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(voteObj)
    })

    if (!response.ok) {
      throw new Error('Network response was not ok')
    }

    const data = await response.json()

    return data
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error)
    return {
      message: 'Error',
      status: 'failed'
    }
  }
}

export async function getPublicKey(jwtToken: string): Promise<getPublicKeyResponse> {
  try {
    const response = await fetch(`${BackendApiUrl}/get_pubkey`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${jwtToken}`,
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error('Network response was not ok')
    }

    const data: getPublicKeyResponse = await response.json()
    return data
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error)
    return {
      message: 'Error',
      key: {},
      code: 500,
      status: 'failed'
    } as getPublicKeyResponse // 返回一个默认的 VoteInfoResponse 对象
  }
}

/**
 * 获取投票结果
 * @param jwtToken JWT 令牌
 * @returns 投票结果响应
 */
export async function getVoteResult(jwtToken: string): Promise<VoteResultResponse> {
  try {
    const response = await fetch(`${BackendApiUrl}/get_vote_result`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${jwtToken}`,
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      const errorData = await response.json()
      const errorMessage = `Error: ${response.status} ${response.statusText} - ${errorData.message}`
      throw new Error(errorMessage)
    }

    const data: VoteResultResponse = await response.json()
    // 处理特殊情况
    for (const key in data.vote_obj) {
      if (data.vote_obj[key].result === 'No vote result') {
        const voteInfo = await getVoteInfo(jwtToken)
        const voteOptions = voteInfo.result.find((info) => info.vote_obj === key)?.list || []
        data.vote_obj[key].result = voteOptions.reduce(
          (acc: { [option: string]: number }, option: string) => {
            acc[option] = 0
            return acc
          },
          {}
        )
        data.vote_obj[key].vote_people_number = 0
      }
    }
    return data
  } catch (error) {
    console.error('获取投票结果失败:', error)
    return {
      status: 'failed',
      message: '获取投票结果失败',
      vote_obj: {}
    } as VoteResultResponse
  }
}
