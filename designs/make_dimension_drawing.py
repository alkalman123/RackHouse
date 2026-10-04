import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Rectangle
import rackhouse_designs as r
INK='#20232a'; ACC='#d85c2a'; BG='#f4f2ee'
prof=(r.rounded_rect(-28,40,28,58,5)+r.rounded_rect(-9,0,17,44,4)).offset(3).offset(-3)
fig,(a1,a2)=plt.subplots(1,2,figsize=(14,7),dpi=130,gridspec_kw={'width_ratios':[1,1.35]})
fig.patch.set_facecolor(BG)
for ax in (a1,a2): ax.set_aspect('equal'); ax.axis('off'); ax.set_facecolor(BG)
for poly in prof.to_polygons():
    a1.add_patch(Polygon(poly,closed=True,fc='#c9ced3',ec=INK,lw=2))
a1.add_patch(Circle((4,14),7,fc=BG,ec=INK,lw=2))
def dim(ax,p0,p1,label,off,horiz=True,color=INK):
    (x0,y0),(x1,y1)=p0,p1
    if horiz:
        y=off; ax.plot([x0,x0],[y0,y],color=color,lw=.8); ax.plot([x1,x1],[y1,y],color=color,lw=.8)
        ax.annotate('',(x0,y),(x1,y),arrowprops=dict(arrowstyle='<->',color=color,lw=1.4))
        ax.text((x0+x1)/2,y+1.6,label,ha='center',va='bottom',fontsize=13,fontweight='bold',color=color)
    else:
        x=off; ax.plot([x0,x],[y0,y0],color=color,lw=.8); ax.plot([x1,x],[y1,y1],color=color,lw=.8)
        ax.annotate('',(x,y0),(x,y1),arrowprops=dict(arrowstyle='<->',color=color,lw=1.4))
        ax.text(x+1.8,(y0+y1)/2,label,ha='left',va='center',fontsize=13,fontweight='bold',color=color,rotation=90)
dim(a1,(-28,58),(28,58),'56 mm',66)
dim(a1,(-28,40),(-9,40),'19 mm',30,color=ACC)
dim(a1,(17,40),(28,40),'11 mm',30,color=ACC)
dim(a1,(28,0),(28,58),'58 mm',34,horiz=False)
a1.annotate('Ø14 mm cord channel\n45° countersunk ends',(4,14),(-48,-14),fontsize=11,color=INK,
            arrowprops=dict(arrowstyle='->',color=INK,lw=1.1),ha='left')
a1.set_xlim(-50,46); a1.set_ylim(-22,78)
a1.set_title('END PROFILE',fontsize=13,fontweight='bold',color=INK,loc='left')
# side view
a2.add_patch(Rectangle((-50,40),100,18,fc='#c9ced3',ec=INK,lw=2))
a2.add_patch(Rectangle((-50,0),100,40,fc='#b4bac0',ec=INK,lw=2))
a2.plot([-50,50],[21,21],ls='--',color=INK,lw=.8); a2.plot([-50,50],[7,7],ls='--',color=INK,lw=.8)
dim(a2,(-50,58),(50,58),'100 mm',66)
a2.text(0,49,'RACKHOUSE',ha='center',va='center',fontsize=12,fontweight='bold',color='#6b737b')
a2.text(0,-12,'Pinch the 19 mm or 11 mm flange edge · hang weight from the channel',ha='center',fontsize=11,color=INK)
a2.set_xlim(-58,60); a2.set_ylim(-22,78)
a2.set_title('SIDE',fontsize=13,fontweight='bold',color=INK,loc='left')
fig.suptitle('Rock Ring V2 — edge lift block  ·  ~110 g printed (4 walls, 30% infill)',fontsize=16,fontweight='bold',color=INK,x=0.04,ha='left')
plt.savefig(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'img', 'rockring-dimensions.jpg'),facecolor=BG,bbox_inches='tight',pad_inches=0.3,pil_kwargs={'quality':90})
