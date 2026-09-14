L = 100
D = [5]
W = 1
H = 1
print(D,type(D[0]))
scale = 10000/L
D = [d * scale for d in D]
W,H = W,H * scale
size = tuple(dim for dim in (sum(D), W, H))

print(size)
