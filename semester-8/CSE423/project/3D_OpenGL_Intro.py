from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Window / world settings
WINDOW_W = 1000
WINDOW_H = 800
fovY = 75
GRID_LENGTH = 700

# Simple fall physics
GRAVITY = 9.8
FREEFALL_DRAG = 0.18
PARACHUTE_DRAG = 1.35

# More streamlined head-down dive
DIVE_DRAG = 0.10

# Archery-style landing target (10 rings)
TARGET_CENTER_X = 0.0
TARGET_CENTER_Y = 0.0
TARGET_INNER_RADIUS = 40.0
TARGET_RING_STEP = 20.0
TARGET_RING_COUNT = 10
TARGET_OUTER_RADIUS = TARGET_INNER_RADIUS + TARGET_RING_STEP * (TARGET_RING_COUNT - 1)

# Skydiver gameplay state
start_altitude = 1500.0
player_x = 0.0
player_y = 0.0
player_z = start_altitude
vx = 0.0
vy = 0.0
fall_speed = 0.0

parachute_deployed = False
parachute_open_progress = 0.0
diving = False
dive_progress = 0.0
wind_on = True
wind_vec = (5.0, 2.0)

camera_mode = 0  # 0: follow, 1: top-down, 2: free
free_cam_pos = [300.0, -500.0, 500.0]

game_status = "FREEFALL"
outcome_text = ""
score = 0
jump_started = False
camera_follow = [0.0, 0.0, start_altitude + 120.0]
last_impact_speed = 0.0

# Plane state
plane_x = -260.0
plane_y = -260.0
plane_z = start_altitude + 40.0

# Continuous arrow-key control
active_special_keys = set()

# Deterministic star field
random.seed(423)
stars = []
for _ in range(70):
    stars.append((random.uniform(-900, 900), random.uniform(-900, 900), random.uniform(1650, 1820)))

world_time = 0.0


def clamp(v, lo, hi):
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v


def lerp(a, b, t):
    return a + (b - a) * t


def reset_game():
    global player_x, player_y, player_z, vx, vy, fall_speed
    global parachute_deployed, parachute_open_progress, wind_on, camera_mode
    global diving, dive_progress
    global game_status, outcome_text, score, last_impact_speed
    global plane_x, plane_y, plane_z
    global active_special_keys, jump_started, camera_follow
    global world_time

    player_x = 0.0
    player_y = 0.0
    player_z = start_altitude
    vx = 0.0
    vy = 0.0
    fall_speed = 0.0

    parachute_deployed = False
    parachute_open_progress = 0.0
    diving = False
    dive_progress = 0.0
    wind_on = True
    camera_mode = 0
    jump_started = False

    game_status = "ON PLANE"
    outcome_text = ""
    score = 0
    last_impact_speed = 0.0

    plane_x = -260.0
    plane_y = -260.0
    plane_z = start_altitude + 40.0
    camera_follow = [0.0, 0.0, start_altitude + 120.0]

    active_special_keys = set()
    world_time = 0.0


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, color=(1, 1, 1)):
    glColor3f(color[0], color[1], color[2])
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, WINDOW_W, 0, WINDOW_H)  # left, right, bottom, top

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_sky_gradient_overlay():
    # 2D background gradient: darker sky at top, lighter near ground
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_W, 0, WINDOW_H)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # t = 1.0 at high altitude (deeper sky), 0.0 at ground (lighter sky)
    t = clamp(player_z / start_altitude, 0.0, 1.0)

    top_deep = (0.03, 0.06, 0.25)
    top_light = (0.25, 0.55, 0.95)
    bot_deep = (0.08, 0.18, 0.55)
    bot_light = (0.65, 0.90, 1.00)

    top = (
        lerp(top_light[0], top_deep[0], t),
        lerp(top_light[1], top_deep[1], t),
        lerp(top_light[2], top_deep[2], t),
    )
    bot = (
        lerp(bot_light[0], bot_deep[0], t),
        lerp(bot_light[1], bot_deep[1], t),
        lerp(bot_light[2], bot_deep[2], t),
    )

    glBegin(GL_QUADS)
    glColor3f(bot[0], bot[1], bot[2])
    glVertex2f(0, 0)
    glVertex2f(WINDOW_W, 0)
    glColor3f(top[0], top[1], top[2])
    glVertex2f(WINDOW_W, WINDOW_H)
    glVertex2f(0, WINDOW_H)
    glEnd()

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)


