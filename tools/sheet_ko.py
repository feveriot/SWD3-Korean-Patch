import sys, os
from PIL import Image
X='x/en'; K='ko'; files=sorted(os.listdir(K)); pre=sys.argv[2:] 
if pre: files=[f for f in files if f.startswith(tuple(pre))]
tiles=[]
for f in files:
    a=Image.open(f'{X}/{f}').convert('RGBA'); b=Image.open(f'{K}/{f}').convert('RGBA')
    s=min(1,330/a.width); a=a.resize((int(a.width*s),int(a.height*s))); b=b.resize(a.size); tiles.append((a,b))
cols=2; cw=700; rows=[tiles[i:i+cols] for i in range(0,len(tiles),cols)]
H=sum(max(t[0].height for t in r)+6 for r in rows)
sh=Image.new('RGBA',(cw*cols,H),(70,70,70,255)); y=0
for r in rows:
    for j,(a,b) in enumerate(r): sh.alpha_composite(a,(j*cw,y)); sh.alpha_composite(b,(j*cw+340,y))
    y+=max(t[0].height for t in r)+6
sh.convert('RGB').save(sys.argv[1]); print(sh.size)
