import re


test = '001'
test1 = '002-3_pcs'

print(re.findall(r'\d{3}-(\d+)_pcs', test1))
