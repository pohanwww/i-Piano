import pickle
from rectangle import Rectangle

with open('temp/output.txt', 'rb') as fp:
    rec = pickle.load(fp)

for i in rec:
    print(i.y)
# print(rec)