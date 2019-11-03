from random import randrange, getrandbits


def is_prime(n, k=128):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    print("\nPerforming Rabin Miller's Primality Test\n")
    for _ in range(k):
        a = randrange(2, n - 1)
        print("Selecting a random number a : ", a)
        x = pow(a, r, n)
        print("Calculating a=n(mod r) : ", x)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                print("Calculating x=n(mod 2) : ", x)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True


def generate_prime_candidate(length):
    p = getrandbits(length)
    p |= (1 << length - 1) | 1
    return p


def generate_prime_number(length):
    p = 4
    while not is_prime(p, 128):
        p = generate_prime_candidate(length)
        print("Generating a prime candidate : ", p)
    return p