def draw_stars_and_sun():
    # Stars at very high altitude
    t = clamp(player_z / start_altitude, 0.0, 1.0)
    star_brightness = clamp((t - 0.55) / 0.45, 0.0, 1.0)
    if star_brightness > 0.01:
        glPointSize(2.0)
        glBegin(GL_POINTS)
        glColor3f(star_brightness, star_brightness, star_brightness)
        for sx, sy, sz in stars:
            glVertex3f(sx, sy, sz)
        glEnd()

    # Distant sun
    glPushMatrix()
    glTranslatef(780, -780, 1150)
    glColor3f(1.0, 0.85, 0.2)
    glutSolidSphere(70, 16, 16)
    glPopMatrix()


def draw_cloud(cx, cy, cz, alpha=0.55, scale=1.0):
    glColor4f(1.0, 1.0, 1.0, alpha)
    glPushMatrix()
    glTranslatef(cx, cy, cz)
    glScalef(scale, scale, scale)
    glutSolidSphere(28, 12, 12)
    glTranslatef(35, 5, 5)
    glutSolidSphere(24, 12, 12)
    glTranslatef(-70, -2, -2)
    glutSolidSphere(22, 12, 12)
    glPopMatrix()


def draw_clouds():
    glDepthMask(GL_FALSE)
    cloud_positions = [
        (-380, 250, 1100),
        (270, -180, 900),
        (520, 360, 700),
        (-520, -420, 580),
        (120, 480, 450),
    ]
    # Soft moving clouds
    for i, (cx, cy, cz) in enumerate(cloud_positions):
        dx = math.sin(world_time * 0.18 + i) * 28
        dy = math.cos(world_time * 0.14 + i * 1.7) * 18
        a = 0.42 + (i % 3) * 0.08
        s = 0.95 + (i % 4) * 0.06
        draw_cloud(cx + dx, cy + dy, cz, alpha=a, scale=s)
    glDepthMask(GL_TRUE)


def draw_player_ground_marker():
    # Shows where you are above the ground (makes drift obvious).
    glLineWidth(2.0)
    glPushMatrix()
    glTranslatef(player_x, player_y, 1.2)
    glColor3f(1.0, 0.95, 0.25)
    size = 28
    glBegin(GL_LINES)
    glVertex3f(-size, 0, 0)
    glVertex3f(size, 0, 0)
    glVertex3f(0, -size, 0)
    glVertex3f(0, size, 0)
    glEnd()

    glColor3f(0.95, 0.65, 0.12)
    glBegin(GL_LINE_LOOP)
    for a in range(0, 360, 20):
        r = 18
        rad = math.radians(a)
        glVertex3f(math.cos(rad) * r, math.sin(rad) * r, 0)
    glEnd()
    glPopMatrix()
    glLineWidth(1.0)


def draw_jump_marker():
    glPushMatrix()
    glTranslatef(-120, -120, plane_z - 30)
    glColor3f(1.0, 1.0, 0.2)
    glutSolidCone(18, 48, 10, 2)
    glPopMatrix()


