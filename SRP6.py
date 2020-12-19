from random import randint
import hashlib
import string

def CheckPrime(N):
    
    small_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31,
                   37, 41, 43, 47, 53, 59, 61, 67, 71, 73,
                   79, 83, 89, 97, 101, 103, 107, 109, 113, 127,
                   131, 137, 139, 149, 151, 157, 163, 167, 173, 179,
                   181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251]

    for pr in small_primes:
            if N % pr == 0:
                return False

    n = N - 1

    s, d = 0, 0

    while True:
        if n % 2 == 0:
            n //= 2
            s += 1
        else:
            d = n
            n = N - 1
            break

        for i in range(5):

            a = randint(1, n)

            for j in range(s):
                test = pow(a, 2 ** j * d, N)
                if test == 1 or test == n:
                    return True

            return False

def GenPrimes():
    
    while True:
        q = randint(1999, 4999)
        N = 2 * q +1
        if CheckPrime(q) and CheckPrime(N):
            return N



def Generator(N):
    X = N - 1
    for x in range(1, X):
        for g in range(1, X):
            if pow(g, x, N) == X:
                return g

def GenHash(*args):
    a = ''.join(str(a) for a in args)
    return int(hashlib.sha256(a.encode('utf-8')).hexdigest(), 16)

def GenSalt():

    alphabet = string.ascii_letters + string.digits
    s = str()

    for i in range(10):
        s += alphabet[randint(0, 61)]

    return s

I = 'MyName'
p = 'qwerty12345'

N = GenPrimes()
print("N =", N)

g = Generator(N)
print("g =", g)

k = GenHash(N, g)
print("k =", k)

s = GenSalt()
print("s =", s)

x = GenHash(s, p)
print("x =", x)

v = pow(g, x, N)
print("v =", v)

a = randint(100, 500)
A = pow(g, a, N)

while A == 0:
    a = randint(100, 500)
    A = pow(g, a, N)

print("a = ", a, ", A = ", A, sep = '')

b = randint(100, 500)
B = (k*v + pow(g, b, N)) % N

while B == 0:
    b = randint(100, 500)
    B = (k*v + pow(g, b, N)) % N

print("b = ", b, ", B = ", B, sep = '')

u = GenHash(A, B)
if u == 0:
    print("Прерывание соединения")
    quit()

print(u)

Client_S = pow(B - k * pow(g, x, N), a + u * x, N)
Client_K = GenHash(Client_S)

print("S(Client side) = ", Client_S, ", K(Client side) = ", Client_K, sep = '')

Server_S = pow(A * pow(v, u, N), b, N)
Server_K = GenHash(Server_S)

print("S(Server side) = ", Server_S, ", K(Server side) = ", Server_K, sep = '')

if Client_K == Server_K:

    Client_M = GenHash(GenHash(N) ^ GenHash(g), GenHash(I), s, A, B, Client_K)
    Server_M = GenHash(GenHash(N) ^ GenHash(g), GenHash(I), s, A, B, Server_K)

    print("M(Client side) = ", Client_M, ", M(Server side) = ", Server_M, sep = '')

    if Client_M == Server_M:
        Server_R = GenHash(A, Server_M, Server_K)
        Client_R = GenHash(A, Client_M, Client_K)

        print("R(Client side) = ", Client_R, ", R(Server side) = ", Server_R, sep = '')

        if Server_R == Client_R:
            print("Аутентификация прошла успешно")
        else:
            print("Сервер не подтвердил свою подлинность")

    else:
        print("Клиент не подтвердил свою подлинность")

else:
    print("Клиент и/или сервер не являются подлинными")