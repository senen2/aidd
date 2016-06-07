import numpy as np

dx, dT = 0.005, 0.1
k=200.0
cap=910.0
den=2700.0
alfa=k/(den*cap)
beta=alfa*dT/dx**2
potencia=10.0*.2/2e-4

T_old=np.zeros(100)
T_new=np.zeros(100)
T_matriz=np.zeros((200,100))

T_old[0]=50.0
T_new[0]=50.0
t=1.0
for t in range (1,100000,1):
    if t >= 50000:
        T_old[0] = T_old[1]
    else:
        T_old[0] = T_old[1]+potencia*dx/k
        
    for n in range (1,98,1):
        T_new[n] = T_old[n] + beta*(T_old[n-1] - 2*T_old[n] + T_old[n+1])
   
    if t%500==0:
        ti = t/500
        T_matriz[ti-1,:]=T_new
   
    T_old=T_new


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import rc
rc('mathtext', default='regular')

fig1 = plt.figure(1)
ax = fig1.gca(projection='3d')
x = np.arange(0, 200, 1.0)
y = np.arange(0, 100, 1.0)
X, Y = np.meshgrid(x, y)
zs = np.array([T_matriz[x,y] for x,y in zip(np.ravel(X), np.ravel(Y))])
Z =zs.reshape(X.shape)
ax.plot_surface(X, Y, Z, rstride=5, cstride=5, alpha=0.3)
#cset = ax.contourf(X, Y, Z, zdir='z', offset=0, cmap=cm.coolwarm)
#cset = ax.contourf(X, Y, Z, zdir='x', offset=0, cmap=cm.coolwarm)
cset = ax.contour(X, Y, Z, zdir='y', offset=150, cmap=cm.coolwarm)
ax.set_ylabel('Distancia')
ax.set_xlabel('Tiempo')
ax.set_zlabel('Terperatura')
ax.set_zlim(0,25)
ax.set_ylim(0,150)
plt.show()