def draw_checkered_ground():
    step = 120
    for ix in range(-GRID_LENGTH, GRID_LENGTH, step):
        for iy in range(-GRID_LENGTH, GRID_LENGTH, step):
            c = ((ix // step) + (iy // step)) % 2
            if c == 0:
                glColor3f(0.18, 0.45, 0.18)
            else:
                glColor3f(0.12, 0.33, 0.12)
            glBegin(GL_QUADS)
            glVertex3f(ix, iy, 0)
            glVertex3f(ix + step, iy, 0)
            glVertex3f(ix + step, iy + step, 0)
            glVertex3f(ix, iy + step, 0)
            glEnd()


def draw_landing_target():
    # Archery-style target board (colored rings)
    # NOTE: Draw as non-overlapping ring strips to avoid z-fighting/shimmer
    # (the old approach stacked filled circles at the same depth).

    def ring_color(score):
        # 10-9 yellow, 8-7 red, 6-5 blue, 4-3 black, 2-1 white
        if score >= 9:
            return (1.0, 0.92, 0.12)
        if score >= 7:
            return (0.95, 0.15, 0.12)
        if score >= 5:
            return (0.15, 0.35, 0.95)
        if score >= 3:
            return (0.08, 0.08, 0.08)
        return (0.95, 0.95, 0.95)

    def filled_circle(radius, color, z=0.0):
        glColor3f(color[0], color[1], color[2])
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, z)
        for a in range(0, 361, 8):
            rad = math.radians(a)
            glVertex3f(math.cos(rad) * radius, math.sin(rad) * radius, z)
        glEnd()

    def ring_strip(inner_r, outer_r, color, z=0.0):
        glColor3f(color[0], color[1], color[2])
        glBegin(GL_TRIANGLE_STRIP)
        for a in range(0, 361, 8):
            rad = math.radians(a)
            ca = math.cos(rad)
            sa = math.sin(rad)
            glVertex3f(ca * outer_r, sa * outer_r, z)
            glVertex3f(ca * inner_r, sa * inner_r, z)
        glEnd()

    def circle_outline(radius, color=(0, 0, 0)):
        glColor3f(color[0], color[1], color[2])
        glBegin(GL_LINE_LOOP)
        for a in range(0, 360, 10):
            rad = math.radians(a)
            glVertex3f(math.cos(rad) * radius, math.sin(rad) * radius, 0)
        glEnd()

    glPushMatrix()
    # Slightly above ground to avoid depth fighting with the checkered floor.
    glTranslatef(TARGET_CENTER_X, TARGET_CENTER_Y, 0.15)

    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(-1.0, -1.0)

    # Bullseye (10)
    filled_circle(TARGET_INNER_RADIUS, ring_color(10), z=0.0)

    # Rings outward (9..1) as non-overlapping strips
    for i in range(TARGET_RING_COUNT - 1):
        points = TARGET_RING_COUNT - (i + 1)
        r0 = TARGET_INNER_RADIUS + TARGET_RING_STEP * i
        r1 = TARGET_INNER_RADIUS + TARGET_RING_STEP * (i + 1)
        ring_strip(r0, r1, ring_color(points), z=0.0)

    glDisable(GL_POLYGON_OFFSET_FILL)

    # Ring boundaries
    glLineWidth(2.0)
    glDisable(GL_DEPTH_TEST)
    for i in range(TARGET_RING_COUNT):
        r = TARGET_INNER_RADIUS + TARGET_RING_STEP * i
        # White outline on black rings so it stays visible
        outline_c = (1, 1, 1) if (3 <= (TARGET_RING_COUNT - i) <= 4) else (0, 0, 0)
        circle_outline(r, outline_c)

    # Center dot
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.08)
    glutSolidSphere(2.3, 10, 10)
    glPopMatrix()
    glEnable(GL_DEPTH_TEST)
    glLineWidth(1.0)
    glPopMatrix()


def draw_tree(tx, ty):
    quad = gluNewQuadric()
    # trunk
    glPushMatrix()
    glTranslatef(tx, ty, 0)
    glColor3f(0.45, 0.28, 0.1)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quad, 8, 8, 45, 8, 1)
    glPopMatrix()

    # leaves
    glPushMatrix()
    glTranslatef(tx, ty, 62)
    glColor3f(0.05, 0.45, 0.1)
    glutSolidSphere(24, 12, 12)
    glPopMatrix()


def draw_trees():
    positions = [
        (-620, -620),
        (-620, 620),
        (620, -620),
        (620, 620),
        (-620, 0),
        (620, 0),
        (0, -620),
        (0, 620),
    ]
    for tx, ty in positions:
        draw_tree(tx, ty)


