"""Tải ô bản đồ OpenStreetMap cho một vùng và ghép thành ảnh nền.
python3 tiles.py <lat_min> <lon_min> <lat_max> <lon_max> <zoom> <out_dir>"""
import math,sys,json,time,urllib.request,io,os
from PIL import Image
la0,lo0,la1,lo1,z,out=float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),int(sys.argv[5]),sys.argv[6]
def tx(lon): return (lon+180)/360*2**z
def ty(lat): r=math.radians(lat); return (1-math.log(math.tan(r)+1/math.cos(r))/math.pi)/2*2**z
x0,x1=int(tx(lo0)),int(tx(lo1)); y0,y1=int(ty(la1)),int(ty(la0))
os.makedirs(out,exist_ok=True); cache=os.path.join(os.path.dirname(os.path.abspath(__file__)),".tilecache"); os.makedirs(cache,exist_ok=True)
img=Image.new('RGB',((x1-x0+1)*256,(y1-y0+1)*256))
for x in range(x0,x1+1):
    for y in range(y0,y1+1):
        f=f'{cache}/{z}_{x}_{y}.png'
        if not os.path.exists(f):
            req=urllib.request.Request(f'https://tile.openstreetmap.org/{z}/{x}/{y}.png',headers={'User-Agent':'trung-diem-bao-video/1.0 (map scenes)'})
            open(f,'wb').write(urllib.request.urlopen(req,timeout=30).read()); time.sleep(0.15)
        img.paste(Image.open(f).convert('RGB'),((x-x0)*256,(y-y0)*256))
img.save(f'{out}/map.png')
json.dump({'z':z,'x0':x0,'y0':y0,'w':img.width,'h':img.height},open(f'{out}/map.json','w'))
print('tiles',(x1-x0+1)*(y1-y0+1),'size',img.size)
