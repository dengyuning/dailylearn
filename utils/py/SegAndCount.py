import jieba
import json
import jieba
import sys
import pdb
from collections import Counter
import jieba.posseg as pseg
in_f = sys.argv[1]
out_f = sys.argv[2]
c = Counter()
with open(in_f,"r") as fr,open(out_f,"w") as fw:
	d = json.load(fr)
	for k in d:
		if "商品名称" in d[k]:
			name = d[k]["商品名称"]
			words =pseg.cut(name)
			for w in words:
				c[w.word+"_"+w.flag] += 1
		else:
			print(k)
	items = sorted(c.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
	for k in items:
		fw.write("{}	{}\n".format(k[0],k[1]))