def draw_plane():
    glPushMatrix()
    glTranslatef(plane_x, plane_y, plane_z)

    # Face the direction the plane is moving
    heading = math.degrees(math.atan2(24.0, 90.0))
    glRotatef(heading, 0, 0, 1)
    glRotatef(-8, 1, 0, 0)
    glScalef(1.7, 1.7, 1.7)

    # Main fuselage
    glColor3f(0.86, 0.86, 0.90)
    glPushMatrix()
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 11, 11, 90, 12, 2)
    glPopMatrix()

    # Nose and tail
    glColor3f(0.82, 0.82, 0.86)
    glPushMatrix()
    glTranslatef(48, 0, 0)
    glRotatef(90, 0, 1, 0)
    glutSolidCone(11, 16, 12, 2)
    glPopMatrix()

    glColor3f(0.62, 0.62, 0.66)
    glPushMatrix()
    glTranslatef(-44, 0, 0)
    glRotatef(90, 0, 1, 0)
    glutSolidCone(8, 16, 10, 2)
    glPopMatrix()

    # Wings
    glColor3f(0.90, 0.22, 0.18)
    glPushMatrix()
    glTranslatef(0, 0, -2)
    glScalef(2.6, 0.20, 0.55)
    glutSolidCube(28)
    glPopMatrix()

    # Tail wing
    glPushMatrix()
    glTranslatef(-30, 0, 14)
    glScalef(0.45, 0.15, 0.30)
    glutSolidCube(24)
    glPopMatrix()

    # Vertical tail fin
    glColor3f(0.90, 0.22, 0.18)
    glPushMatrix()
    glTranslatef(-36, 0, 26)
    glScalef(0.10, 0.45, 0.55)
    glutSolidCube(30)
    glPopMatrix()

    # Window strip
    glColor3f(0.18, 0.25, 0.40)
    glPushMatrix()
    glTranslatef(-6, 0, 6)
    glScalef(1.3, 0.12, 0.18)
    glutSolidCube(24)
    glPopMatrix()

    # Small engine pods to make the shape easier to read
    glColor3f(0.55, 0.55, 0.58)
    for wing_side in (-1, 1):
        glPushMatrix()
        glTranslatef(8, wing_side * 14, -11)
        glScalef(0.35, 0.65, 0.35)
        glutSolidCube(16)
        glPopMatrix()

    # Cockpit bubble
    glColor4f(0.20, 0.35, 0.55, 0.55)
    glPushMatrix()
    glTranslatef(26, 0, 10)
    glScalef(1.1, 0.75, 0.65)
    glutSolidSphere(10, 14, 14)
    glPopMatrix()

    glPopMatrix()


def draw_drift_indicator():
    if not jump_started:
        return

    glLineWidth(2.0)

    # Actual movement vector (velocity + wind)
    mx = vx + (wind_vec[0] if wind_on else 0.0)
    my = vy + (wind_vec[1] if wind_on else 0.0)
    mlen = math.sqrt(mx * mx + my * my)
    if mlen < 0.001:
        mlen = 0.001
    arrow_len = min(160.0, mlen * 1.2)
    af = arrow_len / mlen
    glColor3f(1.0, 1.0, 0.12)
    glBegin(GL_LINES)
    glVertex3f(player_x, player_y, player_z)
    glVertex3f(player_x + mx * af, player_y + my * af, player_z + 30)
    glEnd()

    # Wind vector (cyan)
    if wind_on:
        glColor3f(0.25, 0.9, 1.0)
        glBegin(GL_LINES)
        glVertex3f(player_x, player_y, player_z + 10)
        glVertex3f(player_x + wind_vec[0] * 6.0, player_y + wind_vec[1] * 6.0, player_z + 10)
        glEnd()

    # Input direction (green) when arrows are pressed
    ix = 0
    iy = 0
    if GLUT_KEY_LEFT in active_special_keys:
        ix -= 1
    if GLUT_KEY_RIGHT in active_special_keys:
        ix += 1
    if GLUT_KEY_UP in active_special_keys:
        iy += 1
    if GLUT_KEY_DOWN in active_special_keys:
        iy -= 1
    if ix != 0 or iy != 0:
        glColor3f(0.25, 1.0, 0.35)
        glBegin(GL_LINES)
        glVertex3f(player_x, player_y, player_z + 20)
        glVertex3f(player_x + ix * 55, player_y + iy * 55, player_z + 20)
        glEnd()

    glLineWidth(1.0)


