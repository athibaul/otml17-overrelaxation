import matplotlib.pyplot as plt

def normalize(x,y):
    n = (x**2+y**2)**.5
    return x/n,y/n

"""
Projects the point (gx,gy) onto the line passing through (0,0) with direction (dx,dy)
"""
def project(gx,gy,dx,dy):
    # Supposes that ||dx,dy|| = 1
    scal = gx*dx+gy*dy
    return scal*dx,scal*dy

alpha = 1.7
def overrelaxed(gx,gy,dx,dy,alpha):
    gx2,gy2 = project(gx,gy,dx,dy)
    return alpha*gx2+(1-alpha)*gx, alpha*gy2+(1-alpha)*gy

# gamma^epsilon = 0
# lines going out from it in directions :
x1,y1 = normalize(0,1)
x2,y2 = normalize(-0.4,1.5)


ax = plt.axes()
pict = "\\begin{tikzpicture}\n"
gx,gy = -0.5,4
ax.plot([gx],[gy],'o',color=(0.5,0,0.5),label="")
pict += "\\fill (%f,%f) circle (2pt) node[above] (gamma0) {$\\gamma^0$};\n" % (gx,gy)
pict += "\\fill (0,0) circle (2pt) node[right] {$\\gamma^*$};\n"
ax.text(gx,gy,"$\\gamma^0$",fontsize=25)
xx,yy = [],[]
pict += "\\draw[dashed] "
for _ in range(100):
    xx.append(gx)
    yy.append(gy)
    new_gx,new_gy = overrelaxed(gx,gy,x1,y1,alpha)
    pict += "(%f,%f) -- (%f,%f)\n" % (gx,gy,new_gx,new_gy)
    xx.append(new_gx)
    yy.append(new_gy)
    gx,gy = overrelaxed(new_gx,new_gy,x2,y2,alpha)
    pict += "(%f,%f) -- (%f,%f)\n" % (gx,gy,new_gx,new_gy)
pict += ";\n"

def constraint(x1,y1):
    cx,cy = [-5*x1,10*x1],[-5*y1,10*y1]
    maxy = max(yy)
    for i in range(2):
        if cy[i] > maxy:
            ratio = 1.1*maxy/cy[i]
            cy[i] *= ratio
            cx[i] *= ratio
        if cy[i] < -maxy:
            ratio = -0.1*maxy/cy[i]
            cy[i] *= ratio
            cx[i] *= ratio
    return cx,cy

c1x,c1y = constraint(x1,y1)
c2x,c2y = constraint(x2,y2)
c1_name = "$\mathcal{C}_1$"; c2_name = "$\mathcal{C}_2$"

ax.plot(xx,yy,'--',color=(0.5,0,0.5),label="$\\gamma^k$")
pict += "\draw (%f,%f) -- (%f,%f) node[right] {%s};\n" % (c1x[0],c1y[0],c1x[1],c1y[1],c1_name)
pict += "\draw (%f,%f) -- (%f,%f) node[right] {%s};\n" % (c2x[0],c2y[0],c2x[1],c2y[1],c2_name)
ax.plot(c1x,c1y,color='red',label=c1_name)
ax.plot(c2x,c2y,color='blue',label=c2_name)
ax.plot(gx,gy,'o',color=(0.5,0,0.5),label="")
ax.text(gx,gy,"$\\gamma^*$",fontsize=25)
ax.text(3*x1,3*y1,"$\mathcal{C}_1$",fontsize=25)
ax.text(4*x2,4*y2,"$\mathcal{C}_2$",fontsize=25)

ax.axis('equal')
ax.axis('off')
ax.set_xticks([])
ax.set_yticks([])
#plt.legend()
plt.show()


pict += "\\end{tikzpicture}"
outfile = open("schema.tex","w")
print(pict,file=outfile)
outfile.close()