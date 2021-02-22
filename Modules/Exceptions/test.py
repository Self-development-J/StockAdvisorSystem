import re

ppp = [1, 2, 3]

tar = "+000500"
p = re.compile("\w")

res = tar.lstrip("+").lstrip("0")

print(res)