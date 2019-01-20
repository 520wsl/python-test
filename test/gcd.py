def gcd(a, b):
    if a < b:
        a, b = b, a

    y = a % b

    if y == 0:
        return b
    else:
        a, b = b, y
    return gcd(a, b)


print(gcd(35, 100))
print(gcd(10, 100))
print(gcd(2, 100))
print(gcd(3, 100))