def draw_skydiver():
    # Lean according to drift velocity
    if parachute_deployed:
        lean_scale = 0.55
    else:
        lean_scale = lerp(1.0, 0.45, dive_progress)
    lean_x = max(-18, min(18, -vy * 4.0 * lean_scale))
    lean_y = max(-18, min(18, vx * 4.0 * lean_scale))

    glPushMatrix()
    glTranslatef(player_x, player_y, player_z)

    # Smooth flip into head-down dive (freefall only)
    if (not parachute_deployed) and dive_progress > 0.001:
        glRotatef(-180.0 * dive_progress, 1, 0, 0)

    glRotatef(lean_x, 1, 0, 0)
    glRotatef(lean_y, 0, 1, 0)

    # Body pose differs before/after parachute deployment
    if parachute_deployed:
        body_tilt = -2
    else:
        body_tilt = lerp(15.0, 0.0, dive_progress)
    glRotatef(body_tilt, 1, 0, 0)

    # body
    glColor3f(0.25, 0.3, 0.85)
    glPushMatrix()
    glScalef(0.6, 0.35, 1.0)
    glutSolidCube(30)
    glPopMatrix()

    # head
    glColor3f(1.0, 0.84, 0.68)
    glPushMatrix()
    glTranslatef(0, 0, 28)
    glutSolidSphere(9, 12, 12)
    glPopMatrix()

    # arms
    glColor3f(0.95, 0.7, 0.15)
    if parachute_deployed:
        arm_ang = 95.0
    else:
        # tuck arms slightly in a dive
        arm_ang = lerp(55.0, 20.0, dive_progress)

    glPushMatrix()
    glTranslatef(12, 0, 10)
    glRotatef(arm_ang, 0, 1, 0)
    glScalef(1.0, 0.22, 0.22)
    glutSolidCube(20)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-12, 0, 10)
    glRotatef(-arm_ang, 0, 1, 0)
    glScalef(1.0, 0.22, 0.22)
    glutSolidCube(20)
    glPopMatrix()

    # legs
    glColor3f(0.1, 0.1, 0.1)
    if parachute_deployed:
        leg_ang = -5.0
    else:
        leg_ang = lerp(-35.0, -10.0, dive_progress)

    glPushMatrix()
    glTranslatef(6, 0, -17)
    glRotatef(leg_ang, 1, 0, 0)
    glScalef(0.25, 0.25, 1.0)
    glutSolidCube(18)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-6, 0, -17)
    glRotatef(leg_ang, 1, 0, 0)
    glScalef(0.25, 0.25, 1.0)
    glutSolidCube(18)
    glPopMatrix()

    # parachute canopy and lines
    if parachute_deployed:
        # Inflate visually with the same progress used for physics
        t = clamp(parachute_open_progress, 0.0, 1.0)
        t = t * t * (3.0 - 2.0 * t)  # smoothstep

        canopy_r = lerp(10.0, 48.0, t)
        canopy_h = lerp(4.0, 22.0, t)
        rim_z = 62.0 + lerp(0.0, 10.0, t)

        harness_l = (-10.0, 0.0, 18.0)
        harness_r = (10.0, 0.0, 18.0)

        # Suspension lines to the canopy rim
        glColor3f(0.88, 0.88, 0.88)
        glBegin(GL_LINES)
        line_count = 14
        for i in range(line_count):
            phi = (i / line_count) * (2.0 * math.pi)
            scallop = 1.0 + 0.06 * math.sin(phi * line_count)
            ax = math.cos(phi) * canopy_r * scallop
            ay = math.sin(phi) * canopy_r * scallop
            az = rim_z
            hx, hy, hz = harness_l if (i % 2 == 0) else harness_r
            glVertex3f(hx, hy, hz)
            glVertex3f(ax, ay, az)
        glEnd()

        # Two main risers (slightly thicker)
        glLineWidth(3.0)
        glColor3f(0.75, 0.75, 0.75)
        glBegin(GL_LINES)
        glVertex3f(harness_l[0], harness_l[1], harness_l[2])
        glVertex3f(-6.0, 0.0, rim_z - 6.0)
        glVertex3f(harness_r[0], harness_r[1], harness_r[2])
        glVertex3f(6.0, 0.0, rim_z - 6.0)
        glEnd()
        glLineWidth(1.0)

        # Canopy: a ribbed hemisphere with colored panels
        glPushMatrix()
        glTranslatef(0.0, 0.0, rim_z)

        panels = 12
        slices = 36
        stacks = 9

        for si in range(stacks):
            theta0 = (si / stacks) * (math.pi / 2.0)
            theta1 = ((si + 1) / stacks) * (math.pi / 2.0)
            r0 = math.cos(theta0) * canopy_r
            r1 = math.cos(theta1) * canopy_r
            z0 = math.sin(theta0) * canopy_h
            z1 = math.sin(theta1) * canopy_h
            glBegin(GL_TRIANGLE_STRIP)
            for sj in range(slices + 1):
                phi = (sj / slices) * (2.0 * math.pi)
                panel = int((phi / (2.0 * math.pi)) * panels)
                base = (0.92, 0.18, 0.18) if (panel % 2 == 0) else (0.94, 0.94, 0.94)

                # subtle shading so it reads like cloth
                shade0 = 0.82 + 0.18 * (z0 / max(0.001, canopy_h))
                shade1 = 0.82 + 0.18 * (z1 / max(0.001, canopy_h))

                scallop = 1.0 + 0.06 * math.sin(phi * panels)
                x0 = math.cos(phi) * r0 * scallop
                y0 = math.sin(phi) * r0 * scallop
                x1 = math.cos(phi) * r1
                y1 = math.sin(phi) * r1

                glColor3f(base[0] * shade0, base[1] * shade0, base[2] * shade0)
                glVertex3f(x0, y0, z0)
                glColor3f(base[0] * shade1, base[1] * shade1, base[2] * shade1)
                glVertex3f(x1, y1, z1)
            glEnd()

        # Rim band (adds thickness)
        glColor3f(0.20, 0.20, 0.22)
        glBegin(GL_QUAD_STRIP)
        for sj in range(slices + 1):
            phi = (sj / slices) * (2.0 * math.pi)
            scallop = 1.0 + 0.06 * math.sin(phi * panels)
            x = math.cos(phi) * canopy_r * scallop
            y = math.sin(phi) * canopy_r * scallop
            glVertex3f(x, y, 0.0)
            glVertex3f(x, y, -2.0)
        glEnd()

        glPopMatrix()

        # Vent cap at the top
        glColor3f(0.08, 0.08, 0.10)
        glPushMatrix()
        glTranslatef(0.0, 0.0, rim_z + canopy_h)
        glutSolidSphere(2.2, 10, 10)
        glPopMatrix()

    glPopMatrix()


