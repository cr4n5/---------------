// 生成一个在 [1, n-1] 范围内的随机大整数
export function randomBigInt(n: bigint): bigint {
  const byteLength = Math.ceil(n.toString(2).length / 8)
  let r: bigint
  do {
    const randomBytes = new Uint8Array(byteLength)
    crypto.getRandomValues(randomBytes)
    r = BigInt(
      '0x' +
        Array.from(randomBytes)
          .map((b) => b.toString(16).padStart(2, '0'))
          .join('')
    )
  } while (r >= n)
  return r
}
// 快速幂算法计算 (base ** exp) % mod
function modPow(base: bigint, exp: bigint, mod: bigint): bigint {
  let result = 1n
  base = base % mod
  while (exp > 0) {
    if (exp % 2n === 1n) {
      result = (result * base) % mod
    }
    exp = exp >> 1n
    base = (base * base) % mod
  }
  return result
}

// 加密函数
export function encrypt(pk: [bigint, bigint], m: bigint): bigint {
  const [n, g] = pk
  const r = randomBigInt(n - 1n) + 1n
  const n2 = n ** 2n
  const c = (modPow(g, m, n2) * modPow(r, n, n2)) % n2
  return c
}
