# Task-1
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W, H = 800, 600
bg = 0.0
bend = 0
spd = 3
drops = []

def mk_drops():
    global drops
    drops = []
    for i in range(200):
        x = random.randint(0, W)
        y = random.randint(0, H)
        drops.append([x, y])

def tri(x1,y1,x2,y2,x3,y3):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1,y1); glVertex2f(x2,y2); glVertex2f(x3,y3)
    glEnd()

def rect(x,y,w,h):
    glBegin(GL_TRIANGLES)
    glVertex2f(x,y); glVertex2f(x+w,y); glVertex2f(x+w,y+h)
    glVertex2f(x,y); glVertex2f(x+w,y+h); glVertex2f(x,y+h)
    glEnd()

def ln(x1,y1,x2,y2):
    glBegin(GL_LINES)
    glVertex2f(x1,y1); glVertex2f(x2,y2)
    glEnd()

def pt(x,y,sz):
    glPointSize(sz)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()

def sky():
    glColor3f(bg*0.53, bg*0.81, bg*0.92)
    rect(0,0,W,H)

def ground():
    s = 0.3+0.7*bg
    glColor3f(0.55*s, 0.35*s, 0.05*s)
    rect(0,0,W,200)

def trees():
    s = 0.3+0.7*bg
    for x in range(0,W,50):
        if 280<x<560: continue
        glColor3f(0, 0.8*s, 0)
        tri(x,200, x+30,200, x+15,240)

def win(x,y,w,h):
    s = 0.3+0.7*bg
    glColor3f(0.3*s, 0.7*s, 1.0*s)
    rect(x,y,w,h)
    glColor3f(0.1,0.1,0.3)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(x,y+h/2); glVertex2f(x+w,y+h/2)
    glVertex2f(x+w/2,y); glVertex2f(x+w/2,y+h)
    glVertex2f(x,y); glVertex2f(x+w,y)
    glVertex2f(x+w,y); glVertex2f(x+w,y+h)
    glVertex2f(x+w,y+h); glVertex2f(x,y+h)
    glVertex2f(x,y+h); glVertex2f(x,y)
    glEnd()

def house():
    s = 0.3+0.7*bg
    lx,rx = 300,550
    by,ty = 190,350
    mx = (lx+rx)/2

    # walls
    glColor3f(0.96*s, 0.91*s, 0.76*s)
    rect(lx,by,rx-lx,ty-by)

    # roof
    glColor3f(0.4*s, 0.2*s, 0.8*s)
    tri(lx-30,ty, rx+30,ty, mx,ty+100)

    # door
    dw,dh = 30,60
    glColor3f(0, 0.5*s, 1.0*s)
    rect(mx-dw/2, by, dw, dh)
    glColor3f(1,1,1)
    pt(mx+dw/2-6, by+dh/2, 4)

    # windows
    win(lx+25, by+55, 50, 50)
    win(rx-75, by+55, 50, 50)

def rain():
    if bg>0.5: glColor3f(0,0,0.8)
    else: glColor3f(0.4,0.7,1.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    for d in drops:
        glVertex2f(d[0], d[1])
        glVertex2f(d[0]+bend*2, d[1]-15)
    glEnd()

def move_rain():
    drift = bend*(H/spd)
    lo = min(0, -drift)-100
    hi = max(W, W-drift)+100
    for d in drops:
        d[1] -= spd
        d[0] += bend
        if d[1]<0 or d[0]<lo or d[0]>hi:
            d[1] = H+random.randint(0,50)
            a = min(0,-drift)
            b = max(W, W-drift)
            d[0] = random.uniform(a,b)

def proj():
    glViewport(0,0,W,H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0,W,0,H,0,1)
    glMatrixMode(GL_MODELVIEW)

def show():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    proj()
    sky(); ground(); trees(); house(); rain()
    glutSwapBuffers()

def idle():
    move_rain()
    glutPostRedisplay()

def kb(key,x,y):
    global bg
    if key in [b'd',b'D']: bg = min(1.0, bg+0.05)
    elif key in [b'n',b'N']: bg = max(0.0, bg-0.05)
    glutPostRedisplay()

def sp(key,x,y):
    global bend
    if key==GLUT_KEY_LEFT: bend -= 0.3
    elif key==GLUT_KEY_RIGHT: bend += 0.3
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(W,H)
glutInitWindowPosition(100,100)
glutCreateWindow(b"Assignment1 Task1")
mk_drops()
glutDisplayFunc(show)
glutIdleFunc(idle)
glutKeyboardFunc(kb)
glutSpecialFunc(sp)
glutMainLoop()
# Task-1