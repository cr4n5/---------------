import { describe, it, expect } from 'vitest'
import { encrypt, randomBigInt } from './Paillier'
import { getPublicKey } from '@/api/fetchDataConsumer'
import { login } from '@/api/fetchDataConsumer'
import { submitVote } from '@/api/fetchThirdComputed'

describe('encrypt', () => {
  it('encrypts a message correctly', () => {
    const fakepublicKey: [bigint, bigint] = [
      BigInt(
        '7337557215804574661100506591219143022575346140804500100457434858552069798317598021570694631997824961647965705117388293133726874709252295791626820001863927'
      ),
      BigInt(
        '20847325372287666838785353400896933940691293758196339812281660371832223591677136829356671684289133614275841377211535144456946804516911613684996263348764230148913236373812773187361091565667451377387406144762635482424180918172346819296272468386811700901952701584627236915560060728299689056497443022562880083996'
      )
    ]

    const message = BigInt(123)
    console.log('message', message)
    const encryptedMessage = encrypt(fakepublicKey, message)
    console.log('encryptedMessage', encryptedMessage)
    expect(encryptedMessage).toBeDefined()
    expect(encryptedMessage).not.toBe(message)
  })

  it('can generate random', () => {
    const n = BigInt(123)
    console.log('n', n)
    const random = randomBigInt(n)
    console.log('random', random)
    expect(random).toBeDefined()
    expect(random).toBeLessThan(n)
  })

  it('can fetch public key', async () => {
    const token = await login('admin', 'admin')
    const publicKey = await getPublicKey(token)
    expect(publicKey).toBeDefined()
  })

  it('can submit vote', async () => {
    const token = await login('admin', 'admin')
    const publicKey = await getPublicKey(token)

    // 确保 publicKey['key']['a'] 是一个包含两个元素的数组
    const keyArray = publicKey['key']['a']

    if (keyArray.length !== 2) {
      throw new Error('Invalid public key format')
    }
    const pubkey: [bigint, bigint] = [BigInt(keyArray[0]), BigInt(keyArray[1])]
    const vote = {
      n: encrypt(pubkey, BigInt(1)),
      k: encrypt(pubkey, BigInt(2)),
      w: encrypt(pubkey, BigInt(3)),
      m: encrypt(pubkey, BigInt(4))
    }
    const response = await submitVote(token, {
      vote_obj: 'a',
      username: 'admin',
      vote,
      pubkey
    })
    console.log('response', response)
    expect(response).toBeDefined()
  })
})