def draw_world():
    draw_stars_and_sun()
    draw_clouds()
    if not jump_started:
        draw_jump_marker()
    draw_checkered_ground()
    draw_landing_target()
    draw_player_ground_marker()
    draw_trees()
    draw_drift_indicator()
    if game_status != "LANDED":
        draw_plane()
    draw_skydiver()


def apply_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, WINDOW_W / WINDOW_H, 0.1, 3000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if camera_mode == 0:
        # Follow camera
        target_x = player_x - 160
        target_y = player_y - 210
        target_z = player_z + 90
        if game_status == "LANDED":
            # Snap camera on landing to avoid the "rotating" feel from smoothing.
            camera_follow[0] = target_x
            camera_follow[1] = target_y
            camera_follow[2] = target_z
        else:
            camera_follow[0] += (target_x - camera_follow[0]) * 0.12
            camera_follow[1] += (target_y - camera_follow[1]) * 0.12
            camera_follow[2] += (target_z - camera_follow[2]) * 0.12
        gluLookAt(camera_follow[0], camera_follow[1], camera_follow[2], player_x, player_y, player_z, 0, 0, 1)
    elif camera_mode == 1:
        # Top-down camera
        gluLookAt(player_x, player_y, player_z + 320, player_x, player_y, player_z - 50, 0, 1, 0)
    else:
        # Free camera
        gluLookAt(
            free_cam_pos[0], free_cam_pos[1], free_cam_pos[2],
            player_x, player_y, max(0, player_z - 40),
            0, 0, 1
        )


def try_deploy_parachute():
    global parachute_deployed, parachute_open_progress, game_status, jump_started
    global diving, dive_progress
    if game_status == "LANDED":
        return
    jump_started = True
    parachute_deployed = True
    parachute_open_progress = 0.0
    diving = False
    dive_progress = 0.0
    game_status = "CANOPY"


def trigger_jump_or_chute():
    global jump_started
    if not jump_started:
        jump_started = True
        return

    if not parachute_deployed:
        try_deploy_parachute()


