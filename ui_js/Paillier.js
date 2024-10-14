"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.encrypt = encrypt;
// 生成一个在 [1, n-1] 范围内的随机大整数
function randomBigInt(n) {
    const byteLength = Math.ceil(n.toString(2).length / 8);
    let r;
    do {
        const randomBytes = new Uint8Array(byteLength);
        crypto.getRandomValues(randomBytes);
        r = BigInt('0x' +
            Array.from(randomBytes)
                .map((b) => b.toString(16).padStart(2, '0'))
                .join(''));
    } while (r >= n);
    return r;
}
// 快速幂算法计算 (base ** exp) % mod
function modPow(base, exp, mod) {
    let result = 1n;
    base = base % mod;
    while (exp > 0) {
        if (exp % 2n === 1n) {
            result = (result * base) % mod;
        }
        exp = exp >> 1n;
        base = (base * base) % mod;
    }
    return result;
}
// 加密函数
function encrypt(pk, m) {
    const [n, g] = pk;
    const r = randomBigInt(n - 1n) + 1n;
    const n2 = n ** 2n;
    const c = (modPow(g, m, n2) * modPow(r, n, n2)) % n2;
    return c;
}
// 示例使用
const publicKey = [BigInt('9292770072280002632872384766929534187704042406374927299421759497484867499398448709157541684874762332977442863512477087398283677218674298619842062068118713'), BigInt('15358756879889351578838625081596159635274139051861385797559489777439838291132907758243816265063412349701422197035171747363819013261112999252404469915446046185826640108460741874088520082898327915390410786727896843993564847109934874886947930388392882621797849835302209575609304274087327679322157387232981713937')];
const privateKey = [BigInt('4646385036140001316436192383464767093852021203187463649710879748742433749699127697383300203735056451044517707604817329375971485031963258310218181207526330'), BigInt('9271238385347014366247444470431759667446553307784074467263031788936248959877164780962817948330019336977554741633769585314194085215345022139428862935862515')];
const m1 = 42n;
const c1 = encrypt(publicKey, m1);
// const decryptedM1 = decrypt(privateKey, publicKey, c1);
console.log(`Original message: ${m1}`);
console.log(`Encrypted message: ${c1}`);
// console.log(`Decrypted message: ${decryptedM1}`);
