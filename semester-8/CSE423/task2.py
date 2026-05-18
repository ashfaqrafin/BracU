from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W, H = 500, 500
L, R, B, T = -200, 200, -200, 200

pts = []
spd = 1.0

b_on = False
b_show = True
b_t = 0
frz = False

def world(mx, my):
    ww = glutGet(GLUT_WINDOW_WIDTH)
    hh = glutGet(GLUT_WINDOW_HEIGHT)
    return mx - ww/2, hh/2 - my

def in_box(x, y):
    return L<=x<=R and B<=y<=T

def pt(x,y,sz=6):
    glPointSize(sz)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()

def bdr():
    glColor3f(1, 1, 1)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(L,B); glVertex2f(R,B)
    glVertex2f(R,B); glVertex2f(R,T)
    glVertex2f(R,T); glVertex2f(L,T)
    glVertex2f(L,T); glVertex2f(L,B)
    glEnd()

def move():
    for p in pts:
        p[0] += p[2] * spd
        p[1] += p[3] * spd

        if p[0] <= L: p[0] = L; p[2] *= -1
        elif p[0] >= R: p[0] = R; p[2] *= -1

        if p[1] <= B: p[1] = B; p[3] *= -1
        elif p[1] >= T: p[1] = T; p[3] *= -1

def blink():
    global b_t, b_show
    if not b_on: return
    b_t += 1
    if b_t >= 20:
        b_t = 0
        b_show = not b_show

def proj():
    ww = glutGet(GLUT_WINDOW_WIDTH)
    hh = glutGet(GLUT_WINDOW_HEIGHT)
    glViewport(0, 0, ww, hh)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -250, 250, 0, 1)
    glMatrixMode(GL_MODELVIEW)

def show():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    proj()
    
    bdr()

    for p in pts:
        if b_on and (not b_show): glColor3f(0, 0, 0)
        else: glColor3f(p[4], p[5], p[6])
        pt(p[0], p[1], 6)

    glutSwapBuffers()

def idle():
    if not frz:
        move()
        blink()
    glutPostRedisplay()

def kb(key,x,y):
    global frz
    if key == b' ': frz = not frz
    glutPostRedisplay()

def sp(key,x,y):
    global spd
    if frz: return
    if key==GLUT_KEY_UP: spd *= 1.2
    elif key==GLUT_KEY_DOWN: spd = max(0.2, spd/1.2)
    glutPostRedisplay()

def ms(btn,st,x,y):
    global b_on, b_show, b_t

    if frz or st != GLUT_DOWN: return

    mod = glutGetModifiers()
    ctrl = (mod & GLUT_ACTIVE_CTRL) != 0

    wx, wy = world(x, y)

    l_act = (btn == GLUT_LEFT_BUTTON and not ctrl)
    r_act = (btn == GLUT_RIGHT_BUTTON) or (btn == GLUT_LEFT_BUTTON and ctrl)

    if l_act:
        b_on = not b_on
        b_show = True
        b_t = 0
        glutPostRedisplay()
        return

    if r_act and in_box(wx, wy):
        dx = random.choice([-1, 1])
        dy = random.choice([-1, 1])
        r = random.uniform(0.3, 1.0)
        g = random.uniform(0.3, 1.0)
        b = random.uniform(0.3, 1.0)
        pts.append([wx, wy, dx, dy, r, g, b])
        glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(W,H)
glutInitWindowPosition(100,100)
glutCreateWindow(b"Assignment1 Task2")
glutDisplayFunc(show)
glutIdleFunc(idle)
glutKeyboardFunc(kb)
glutSpecialFunc(sp)
glutMouseFunc(ms)
glutMainLoop()
