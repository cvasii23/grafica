import sys
try:
        from OpenGL.GL import *
        from OpenGL.GLUT import *
        from OpenGL.GLU import *
except ImportError:
        print "OpenGl nu e instalat ok"
        sys.exit(1)
import math
import numpy as np

varfuri_init=[]#asta va fi lista punctelor de control, o lista de liste
N=int(raw_input("Introduceti numarul punctelor de control:"))
DEG2RAD = 3.14159/(N-1)
for i in range(N):
        degInRad = i*DEG2RAD
        varfuri_init.append([math.cos(degInRad)*200, math.sin(degInRad)*200])
        #asezam la inceput punctele de control pe un semicerc, la lungimi egale de arc
b=np.array(varfuri_init)

def indice_min(a,b):
        distante=[]
        #lista distante calculeaza distanta de la punctul de coordonate
        #(a,b) la fiecare punct de control
        for i in range(len(varfuri_init)):
                distante.append(math.sqrt(((-400+a)-varfuri_init[i][0])**2+((480-b)-varfuri_init[i][1])**2))
        index=np.argmin(distante) # apoi alege indicele punctului de control care
                                  #e cel mai apropiat de punctul (a,b)
        return(index)

##def combinatie(varfuri,t):
##        puncte=[]
##        for i in range(0,len(varfuri)-1):
##                puncte.append(list((1-t)*np.array(varfuri[i])+t*np.array(varfuri[i+1])))
##        return puncte

##def punct_bezier(varfuri,t):
##        punct=[]
##        while (len(varfuri))>1:
##                
##                if len(varfuri)==1:
##                        punct=varfuri
##                else:
##                        varfuri=combinatie(varfuri,t)
##        return(punct)




def deCasteljau(t,b): #punctele de control b_0, b_1, ..., b_n, sunt date intr-un array 2D, 
                      #de n+1 linii si 2 coloane. Pe linia i avem coordonatele punctului b_i
                       
    a=np.copy(b) # se copiaza array-ul b in array-ul a
    N=a.shape[0] # interogam cat este numarul de linii ale lui a (deci si ale lui b); n=N-1
    for r in range(1,N): # echivalentul in C a lui for(r=1;r<N, r++)
        for i in range(N-r):# in C for(i=0; i<N-r;i++)
            a[i,:]=(1-t)*a[i,:]+t*a[i+1,:]# punctul i din etapa r este combinatia convexa 
                                          # apunctelor i si i+1 din etapa r-1
    return a[0,:]



def curbaBezier(b):   
    pcteC=[]
    for k in range(100):
        t=k*0.01# 0.01 este pasul de divizare a intervalului [0,1], al parametrului t
        P=deCasteljau(t,b)# P punct pe curba Bezier, corespunzator lui t
        pcteC.append(P)
    return pcteC# functia returneaza lista punctelor de pe curba calculate

varfuri_finale=curbaBezier(b)
##varfuri_finale=[]
##for k in range(1,100):
##        t= k/100
##        varfuri_finale.append(punct_bezier(varfuri_init,t))
##        k+=1
##        
##print(punct_bezier(combinatie(varfuri_init,1/2),1/2))
##print(varfuri_finale)

def initFun():
    glClearColor(1.0,0.9, 0.4, 0.0)
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(3.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-400.0, 400.0, -120.0, 480.0)
    glEnable(GL_DEPTH_TEST)
    

def displayFun():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)
    for l in varfuri_init:
        glVertex2f(l[0],l[1])
    glEnd()
    
    glBegin(GL_LINE_STRIP)
    glColor3f(0.0, 0.0, 0.0)
    for l in varfuri_init:
        glVertex2f(l[0],l[1])
    glEnd()
    
    glBegin(GL_LINE_STRIP)
    glColor3f(0.0, 1.0, 0.0)
    for n in varfuri_finale:
        glVertex2f(n[0],n[1])
    glEnd()
        
    glFlush()
    
def mouse(button, state, x, y):
   if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
          glutIdleFunc(punctnou(x,y))
   elif button == GLUT_MIDDLE_BUTTON or button == GLUT_RIGHT_BUTTON:
       if(state == GLUT_DOWN):
           glutIdleFunc(None)

def punctnou(x,y):
        global varfuri_finale
        varfuri_noi=varfuri_init
        varfuri_noi[indice_min(x,y)]=[-400+x,480-y]
        c=np.array(varfuri_noi)
        varfuri_finale=curbaBezier(c)
        glutPostRedisplay()

def keyboard(key,x,y):
    if key ==chr(27):
        sys.exit()
    if key =="q":
        sys.exit()


if __name__ == '__main__':
    glutInit()
    glutInitWindowSize(800,600)
    glutInitWindowPosition(300,50)
    glutCreateWindow("Curbe Bezier, poate")
    glutInitDisplayMode(GLUT_DEPTH | GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    initFun()
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    glutMainLoop()
