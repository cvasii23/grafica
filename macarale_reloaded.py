# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import sys
import math
import numpy as np

global width
global height
global axrng
global l1, l2, a1, a2

width=800
height=500
axrng=400
a1=math.pi/4 #unghiul iniţial de rotaţie al primului brat
l1=187.5 #lungimea primului brat
a2=-math.pi/4 #unghiul de rotatie al celui de-al doilea brat
l2=197.5 # lungimea celui de-al doilea brat
def init():
    glClearColor(0.5, 1.0, 0.2, 1.0)
    gluOrtho2D(-axrng, axrng, -0.25*axrng, axrng)


def plotfunc():
    global l1,l2,a1,a2
    glClear(GL_COLOR_BUFFER_BIT)
   
  
    #aici desenez ceva
    glPushMatrix()
    glRotatef(math.degrees(a1), 0.0, 0.0, 1.0)
    glBegin(GL_QUADS)
    glColor3f(1.0, 0.7, 0.0)
    glVertex2f(-25,-30)
    glVertex2f(200,-30)
    glVertex2f(200,30)
    glVertex2f(-25,30)
    glEnd()
   
    glPushMatrix()
    glTranslatef(187.5, 0.0, 0.0)
    glRotatef(math.degrees(a2), 0.0, 0.0, 1.0)
    glTranslatef(-187.5, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.6, 0.0)
    glVertex2f(175,-30)
    glVertex2f(385,0)
    glVertex2f(175,30)
    glEnd()
    glPopMatrix()
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(187.5,0.0)
    deg2rad= 3.14159/180
    for i in range(360):
        deginrad=i*deg2rad
        glVertex2f(187.5+math.cos(deginrad)*10, math.sin(deginrad)*10)
    glEnd()
    glPopMatrix()

    glBegin(GL_TRIANGLE_FAN)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2i(0,0)
    deg2rad= 3.14159/180
    for i in range(360):
        deginrad=i*deg2rad
        glVertex2f(math.cos(deginrad)*10, math.sin(deginrad)*10)
    glEnd()
    
    glFlush()


def pozitie_noua(x,y):
    global a1, a2, l1, l2
    x1=x-400.0
    y1=400.0-y
    if l2-l1<=math.sqrt(x1**2+y1**2)<= l1+l2:
        c2=(x1**2+y1**2-l1**2-l2**2)/(2*l1*l2)
        s2=math.sqrt(c2**2)
        if x1<=0:
            a2=math.acos((x1**2+y1**2-l1**2-l2**2)/(2*l1*l2))
        else:
            a2=-math.acos((x1**2+y1**2-l1**2-l2**2)/(2*l1*l2))
        a1=math.acos((x1*(l1+l2*math.cos(a2))+y1*l2*math.sin(a2))/((l1+l2*math.cos(a2))**2+(l2*math.sin(a2))**2))
    else:
        a1=0.0
        a2=0.0
    glutPostRedisplay()

    
def keyboard(key, x, y):
    if key==chr(27):
        sys.exit()
    if key=='q':
        sys.exit()

def mouse(button,state, x,y):
    if button==GLUT_LEFT_BUTTON and state==GLUT_DOWN:
        glutIdleFunc(pozitie_noua(x,y))
    elif button==GLUT_MIDDLE_BUTTON or button==GLUT_RIGHT_BUTTON:
        if state==GLUT_DOWN:
            glutIdleFunc(None)


def main():
    global width
    global height

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB|GLUT_SINGLE)
    glutInitWindowPosition(100,50)
    glutInitWindowSize(width, height)
    glutCreateWindow("Fun with scara robot")
    glutDisplayFunc(plotfunc)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    init()
    glutMainLoop()

main()

