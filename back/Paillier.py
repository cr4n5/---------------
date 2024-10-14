import random
from math import gcd
from sympy import mod_inverse
from Crypto.Util.number import getPrime
import json

def lcm(x, y):
    return x * y // gcd(x, y)

def generate_keypair(bits):
    p = getPrime(bits)
    q = getPrime(bits)
    n = p * q
    λ = lcm(p-1, q-1)
    g = random.randint(1, n**2)
    μ = mod_inverse(L(pow(g, λ, n**2), n), n)
    return (n, g), (λ, μ)

def L(u, n):
    return (u - 1) // n

def encrypt(pk, m):
    n, g = pk
    r = random.randint(1, n-1)
    c = (pow(g, m, n**2) * pow(r, n, n**2)) % n**2
    return c

def decrypt(sk, pk, c):
    if type(c) == str:
        c = int(c)
    n, g = pk
    λ, μ = sk
    u = pow(c, λ, n**2)
    l = L(u, n)
    m = (l * μ) % n
    return m

def homomorphic_addition(pk, c1, c2):
    n, g = pk
    # 判断pk，c1，c2是否为str
    if type(c1) == str:
        c1 = int(c1)
    if type(c2) == str:
        c2 = int(c2)
    if type(n) == str:
        n = int(n)
    if type(g) == str:
        g = int(g)

    return (c1 * c2) % n**2

def save_keypair(path,bits=256):
    public_key, private_key = generate_keypair(bits)
    with open(path, 'w') as f:
        json.dump({'public_key': public_key, 'private_key': private_key}, f)


if __name__ == "__main__":
    save_keypair()

    # bits = 256
    # public_key, private_key = generate_keypair(bits)
    # print(public_key)
    # print(private_key)
    # m1 = 0
    # m2 = 42
    # m3 = 100

    # c1 = encrypt(public_key, m1)
    # print(c1)
    # c2 = encrypt(public_key, m2)
    # print(c2)
    # c3 = encrypt(public_key, m3)

    # c_sum = homomorphic_addition(public_key, c1, c2)
    # c_sum = homomorphic_addition(public_key, c_sum, c3)
    # m_sum = decrypt(private_key, public_key, c_sum)

    # m1_decrypted = decrypt(private_key, public_key, c1)

    # print(f"m1: {m1}, m2: {m2}")
    # print(f"m1 + m2: {m_sum}")
    # print(f"Decrypted m1: {m1_decrypted}")