const BackendApiUrl = import.meta.env.VITE_BACKEND_THIRD_COMPUTE_API_URL

// 本部分为interface定义

export interface SubmitVoteRequest {
  vote_obj: string
  username: string
  vote: {
    [item: string]: bigint
  }
  pubkey: [bigint, bigint]
}
export interface SubmitVoteResponse {
  status: string
  message: string
}

function bigIntToString(obj: any): any {
  if (typeof obj === 'bigint') {
    return obj.toString()
  } else if (Array.isArray(obj)) {
    return obj.map(bigIntToString)
  } else if (typeof obj === 'object' && obj !== null) {
    return Object.fromEntries(
      Object.entries(obj).map(([key, value]) => [key, bigIntToString(value)])
    )
  } else {
    return obj
  }
}

export async function submitVote(
  jwtToken: string,
  data: SubmitVoteRequest
): Promise<SubmitVoteResponse> {
  try {
    const response = await fetch(`${BackendApiUrl}/submit_vote`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${jwtToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(bigIntToString(data))
    })

    if (!response.ok) {
      const errorData = await response.json()
      const errorMessage = `Error: ${response.status} ${response.statusText} - ${errorData.message}`
      throw new Error(errorMessage)
    }

    const responseData: SubmitVoteResponse = await response.json()
    return responseData
  } catch (error) {
    console.error('提交投票失败:', error)
    return {
      status: 'failed',
      message: '提交投票失败'
    }
  }
}
interface restartVoteObj {
  vote_obj: string
}
export async function restartVoteThird(jwtToken: string, vote_obj: restartVoteObj) {
  try {
    const response = await fetch(`${BackendApiUrl}/restart`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${jwtToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(vote_obj)
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
