def power(number, n):
    if n == 0:
        return 1
    else:
        return power(number, n - 1) * number

def power1(number, n):
    res = 1
    for i in range(n):
        res = res * number
    return res

print(power(5,3))
print(power1(5,3))
print(5 ** 3)