def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for camera mode, parachute deployment, reset,
    and free camera movement.
    """
    global camera_mode, wind_on, jump_started
    global diving

    if key == b'c':
        camera_mode = (camera_mode + 1) % 3
    elif key == b'r':
        reset_game()
    elif key == b' ':
        trigger_jump_or_chute()
    elif key == b'x':
        # Toggle head-down diving (freefall only)
        if jump_started and (not parachute_deployed) and game_status != "LANDED":
            diving = not diving
    elif key == b'w' and camera_mode == 2:
        free_cam_pos[1] += 30
    elif key == b's' and camera_mode == 2:
        free_cam_pos[1] -= 30
    elif key == b'a' and camera_mode == 2:
        free_cam_pos[0] -= 30
    elif key == b'd' and camera_mode == 2:
        free_cam_pos[0] += 30
    elif key == b'q' and camera_mode == 2:
        free_cam_pos[2] += 30
    elif key == b'e' and camera_mode == 2:
        free_cam_pos[2] -= 30
    elif key == b'v':
        # optional quick wind toggle from keyboard too
        wind_on = not wind_on


def specialKeyListener(key, x, y):
    """
    Arrow keys apply drift and body tilt direction while in air.
    """
    active_special_keys.add(key)


def specialKeyUpListener(key, x, y):
    if key in active_special_keys:
        active_special_keys.remove(key)


def mouseListener(button, state, x, y):
    """
    Left click deploys parachute, right click toggles wind.
    """
    global wind_on

    if state != GLUT_DOWN:
        return

    if button == GLUT_LEFT_BUTTON:
        trigger_jump_or_chute()
    elif button == GLUT_RIGHT_BUTTON:
        wind_on = not wind_on


def evaluate_landing(impact_speed):
    global game_status, outcome_text, score, last_impact_speed

    game_status = "LANDED"
    last_impact_speed = impact_speed
    dx = player_x - TARGET_CENTER_X
    dy = player_y - TARGET_CENTER_Y
    drift = math.sqrt(dx * dx + dy * dy)

    # Survival depends on impact speed
    if (not parachute_deployed) or impact_speed > 12.0:
        outcome_text = "Crash"
        score = 0
        return

    # Archery ring scoring (10 = bullseye, 0 = off board)
    points = 0
    if drift <= TARGET_OUTER_RADIUS:
        for i in range(TARGET_RING_COUNT):
            r = TARGET_INNER_RADIUS + TARGET_RING_STEP * i
            if drift <= r:
                points = TARGET_RING_COUNT - i
                break

    score = points
    if points == 10:
        outcome_text = "Bullseye"
    elif points >= 7:
        outcome_text = "Great landing"
    elif points >= 4:
        outcome_text = "Good landing"
    elif points >= 1:
        outcome_text = "On target board"
    else:
        outcome_text = "Missed target"


def update_physics(dt=1 / 60):
    global player_x, player_y, player_z, vx, vy, fall_speed
    global plane_x, plane_y, game_status, jump_started
    global parachute_open_progress
    global diving, dive_progress
    global world_time

    world_time += dt

    if game_status == "LANDED":
        return

    if not jump_started:
        # Stay near the plane until the jump begins.
        player_x = plane_x + 20
        player_y = plane_y
        player_z = plane_z - 10
        plane_x += 55 * dt
        plane_y += 14 * dt
        game_status = "ON PLANE"
        return

    # Plane flies away once jump starts
    plane_x += 90 * dt
    plane_y += 24 * dt

    # Dive transition (head-down) only works before canopy
    if parachute_deployed:
        diving = False
        dive_progress = 0.0
    else:
        if diving:
            dive_progress += dt * 2.2
        else:
            dive_progress -= dt * 2.6
        dive_progress = clamp(dive_progress, 0.0, 1.0)

    # Arrow-key drift control (more noticeable): steer toward a target horizontal speed.
    ix = 0
    iy = 0
    if GLUT_KEY_LEFT in active_special_keys:
        ix -= 1
    if GLUT_KEY_RIGHT in active_special_keys:
        ix += 1
    if GLUT_KEY_UP in active_special_keys:
        iy += 1
    if GLUT_KEY_DOWN in active_special_keys:
        iy -= 1

    if ix != 0 or iy != 0:
        ln = math.sqrt(ix * ix + iy * iy)
        ix /= ln
        iy /= ln

    if parachute_deployed:
        max_h_speed = 160.0
        response = 10.0
    else:
        # In a head-down dive you go faster vertically, but drift control becomes a bit less powerful.
        max_h_speed = lerp(220.0, 180.0, dive_progress)
        response = lerp(8.0, 6.0, dive_progress)
    desired_vx = ix * max_h_speed
    desired_vy = iy * max_h_speed
    vx += (desired_vx - vx) * response * dt
    vy += (desired_vy - vy) * response * dt

    # A little air friction so it doesn't feel like ice
    air_damp = 0.988 if parachute_deployed else 0.994
    vx *= air_damp
    vy *= air_damp

    # Vertical speed model:
    # Gravity pulls down and air drag grows with speed.
    # When the chute opens, the drag ramps up over a short period instead of
    # switching instantly.
    if parachute_deployed:
        parachute_open_progress += dt * 0.6
        if parachute_open_progress > 1.0:
            parachute_open_progress = 1.0
    else:
        parachute_open_progress = 0.0

    base_drag = FREEFALL_DRAG if parachute_deployed else lerp(FREEFALL_DRAG, DIVE_DRAG, dive_progress)
    drag = base_drag + ((PARACHUTE_DRAG - base_drag) * parachute_open_progress)
    fall_accel = GRAVITY - (drag * fall_speed)
    fall_speed += fall_accel * dt
    if fall_speed < 0.0:
        fall_speed = 0.0

    if parachute_deployed:
        game_status = "CANOPY"
    else:
        game_status = "DIVE" if dive_progress > 0.55 else "FREEFALL"

    wx, wy = wind_vec if wind_on else (0.0, 0.0)
    player_x += (vx + wx) * dt
    player_y += (vy + wy) * dt
    player_z -= fall_speed * dt

    # Keep the steering readable and prevent the player from drifting too far off-screen.
    player_x = max(-650, min(650, player_x))
    player_y = max(-650, min(650, player_y))

    # Land check
    if player_z <= 0:
        impact_speed = fall_speed
        player_z = 0
        evaluate_landing(impact_speed)


def draw_hud():
    altitude = player_z
    drift = math.sqrt(player_x * player_x + player_y * player_y)
    wind_label = "ON" if wind_on else "OFF"
    chute_label = "DEPLOYED" if parachute_deployed else "NOT DEPLOYED"
    dive_label = "ON" if (game_status != "LANDED" and dive_progress > 0.55 and (not parachute_deployed) and jump_started) else "OFF"

    draw_text(12, 772, f"Altitude: {altitude:6.1f} m")
    draw_text(12, 746, f"Fall Speed: {fall_speed:5.1f} m/s")
    draw_text(12, 720, f"Drift Distance: {drift:6.1f} m")
    draw_text(12, 694, f"Parachute: {chute_label}")
    draw_text(12, 668, f"Dive (X): {dive_label}")
    draw_text(12, 642, f"Wind: {wind_label}  Dir=({wind_vec[0]:.1f}, {wind_vec[1]:.1f})")

    camera_name = ["Follow", "Top-Down", "Free"]
    draw_text(12, 616, f"Camera: {camera_name[camera_mode]} (press C to switch)")
    draw_text(12, 590, f"Status: {game_status}")

    draw_text(12, 20, "Controls: Arrow=Drift | Space/Left Click=Jump, press again to open chute | X=Dive | Right Click=Wind | C=Camera | R=Reset")
    draw_text(12, 48, "Tip: the yellow line shows your drift direction")

    # Arrow-key indicator (makes left/right/forward/backward obvious)
    active_c = (0.25, 1.0, 0.35)
    idle_c = (0.55, 0.55, 0.55)
    draw_text(890, 140, "UP", font=GLUT_BITMAP_8_BY_13,
              color=active_c if GLUT_KEY_UP in active_special_keys else idle_c)
    draw_text(850, 120, "LEFT", font=GLUT_BITMAP_8_BY_13,
              color=active_c if GLUT_KEY_LEFT in active_special_keys else idle_c)
    draw_text(920, 120, "RIGHT", font=GLUT_BITMAP_8_BY_13,
              color=active_c if GLUT_KEY_RIGHT in active_special_keys else idle_c)
    draw_text(885, 100, "DOWN", font=GLUT_BITMAP_8_BY_13,
              color=active_c if GLUT_KEY_DOWN in active_special_keys else idle_c)

    if not jump_started:
        draw_text(330, 770, "Press Space or Left Click to jump")
    elif not parachute_deployed:
        draw_text(350, 770, "Freefall: open the parachute at the right time")

    if game_status == "LANDED":
        draw_text(370, 760, f"Result: {outcome_text}")
        draw_text(390, 734, f"Impact Speed: {last_impact_speed:4.1f} m/s")
        draw_text(410, 708, f"Points: {score}/10")
        draw_text(345, 682, "Press R for another jump")


def idle():
    """
    Idle function that runs continuously:
    - Updates gameplay physics.
    - Triggers redraw.
    """
    update_physics(1 / 60)
    glutPostRedisplay()


def showScreen():
    """
    Display function to render the full skydiving scene.
    """
    glViewport(0, 0, WINDOW_W, WINDOW_H)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # 2D sky gradient first, then 3D world
    draw_sky_gradient_overlay()

    glClear(GL_DEPTH_BUFFER_BIT)
    apply_camera()
    draw_world()

    # small title text layer for clarity
    draw_text(760, 770, "Skydiving Emulator")

    # HUD on top
    draw_hud()

    glutSwapBuffers()


def setup_gl():
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_POINT_SMOOTH)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)

# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(WINDOW_W, WINDOW_H)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"Skydiving Emulator")  # Create the window

    setup_gl()
    reset_game()

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    # Some GLUT builds may not expose special-key release callback
    try:
        glutSpecialUpFunc(specialKeyUpListener)
    except Exception:
        pass
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register idle update

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
