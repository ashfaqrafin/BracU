from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import os
import random
import time

W, H = 800, 600

score = 0
over = False
paused = False
cheat = False

cx, cy = W // 2, 30
cw, ch = 40, 20
ccol = [1.0, 1.0, 1.0]
cspeed = 500.0

rd = 15
dx = random.randint(rd + 10, W - rd - 10)
dy = H - 50
base_v = 150.0
fall_v = base_v
dcol = [random.uniform(0.3, 1.0) for _ in range(3)]

last_t = 0.0


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def z(x1, y1, x2, y2):
    dx_, dy_ = x2 - x1, y2 - y1
    if abs(dx_) >= abs(dy_):
        if dx_ >= 0 and dy_ >= 0:
            return 0
        if dx_ < 0 and dy_ >= 0:
            return 3
        if dx_ < 0 and dy_ < 0:
            return 4
        return 7
    if dx_ >= 0 and dy_ >= 0:
        return 1
    if dx_ < 0 and dy_ >= 0:
        return 2
    if dx_ < 0 and dy_ < 0:
        return 5
    return 6


def to0(x, y, zone):
    if zone == 0:
        return x, y
    if zone == 1:
        return y, x
    if zone == 2:
        return y, -x
    if zone == 3:
        return -x, y
    if zone == 4:
        return -x, -y
    if zone == 5:
        return -y, -x
    if zone == 6:
        return -y, x
    return x, -y


def from0(x, y, zone):
    if zone == 0:
        return x, y
    if zone == 1:
        return y, x
    if zone == 2:
        return -y, x
    if zone == 3:
        return -x, y
    if zone == 4:
        return -x, -y
    if zone == 5:
        return -y, -x
    if zone == 6:
        return y, -x
    return x, -y


def line(x1, y1, x2, y2):
    x1, y1, x2, y2 = map(lambda v: int(round(v)), (x1, y1, x2, y2))
    if x1 == x2 and y1 == y2:
        glBegin(GL_POINTS)
        glVertex2f(x1, y1)
        glEnd()
        return

    zone = z(x1, y1, x2, y2)
    x1, y1 = to0(x1, y1, zone)
    x2, y2 = to0(x2, y2, zone)
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx_, dy_ = x2 - x1, y2 - y1
    d = 2 * dy_ - dx_
    e = 2 * dy_
    ne = 2 * (dy_ - dx_)

    y = y1
    glBegin(GL_POINTS)
    for x in range(x1, x2 + 1):
        px, py = from0(x, y, zone)
        glVertex2f(px, py)
        if d > 0:
            d += ne
            y += 1
        else:
            d += e
    glEnd()


def draw_catcher():
    glColor3f(*ccol)
    line(cx - cw, cy + ch, cx - cw + 10, cy)
    line(cx - cw + 10, cy, cx + cw - 10, cy)
    line(cx + cw - 10, cy, cx + cw, cy + ch)
    line(cx - cw, cy + ch, cx + cw, cy + ch)


def draw_diamond():
    glColor3f(*dcol)
    line(dx, dy + rd, dx + rd, dy)
    line(dx + rd, dy, dx, dy - rd)
    line(dx, dy - rd, dx - rd, dy)
    line(dx - rd, dy, dx, dy + rd)


def draw_ui():
    glColor3f(0.0, 0.8, 0.8)
    line(40, H - 40, 20, H - 50)
    line(20, H - 50, 40, H - 60)
    line(20, H - 50, 60, H - 50)

    glColor3f(1.0, 0.75, 0.0)
    if paused:
        line(W // 2 - 10, H - 40, W // 2 - 10, H - 60)
        line(W // 2 - 10, H - 40, W // 2 + 10, H - 50)
        line(W // 2 - 10, H - 60, W // 2 + 10, H - 50)
    else:
        line(W // 2 - 5, H - 40, W // 2 - 5, H - 60)
        line(W // 2 + 5, H - 40, W // 2 + 5, H - 60)

    glColor3f(1.0, 0.0, 0.0)
    line(W - 60, H - 40, W - 40, H - 60)
    line(W - 60, H - 60, W - 40, H - 40)


def spawn():
    global dx, dy, dcol, fall_v
    dx = random.randint(rd + 10, W - rd - 10)
    dy = H - 50
    dcol = [random.uniform(0.3, 1.0) for _ in range(3)]
    fall_v += 10.0


def hit():
    l1, r1, b1, t1 = cx - cw, cx + cw, cy, cy + ch
    l2, r2, b2, t2 = dx - rd, dx + rd, dy - rd, dy + rd
    return l1 < r2 and r1 > l2 and b1 < t2 and t1 > b2


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    draw_ui()
    draw_catcher()
    if not over:
        draw_diamond()
    glutSwapBuffers()


def step(now):
    global dy, score, over, ccol, cx
    dt = now - last_t
    if dt < 1e-3:
        return
    if paused or over:
        glutPostRedisplay()
        return

    if cheat:
        if cx < dx:
            cx = min(dx, cx + cspeed * dt)
        elif cx > dx:
            cx = max(dx, cx - cspeed * dt)
        cx = clamp(cx, cw, W - cw)

    dy -= fall_v * dt
    if dy < cy + ch:
        if hit():
            score += 1
            print(f"Score: {score}")
            spawn()
        elif dy < rd:
            over = True
            ccol = [1.0, 0.0, 0.0]
            print(f"Game Over. Last Score: {score}")

    glutPostRedisplay()


def idle():
    global last_t
    now = time.time()
    step(now)
    last_t = now


def key_sp(k, _x, _y):
    global cx
    if over or paused or cheat:
        return
    if k == GLUT_KEY_LEFT:
        cx -= 25
    elif k == GLUT_KEY_RIGHT:
        cx += 25
    cx = clamp(cx, cw, W - cw)
    glutPostRedisplay()


def key(ch_, _x, _y):
    global cheat
    if ch_ == b"c":
        cheat = not cheat
        print("Cheat Mode:", "ON" if cheat else "OFF")
    glutPostRedisplay()


def click(btn, state, x, y):
    global over, score, fall_v, ccol, paused
    if btn != GLUT_LEFT_BUTTON or state != GLUT_DOWN:
        return
    yy = H - y

    if 20 <= x <= 60 and H - 60 <= yy <= H - 40:
        print("Starting Over")
        score = 0
        over = False
        ccol = [1.0, 1.0, 1.0]
        fall_v = base_v
        paused = False
        spawn()
    elif W // 2 - 10 <= x <= W // 2 + 10 and H - 60 <= yy <= H - 40:
        if not over:
            paused = not paused
    elif W - 60 <= x <= W - 40 and H - 60 <= yy <= H - 40:
        print(f"Goodbye. Final Score: {score}")
        try:
            glutLeaveMainLoop()
        except Exception:
            pass
        os._exit(0)


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glViewport(0, 0, W, H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, W, 0, H, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glPointSize(2)


def main():
    global last_t
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(W, H)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Assignment 2")

    init()
    last_t = time.time()

    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutSpecialFunc(key_sp)
    glutKeyboardFunc(key)
    glutMouseFunc(click)
    glutMainLoop()


if __name__ == "__main__":
    main()
