a = 3
a *=2

print(a)

b = [
    {'amount': 1},
    {'amount': 2},
    {'amount': 3},
    {'amount': 4},
    {'amount': 5}
]

k = [1, 2, 3, 4, 5]

c = sum(item['amount'] for item in b)
print(c)
print(sum(k))