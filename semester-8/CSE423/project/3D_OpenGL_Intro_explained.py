""" 
3D_OpenGL_Intro_explained.py

This is an *annotated* (explained) copy of 3D_OpenGL_Intro.py.

Goal of this file:
- Keep the SAME game behavior and structure.
- Add section-by-section explanations.
- Add inline comments so you can understand what each line does.

How to run:
- `python3 3D_OpenGL_Intro_explained.py`

Controls:
- Space / Left Click: Jump (press again to open parachute)
- Arrow keys: Drift left/right/forward/backward
- X: Toggle head-down dive (freefall only)
- Right Click (or V): Toggle wind
- C: Switch camera mode
- R: Reset
"""

# =============================================================================
# SECTION 1) Imports
# =============================================================================

from OpenGL.GL import *  # OpenGL core API (drawing, colors, transforms, depth testing)
from OpenGL.GLUT import *  # GLUT (window creation, input callbacks, built-in shapes)
from OpenGL.GLU import *  # GLU helpers (camera perspective, cylinders, quadrics)
import math  # Math utilities (sin/cos, radians, sqrt, etc.)
import random  # Random numbers (used for star field positions)

# =============================================================================
# SECTION 1B) Cheat-sheet: “built-in” functions used in this file
# =============================================================================
# In this project, "built-in" usually means functions provided by:
# - OpenGL (gl*), GLUT (glut*), and GLU (glu*)
# - plus a few Python built-ins (range, enumerate, min/max, etc.)
#
# The short explanations below answer:
# - What the function does
# - Why we use it here
# - A tiny example when it helps
#
# -------------------------
# A) OpenGL drawing basics
# -------------------------
# glBegin(MODE) / glEnd()
# - Meaning: Start/finish describing a shape.
# - Why: We build ground tiles, rings, arrows, etc. by listing vertices.
# - Example:
#     glBegin(GL_LINES)
#     glVertex3f(0, 0, 0); glVertex3f(50, 0, 0)
#     glEnd()
#
# glVertex2f(x, y) / glVertex3f(x, y, z)
# - Meaning: Add a vertex (point) to the current glBegin block.
# - Why: Every custom shape is made of vertices.
#
# glColor3f(r, g, b) / glColor4f(r, g, b, a)
# - Meaning: Set the current drawing color (and alpha if using 4f).
# - Why: Colors for sky, ground, parachute panels, HUD accents.
#
# glLineWidth(w) / glPointSize(s)
# - Meaning: Change thickness of lines / size of points.
# - Why: Make markers and arrows easier to see.
#
# -------------------------
# B) Transforms (move/rotate/scale objects)
# -------------------------
# glPushMatrix() / glPopMatrix()
# - Meaning: Save/restore the current transform.
# - Why: So moving/rotating one object (plane, player, cloud) doesn’t affect others.
#
# glTranslatef(dx, dy, dz)
# - Meaning: Move subsequent drawing by (dx, dy, dz).
# - Why: Place objects in the world (e.g., move to player position).
#
# glRotatef(angle_deg, ax, ay, az)
# - Meaning: Rotate subsequent drawing around axis (ax, ay, az).
# - Why: Lean the skydiver, tilt the plane, draw upright trees.
#
# glScalef(sx, sy, sz)
# - Meaning: Scale subsequent drawing.
# - Why: Stretch a cube into a wing/torso, scale clouds, etc.
#
# -------------------------
# C) Camera + coordinate setup (GLU + matrix modes)
# -------------------------
# glMatrixMode(GL_PROJECTION) / glMatrixMode(GL_MODELVIEW)
# - Meaning: Choose which matrix you’re editing:
#   - PROJECTION = “lens” (perspective/ortho)
#   - MODELVIEW = camera + object transforms
# - Why: We switch to PROJECTION for camera setup and for 2D HUD, then back.
#
# glLoadIdentity()
# - Meaning: Reset the current matrix to “no transform”.
# - Why: Start from a clean transform before building camera/HUD transforms.
#
# gluPerspective(fovY, aspect, near, far)
# - Meaning: Set a perspective projection (3D depth).
# - Why: The main 3D view uses perspective so distant things look smaller.
#
# gluOrtho2D(left, right, bottom, top)
# - Meaning: Set a 2D projection (no perspective).
# - Why: Used for HUD/text overlay in screen coordinates.
#
# gluLookAt(eyeX, eyeY, eyeZ, centerX, centerY, centerZ, upX, upY, upZ)
# - Meaning: Position the camera (eye) and point it at (center).
# - Why: Follow camera, top-down camera, and free camera all use this.
#
# -------------------------
# D) Common OpenGL “state” controls
# -------------------------
# glEnable(GL_DEPTH_TEST) / glDisable(GL_DEPTH_TEST)
# - Meaning: Depth test makes nearer pixels cover farther pixels.
# - Why: Needed for 3D; sometimes disabled for HUD outlines to avoid flicker.
#
# glClearColor(r, g, b, a) and glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
# - Meaning: Set the clear color, then clear the screen each frame.
# - Why: Every frame starts fresh to avoid “smearing” old frames.
#
# glViewport(x, y, w, h)
# - Meaning: Tell OpenGL which part of the window to draw into.
# - Why: Match rendering to window size.
#
# glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
# - Meaning: Standard transparency blending.
# - Why: Makes cockpit bubble and clouds appear translucent.
#
# glDepthMask(GL_FALSE) / glDepthMask(GL_TRUE)
# - Meaning: Control whether we WRITE into the depth buffer.
# - Why: For transparent clouds, we often don’t write depth so blending looks nicer.
#
# glPolygonOffset(factor, units) + glEnable(GL_POLYGON_OFFSET_FILL)
# - Meaning: Push filled polygons slightly in depth.
# - Why: Avoid “z-fighting shimmer” when two surfaces are almost on the same plane
#   (e.g., target board vs ground).
#
# glHint(target, GL_NICEST)
# - Meaning: Ask for nicer smoothing quality (implementation-dependent).
# - Why: Better-looking lines/points.
#
# glRasterPos2f(x, y) + glutBitmapCharacter(font, code)
# - Meaning: Place and draw bitmap text.
# - Why: HUD text.
#
# -------------------------
# E) GLUT built-in 3D primitives (quick shapes)
# -------------------------
# glutSolidSphere(radius, slices, stacks)
# glutSolidCube(size)
# glutSolidCone(baseRadius, height, slices, stacks)
# - Meaning: Pre-made 3D shapes.
# - Why: Fast way to build a scene without custom mesh files.
#
# -------------------------
# F) GLUT window + event loop (“game loop”)
# -------------------------
# glutInit(), glutCreateWindow(...)
# - Meaning: Start GLUT and create a window.
#
# glutDisplayFunc(showScreen)
# - Meaning: Register the draw function.
#
# glutIdleFunc(idle)
# - Meaning: Register a function that runs repeatedly.
# - Why: We update physics and request redraws here.
#
# glutKeyboardFunc / glutSpecialFunc / glutMouseFunc
# - Meaning: Register input callbacks.
#
# glutPostRedisplay()
# - Meaning: Ask GLUT to redraw soon.
#
# glutSwapBuffers()
# - Meaning: Show the drawn frame (double buffering prevents flicker).
#
# glutMainLoop()
# - Meaning: Start the event loop (keeps the program running).
#
# -------------------------
# G) GLU “quadric” helpers (cylinders)
# -------------------------
# gluNewQuadric()
# - Meaning: Create a helper object used by GLU for curved shapes.
#
# gluCylinder(quad, baseR, topR, height, slices, stacks)
# - Meaning: Draw a cylinder.
# - Why: Used for tree trunks and plane fuselage.
#
# -------------------------
# H) Python built-ins + standard-library helpers used
# -------------------------
# range(n)
# - Meaning: Generate 0..n-1 for loops.
# - Example: for i in range(3): print(i)  # 0,1,2
#
# enumerate(iterable)
# - Meaning: Loop with both index and value.
# - Example: for i, v in enumerate([10,20]): ...
#
# min(a, b) / max(a, b)
# - Meaning: Pick smallest/largest.
# - Why: Used to clamp movement and keep values in bounds.
#
# set()
# - Meaning: A collection of unique items.
# - Why: Perfect for “which arrow keys are currently held down”.
#
# ord(ch)
# - Meaning: Convert a character to its integer code.
# - Why: GLUT bitmap text needs a number (ASCII code).
#
# int(x)
# - Meaning: Convert to integer.
# - Why: Used when turning an angle into a “panel index” for coloring.
#
# math.sin/cos/sqrt/radians/degrees/atan2
# - Meaning: Standard math building blocks.
# - Why: Movement vectors, circles, headings, and smooth animations.
#
# random.uniform(a, b)
# - Meaning: Random float between a and b.
# - Why: Scatter stars naturally across the sky.

# -------------------------
# I) Common OpenGL / GLUT constants (“named numbers”)
# -------------------------
# You’ll see many GL_* and GLUT_* values passed into functions.
# They are NOT functions themselves — they’re just constants that tell
# OpenGL/GLUT *which mode* you want.
#
# Drawing modes (used with glBegin):
# - GL_POINTS: each vertex is a dot
# - GL_LINES: each pair of vertices is a separate line
# - GL_LINE_LOOP: vertices make a closed outline
# - GL_TRIANGLE_FAN: triangles around a center point (good for filled circles)
# - GL_TRIANGLE_STRIP: connected strip of triangles (good for rings)
# - GL_QUADS: every 4 vertices make a quad tile (used for the ground)
#
# Buffers (used with glClear):
# - GL_COLOR_BUFFER_BIT: the color image
# - GL_DEPTH_BUFFER_BIT: the depth buffer (for 3D visibility)
#
# Matrix targets (used with glMatrixMode):
# - GL_PROJECTION: the camera “lens”
# - GL_MODELVIEW: camera position + object transforms
#
# Enable/Disable flags (used with glEnable/glDisable):
# - GL_DEPTH_TEST: enable 3D depth testing
# - GL_BLEND: enable transparency blending
# - GL_CULL_FACE: remove back-facing polygons (we keep this OFF in this project)
# - GL_POLYGON_OFFSET_FILL: allow polygon offset for filled polygons
# - GL_LINE_SMOOTH / GL_POINT_SMOOTH: try to smooth lines/points
#
# Blending parameters (used with glBlendFunc):
# - GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA: standard “normal” alpha blending
#
# Boolean-style constants:
# - GL_TRUE / GL_FALSE: used in some OpenGL calls like glDepthMask(...)
#
# GLUT window flags (used with glutInitDisplayMode):
# - GLUT_DOUBLE: double buffering (prevents flicker)
# - GLUT_RGB: RGB color buffer
# - GLUT_DEPTH: depth buffer
#
# GLUT input constants:
# - GLUT_KEY_LEFT/RIGHT/UP/DOWN: arrow keys
# - GLUT_LEFT_BUTTON / GLUT_RIGHT_BUTTON: mouse buttons
# - GLUT_DOWN: button pressed state

# =============================================================================
# SECTION 2) Global settings (window + world)
# =============================================================================

WINDOW_W = 1000  # Window width in pixels
WINDOW_H = 800  # Window height in pixels
fovY = 75  # Field-of-view angle (vertical) for perspective camera
GRID_LENGTH = 700  # Size of ground/grid area (half-extent)

# =============================================================================
# SECTION 3) Physics constants
# =============================================================================

GRAVITY = 9.8  # Gravity acceleration (m/s^2) pulling you down
FREEFALL_DRAG = 0.18  # Air drag factor in freefall (bigger = slower terminal speed)
PARACHUTE_DRAG = 1.35  # Air drag factor after parachute opens (much bigger = slower fall)

DIVE_DRAG = 0.10  # Drag factor in head-down dive (smaller than FREEFALL_DRAG → faster fall)

# =============================================================================
# SECTION 4) Landing target (archery board) parameters
# =============================================================================

TARGET_CENTER_X = 0.0  # X position of the landing target center
TARGET_CENTER_Y = 0.0  # Y position of the landing target center
TARGET_INNER_RADIUS = 40.0  # Radius of the bullseye (inner circle)
TARGET_RING_STEP = 20.0  # Thickness of each ring
TARGET_RING_COUNT = 10  # Number of rings (10 → 1 points)
TARGET_OUTER_RADIUS = TARGET_INNER_RADIUS + TARGET_RING_STEP * (TARGET_RING_COUNT - 1)  # Outer edge radius

# =============================================================================
# SECTION 5) Game state (player + gameplay)
# =============================================================================

start_altitude = 1500.0  # Starting altitude (meters)

player_x = 0.0  # Player X position in world coordinates
player_y = 0.0  # Player Y position in world coordinates
player_z = start_altitude  # Player Z height (altitude)

vx = 0.0  # Player horizontal velocity in X (m/s)
vy = 0.0  # Player horizontal velocity in Y (m/s)
fall_speed = 0.0  # Downward speed (m/s) (positive number means going down)

parachute_deployed = False  # True once parachute is deployed
parachute_open_progress = 0.0  # 0→1 inflation progress of the canopy (smooth opening)

diving = False  # Whether head-down dive mode is toggled (freefall only)
dive_progress = 0.0  # Smooth 0→1 transition into dive pose/physics

wind_on = True  # Whether wind is enabled
wind_vec = (5.0, 2.0)  # Wind direction/speed affecting drift (x, y)

camera_mode = 0  # 0: follow, 1: top-down, 2: free camera
free_cam_pos = [300.0, -500.0, 500.0]  # Free camera position when camera_mode==2

game_status = "FREEFALL"  # String label used by HUD (ON PLANE / FREEFALL / DIVE / CANOPY / LANDED)
outcome_text = ""  # Result text after landing
score = 0  # Landing score (0–10)

jump_started = False  # False until the player actually jumps
camera_follow = [0.0, 0.0, start_altitude + 120.0]  # Smoothed follow camera position
last_impact_speed = 0.0  # Stored impact speed used in landing HUD

# =============================================================================
# SECTION 6) Plane state (the plane you jump from)
# =============================================================================

plane_x = -260.0  # Plane position X
plane_y = -260.0  # Plane position Y
plane_z = start_altitude + 40.0  # Plane position Z (slightly above player start altitude)

# =============================================================================
# SECTION 7) Input state
# =============================================================================

active_special_keys = set()  # Holds currently pressed arrow keys (GLUT special keys)

# =============================================================================
# SECTION 8) Visual world state (stars + time)
# =============================================================================

random.seed(423)  # Fix seed so stars are always placed the same way each run

stars = []  # List of (x, y, z) positions for stars
for _ in range(70):  # Create 70 stars
    stars.append((
        random.uniform(-900, 900),  # X coordinate
        random.uniform(-900, 900),  # Y coordinate
        random.uniform(1650, 1820),  # Z coordinate (high altitude)
    ))

world_time = 0.0  # A time counter used for cloud drifting animation

# =============================================================================
# SECTION 9) Small math helpers
# =============================================================================

def clamp(v, lo, hi):  # Clamp value v so it stays within [lo, hi]
    if v < lo:  # If value is below minimum
        return lo  # Return minimum
    if v > hi:  # If value is above maximum
        return hi  # Return maximum
    return v  # Otherwise return unchanged value


def lerp(a, b, t):  # Linear interpolation between a and b
    return a + (b - a) * t  # t=0→a, t=1→b

# =============================================================================
# SECTION 9B) Math used across this project (deeper, but still simple)
# =============================================================================
# This project has two big kinds of math:
#
# (1)  Game/physics math (motion)
# - We simulate motion using a small time-step `dt` (seconds per frame).
# - The core idea is “integration” (update values a little each frame):
#     speed += acceleration * dt
#     position += speed * dt
# - Units (the way we treat numbers):
#     player_x, player_y, player_z are in “meters” (scene units)
#     vx, vy are horizontal speeds (m/s)
#     fall_speed is vertical speed (m/s)
#
# Gravity + drag (terminal velocity idea)
# - Gravity adds downward acceleration.
# - Drag subtracts acceleration more strongly when speed is high.
# - We use a simple linear drag model for vertical speed:
#     fall_accel = GRAVITY - (drag * fall_speed)
#   When fall_speed increases, the drag term grows, so fall_accel shrinks.
#   Eventually fall_accel becomes near 0 → speed stops increasing much.
#
# (2) Visual/geometry math (circles, angles, smoothing)
# - Many shapes (target rings, markers, canopy rim) are circles.
# - A point on a circle of radius r is:
#     x = r * cos(theta)
#     y = r * sin(theta)
# - Our loops often use degrees (0..360), but Python trig uses radians.
#   So we convert: theta = radians(degrees).
#
# Normalization (make diagonal movement not faster)
# - If you press two arrow keys (diagonal), the input vector becomes (1,1).
#   That has length sqrt(1^2 + 1^2) = 1.414, which is faster than 1.
# - We “normalize” by dividing by the length to keep the final length 1.
#
# Smoothing (avoid sudden snapping)
# - `lerp` blends between values gradually.
# - We also use “exponential smoothing” style updates like:
#     value += (target - value) * k
#   This moves part-way each frame (stable and smooth).
#
# Smoothstep (nice easing curve)
# - We sometimes take a 0..1 progress value and ease it:
#     t = t*t*(3 - 2*t)
#   This starts slow, speeds up, then slows again (looks more natural).
#
# Distance for scoring
# - Landing score uses distance from target center:
#     d = sqrt(dx^2 + dy^2)
#   Compare d to ring radii to decide points.

# =============================================================================
# SECTION 9C) Function-by-function: what math happens inside
# =============================================================================
# clamp(v, lo, hi)
# - Comparisons (<, >) to keep values in a safe range.
# - Used heavily for progress values like parachute_open_progress, dive_progress.
#
# lerp(a, b, t)
# - Linear interpolation formula a + (b-a)*t.
# - Used to blend sizes, colors, steering strength, drag values smoothly.
#
# reset_game()
# - No complex math: sets numeric state back to constants (0.0, start_altitude, etc.).
#
# draw_sky_gradient_overlay()
# - Normalizes altitude: t = clamp(player_z / start_altitude, 0..1)
# - Uses lerp on RGB channels to blend between “near ground” and “high altitude” colors.
#
# draw_stars_and_sun()
# - Normalizes altitude and maps it to brightness using a shifted/scaled range:
#     star_brightness = clamp((t - 0.55) / 0.45, 0..1)
#   So stars appear mostly at high altitude.
#
# draw_clouds()
# - Uses sin/cos(world_time * rate + phase) to create gentle, repeating drift.
#   The result is small dx/dy offsets added to base cloud positions.
#
# draw_player_ground_marker()
# - Builds a circle outline by stepping angles and using cos/sin.
#   This is a direct use of the circle parametric formula.
#
# draw_checkered_ground()
# - Grid math: loops over x/y in steps, places quads at (ix, iy).
# - Uses parity (i+j)%2 to alternate colors.
#
# draw_landing_target()
# - Uses ring radii = inner + step*i.
# - Draws disks/rings via cos/sin.
# - Uses polygon offset + small z offsets (not “mathy”, but depth-buffer technique)
#   to avoid z-fighting shimmer.
#
# draw_plane()
# - Uses atan2 and degrees to approximate a heading angle in the XY plane.
# - Mostly fixed rotation/scaling constants.
#
# draw_drift_indicator()
# - Vector math: total movement vector m = (vx,vy) + wind.
# - Magnitude: mlen = sqrt(mx^2 + my^2)
# - Scaling: cap arrow length and compute factor af = arrow_len / mlen.
#
# draw_skydiver()
# - Uses vx/vy to compute lean angles, then clamps angles to [-18..18].
# - Dive flip uses -180*dive_progress degrees (smoothly rotates body).
# - Parachute inflation uses:
#     t = clamp(progress,0..1) then smoothstep(t)
#   and then uses lerp to grow canopy radius/height.
# - Suspension lines and canopy rim use cos/sin around a circle.
#
# apply_camera()
# - Perspective aspect ratio = WINDOW_W / WINDOW_H.
# - Follow camera smoothing uses partial movement each frame:
#     camera_follow += (target - camera_follow) * 0.12
#
# evaluate_landing(impact_speed)
# - Distance-to-center: drift = sqrt((x-x0)^2 + (y-y0)^2).
# - Ring scoring: compare drift to increasing radii until you find the first ring.
# - Crash threshold compares impact_speed to a constant.
#
# update_physics(dt)
# - Time integration everywhere: value changes are multiplied by dt.
# - Dive progress easing: progress +=/-= rate*dt then clamp.
# - Input normalization: divide (ix,iy) by sqrt(ix^2+iy^2) so diagonal isn’t faster.
# - Steering smoothing: v += (desired - v) * response * dt.
# - Damping: v *= air_damp (reduces jitter over time).
# - Drag blending: base_drag depends on freefall vs dive; then blend toward parachute drag
#   using parachute_open_progress (0..1).
# - Vertical acceleration: fall_accel = GRAVITY - drag*fall_speed.
# - Position update: x += (vx+wind)*dt, y += (vy+wind)*dt, z -= fall_speed*dt.
# - World bounds clamp with min/max.
#
# draw_hud()
# - Computes drift distance with sqrt(x^2 + y^2).
# - Formats numbers to 1 decimal place (presentation only).
#
# idle()
# - Uses a fixed dt of 1/60 seconds (simple fixed-step simulation).

# =============================================================================
# SECTION 10) Game reset
# =============================================================================

def reset_game():  # Reset all gameplay and camera state
    global player_x, player_y, player_z, vx, vy, fall_speed  # We will overwrite these globals
    global parachute_deployed, parachute_open_progress, wind_on, camera_mode  # More globals to reset
    global diving, dive_progress  # Dive-related globals
    global game_status, outcome_text, score, last_impact_speed  # Landing state
    global plane_x, plane_y, plane_z  # Plane state
    global active_special_keys, jump_started, camera_follow  # Input + camera smoothing state
    global world_time  # Time counter

    player_x = 0.0  # Reset position X
    player_y = 0.0  # Reset position Y
    player_z = start_altitude  # Reset altitude
    vx = 0.0  # Reset horizontal speed X
    vy = 0.0  # Reset horizontal speed Y
    fall_speed = 0.0  # Reset vertical speed

    parachute_deployed = False  # No parachute yet
    parachute_open_progress = 0.0  # Canopy not inflated
    diving = False  # Not diving
    dive_progress = 0.0  # Dive transition reset

    wind_on = True  # Start with wind enabled
    camera_mode = 0  # Default camera
    jump_started = False  # You are still on the plane

    game_status = "ON PLANE"  # HUD status string
    outcome_text = ""  # Clear result
    score = 0  # Clear score
    last_impact_speed = 0.0  # Clear impact speed

    plane_x = -260.0  # Reset plane X
    plane_y = -260.0  # Reset plane Y
    plane_z = start_altitude + 40.0  # Reset plane Z

    camera_follow = [0.0, 0.0, start_altitude + 120.0]  # Reset follow camera smoothing start

    active_special_keys = set()  # Clear pressed arrow keys
    world_time = 0.0  # Reset time counter

# =============================================================================
# SECTION 11) 2D text drawing (HUD)
# =============================================================================

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, color=(1, 1, 1)):  # Draw text at screen coords
    glColor3f(color[0], color[1], color[2])  # Set text color

    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix
    glPushMatrix()  # Save current projection
    glLoadIdentity()  # Reset projection

    gluOrtho2D(0, WINDOW_W, 0, WINDOW_H)  # Make a 2D coordinate system: (0..W, 0..H)

    glMatrixMode(GL_MODELVIEW)  # Switch to modelview matrix
    glPushMatrix()  # Save current modelview
    glLoadIdentity()  # Reset modelview

    glRasterPos2f(x, y)  # Position text cursor
    for ch in text:  # Draw each character
        glutBitmapCharacter(font, ord(ch))  # GLUT renders bitmap character

    glPopMatrix()  # Restore modelview
    glMatrixMode(GL_PROJECTION)  # Back to projection
    glPopMatrix()  # Restore projection
    glMatrixMode(GL_MODELVIEW)  # Return to modelview for rest of 3D drawing

# =============================================================================
# SECTION 12) Background sky gradient (2D overlay)
# =============================================================================

def draw_sky_gradient_overlay():  # Draw a full-screen gradient background
    glDisable(GL_DEPTH_TEST)  # Disable depth so overlay always draws on top

    glMatrixMode(GL_PROJECTION)  # Use projection matrix
    glPushMatrix()  # Save projection
    glLoadIdentity()  # Reset projection
    gluOrtho2D(0, WINDOW_W, 0, WINDOW_H)  # 2D screen coordinates

    glMatrixMode(GL_MODELVIEW)  # Use modelview matrix
    glPushMatrix()  # Save modelview
    glLoadIdentity()  # Reset modelview

    t = clamp(player_z / start_altitude, 0.0, 1.0)  # 1=high altitude, 0=ground

    top_deep = (0.03, 0.06, 0.25)  # Dark blue for high altitude
    top_light = (0.25, 0.55, 0.95)  # Lighter blue near ground
    bot_deep = (0.08, 0.18, 0.55)  # Deeper near-horizon color
    bot_light = (0.65, 0.90, 1.00)  # Bright near-ground color

    top = (  # Color at top of screen
        lerp(top_light[0], top_deep[0], t),  # Red component
        lerp(top_light[1], top_deep[1], t),  # Green component
        lerp(top_light[2], top_deep[2], t),  # Blue component
    )
    bot = (  # Color at bottom of screen
        lerp(bot_light[0], bot_deep[0], t),  # Red component
        lerp(bot_light[1], bot_deep[1], t),  # Green component
        lerp(bot_light[2], bot_deep[2], t),  # Blue component
    )

    glBegin(GL_QUADS)  # Draw a rectangle covering the whole screen
    glColor3f(bot[0], bot[1], bot[2])  # Bottom color
    glVertex2f(0, 0)  # Bottom-left
    glVertex2f(WINDOW_W, 0)  # Bottom-right

    glColor3f(top[0], top[1], top[2])  # Top color
    glVertex2f(WINDOW_W, WINDOW_H)  # Top-right
    glVertex2f(0, WINDOW_H)  # Top-left
    glEnd()  # Finish drawing quad

    glPopMatrix()  # Restore modelview
    glMatrixMode(GL_PROJECTION)  # Back to projection
    glPopMatrix()  # Restore projection
    glMatrixMode(GL_MODELVIEW)  # Back to modelview

    glEnable(GL_DEPTH_TEST)  # Re-enable depth test for 3D scene

# =============================================================================
# SECTION 13) Stars and sun (3D background)
# =============================================================================

def draw_stars_and_sun():  # Draw stars at high altitude + a distant sun sphere
    t = clamp(player_z / start_altitude, 0.0, 1.0)  # Normalize altitude
    star_brightness = clamp((t - 0.55) / 0.45, 0.0, 1.0)  # Stars fade in at high altitude

    if star_brightness > 0.01:  # Only draw if visible
        glPointSize(2.0)  # Star point size
        glBegin(GL_POINTS)  # Draw points
        glColor3f(star_brightness, star_brightness, star_brightness)  # White-ish stars
        for sx, sy, sz in stars:  # Loop over star positions
            glVertex3f(sx, sy, sz)  # Place star point
        glEnd()  # Finish drawing points

    glPushMatrix()  # Save transform
    glTranslatef(780, -780, 1150)  # Move to sun location
    glColor3f(1.0, 0.85, 0.2)  # Sun color
    glutSolidSphere(70, 16, 16)  # Draw a sphere
    glPopMatrix()  # Restore transform

# =============================================================================
# SECTION 14) Clouds (semi-transparent)
# =============================================================================

def draw_cloud(cx, cy, cz, alpha=0.55, scale=1.0):  # Draw one cloud as 3 overlapping spheres
    glColor4f(1.0, 1.0, 1.0, alpha)  # White with transparency
    glPushMatrix()  # Save transform
    glTranslatef(cx, cy, cz)  # Move to cloud position
    glScalef(scale, scale, scale)  # Scale the cloud

    glutSolidSphere(28, 12, 12)  # First puff
    glTranslatef(35, 5, 5)  # Move relative
    glutSolidSphere(24, 12, 12)  # Second puff
    glTranslatef(-70, -2, -2)  # Move relative
    glutSolidSphere(22, 12, 12)  # Third puff

    glPopMatrix()  # Restore transform


def draw_clouds():  # Draw multiple clouds drifting slightly over time
    glDepthMask(GL_FALSE)  # Don’t write clouds into depth buffer (helps transparency)

    cloud_positions = [  # Base positions for clouds
        (-380, 250, 1100),
        (270, -180, 900),
        (520, 360, 700),
        (-520, -420, 580),
        (120, 480, 450),
    ]

    for i, (cx, cy, cz) in enumerate(cloud_positions):  # Draw each cloud
        dx = math.sin(world_time * 0.18 + i) * 28  # Small drifting in X
        dy = math.cos(world_time * 0.14 + i * 1.7) * 18  # Small drifting in Y
        a = 0.42 + (i % 3) * 0.08  # Different alpha per cloud
        s = 0.95 + (i % 4) * 0.06  # Different scale per cloud
        draw_cloud(cx + dx, cy + dy, cz, alpha=a, scale=s)  # Draw the cloud

    glDepthMask(GL_TRUE)  # Restore depth writing

# =============================================================================
# SECTION 15) Ground marker (shows your drift clearly)
# =============================================================================

def draw_player_ground_marker():  # Draw a marker on the ground below the player
    glLineWidth(2.0)  # Thicker line for visibility

    glPushMatrix()  # Save transform
    glTranslatef(player_x, player_y, 1.2)  # Move to player position (slightly above ground)

    glColor3f(1.0, 0.95, 0.25)  # Bright yellow cross color
    size = 28  # Cross half-size

    glBegin(GL_LINES)  # Start lines
    glVertex3f(-size, 0, 0)  # Left point
    glVertex3f(size, 0, 0)  # Right point
    glVertex3f(0, -size, 0)  # Down point
    glVertex3f(0, size, 0)  # Up point
    glEnd()  # Finish lines

    glColor3f(0.95, 0.65, 0.12)  # Orange ring color
    glBegin(GL_LINE_LOOP)  # Draw a circle outline
    for a in range(0, 360, 20):  # Angle steps
        r = 18  # Circle radius
        rad = math.radians(a)  # Degrees → radians
        glVertex3f(math.cos(rad) * r, math.sin(rad) * r, 0)  # Point on circle
    glEnd()  # Finish outline

    glPopMatrix()  # Restore transform
    glLineWidth(1.0)  # Reset line width

# =============================================================================
# SECTION 16) Jump marker (shows jump start near plane)
# =============================================================================

def draw_jump_marker():  # Draw a cone marker showing jump zone
    glPushMatrix()  # Save transform
    glTranslatef(-120, -120, plane_z - 30)  # Place near plane
    glColor3f(1.0, 1.0, 0.2)  # Yellow
    glutSolidCone(18, 48, 10, 2)  # Cone(baseRadius, height, slices, stacks)
    glPopMatrix()  # Restore transform

# =============================================================================
# SECTION 17) Ground (checkered grass)
# =============================================================================

def draw_checkered_ground():  # Draw a simple checkered ground using quads
    step = 120  # Tile size

    for ix in range(-GRID_LENGTH, GRID_LENGTH, step):  # Loop over x tiles
        for iy in range(-GRID_LENGTH, GRID_LENGTH, step):  # Loop over y tiles
            c = ((ix // step) + (iy // step)) % 2  # Checker pattern

            if c == 0:  # One color
                glColor3f(0.18, 0.45, 0.18)  # Light green
            else:  # Alternate color
                glColor3f(0.12, 0.33, 0.12)  # Dark green

            glBegin(GL_QUADS)  # Draw quad tile
            glVertex3f(ix, iy, 0)  # Bottom-left
            glVertex3f(ix + step, iy, 0)  # Bottom-right
            glVertex3f(ix + step, iy + step, 0)  # Top-right
            glVertex3f(ix, iy + step, 0)  # Top-left
            glEnd()  # Finish quad

# =============================================================================
# SECTION 18) Landing target (archery board)
# =============================================================================

def draw_landing_target():  # Draw colored target rings
    # NOTE: This draws ring strips (annuli) to avoid z-fighting shimmer.

    def ring_color(score):  # Decide ring color based on points
        if score >= 9:  # 10-9 = yellow
            return (1.0, 0.92, 0.12)
        if score >= 7:  # 8-7 = red
            return (0.95, 0.15, 0.12)
        if score >= 5:  # 6-5 = blue
            return (0.15, 0.35, 0.95)
        if score >= 3:  # 4-3 = black
            return (0.08, 0.08, 0.08)
        return (0.95, 0.95, 0.95)  # 2-1 = white

    def filled_circle(radius, color, z=0.0):  # Draw a filled disk
        glColor3f(color[0], color[1], color[2])  # Set fill color
        glBegin(GL_TRIANGLE_FAN)  # Fan triangles around the center
        glVertex3f(0, 0, z)  # Center of circle
        for a in range(0, 361, 8):  # Go around full 360 degrees
            rad = math.radians(a)  # Convert degrees to radians
            glVertex3f(math.cos(rad) * radius, math.sin(rad) * radius, z)  # Circle point
        glEnd()  # Finish fan

    def ring_strip(inner_r, outer_r, color, z=0.0):  # Draw a ring between two radii
        glColor3f(color[0], color[1], color[2])  # Set ring color
        glBegin(GL_TRIANGLE_STRIP)  # Strip between outer and inner edge
        for a in range(0, 361, 8):  # Go around full circle
            rad = math.radians(a)  # Angle in radians
            ca = math.cos(rad)  # Cos for x
            sa = math.sin(rad)  # Sin for y
            glVertex3f(ca * outer_r, sa * outer_r, z)  # Outer point
            glVertex3f(ca * inner_r, sa * inner_r, z)  # Inner point
        glEnd()  # Finish strip

    def circle_outline(radius, color=(0, 0, 0)):  # Draw just an outline circle
        glColor3f(color[0], color[1], color[2])  # Set outline color
        glBegin(GL_LINE_LOOP)  # Line loop makes a closed circle
        for a in range(0, 360, 10):  # Angle steps
            rad = math.radians(a)  # To radians
            glVertex3f(math.cos(rad) * radius, math.sin(rad) * radius, 0)  # Point on circle
        glEnd()  # Finish outline

    glPushMatrix()  # Save transform
    glTranslatef(TARGET_CENTER_X, TARGET_CENTER_Y, 0.15)  # Lift slightly above ground

    glEnable(GL_POLYGON_OFFSET_FILL)  # Enable polygon offset to prevent z-fighting
    glPolygonOffset(-1.0, -1.0)  # Pull target slightly toward camera in depth

    filled_circle(TARGET_INNER_RADIUS, ring_color(10), z=0.0)  # Bullseye disk (10)

    for i in range(TARGET_RING_COUNT - 1):  # Build the outer rings
        points = TARGET_RING_COUNT - (i + 1)  # 9..1
        r0 = TARGET_INNER_RADIUS + TARGET_RING_STEP * i  # Inner radius of strip
        r1 = TARGET_INNER_RADIUS + TARGET_RING_STEP * (i + 1)  # Outer radius
        ring_strip(r0, r1, ring_color(points), z=0.0)  # Draw ring strip

    glDisable(GL_POLYGON_OFFSET_FILL)  # Stop polygon offset

    glLineWidth(2.0)  # Thicker outlines
    glDisable(GL_DEPTH_TEST)  # Disable depth so outlines don’t flicker

    for i in range(TARGET_RING_COUNT):  # Draw ring boundary outlines
        r = TARGET_INNER_RADIUS + TARGET_RING_STEP * i  # Radius
        outline_c = (1, 1, 1) if (3 <= (TARGET_RING_COUNT - i) <= 4) else (0, 0, 0)  # Contrast
        circle_outline(r, outline_c)  # Draw outline

    glColor3f(0, 0, 0)  # Black center dot
    glPushMatrix()  # Save transform for dot
    glTranslatef(0.0, 0.0, 0.08)  # Lift dot slightly
    glutSolidSphere(2.3, 10, 10)  # Small sphere as dot
    glPopMatrix()  # Restore

    glEnable(GL_DEPTH_TEST)  # Restore depth test for rest of scene
    glLineWidth(1.0)  # Reset line width
    glPopMatrix()  # Restore transform

# =============================================================================
# SECTION 19) Trees (simple decoration)
# =============================================================================

def draw_tree(tx, ty):  # Draw one tree at (tx, ty)
    quad = gluNewQuadric()  # Create quadric object for cylinder

    glPushMatrix()  # Save transform
    glTranslatef(tx, ty, 0)  # Move to tree base
    glColor3f(0.45, 0.28, 0.1)  # Brown trunk color
    glRotatef(-90, 1, 0, 0)  # Rotate so cylinder points up (Z)
    gluCylinder(quad, 8, 8, 45, 8, 1)  # Cylinder(baseRadius, topRadius, height, slices, stacks)
    glPopMatrix()  # Restore

    glPushMatrix()  # Save transform
    glTranslatef(tx, ty, 62)  # Move to tree top
    glColor3f(0.05, 0.45, 0.1)  # Green leaves color
    glutSolidSphere(24, 12, 12)  # Leaves as sphere
    glPopMatrix()  # Restore


def draw_trees():  # Draw multiple trees around edges
    positions = [  # Fixed tree positions
        (-620, -620),
        (-620, 620),
        (620, -620),
        (620, 620),
        (-620, 0),
        (620, 0),
        (0, -620),
        (0, 620),
    ]

    for tx, ty in positions:  # Loop through tree positions
        draw_tree(tx, ty)  # Draw each tree

# =============================================================================
# SECTION 20) Plane model
# =============================================================================

def draw_plane():  # Draw the airplane (simple stylized model)
    glPushMatrix()  # Save transform
    glTranslatef(plane_x, plane_y, plane_z)  # Move to plane position

    heading = math.degrees(math.atan2(24.0, 90.0))  # Heading angle approximation
    glRotatef(heading, 0, 0, 1)  # Rotate plane in XY
    glRotatef(-8, 1, 0, 0)  # Slight pitch for style
    glScalef(1.7, 1.7, 1.7)  # Scale up plane size

    glColor3f(0.86, 0.86, 0.90)  # Fuselage color
    glPushMatrix()  # Save
    glRotatef(90, 0, 1, 0)  # Rotate cylinder along X
    gluCylinder(gluNewQuadric(), 11, 11, 90, 12, 2)  # Main body cylinder
    glPopMatrix()  # Restore

    glColor3f(0.82, 0.82, 0.86)  # Nose color
    glPushMatrix()  # Save
    glTranslatef(48, 0, 0)  # Move to nose
    glRotatef(90, 0, 1, 0)  # Align cone
    glutSolidCone(11, 16, 12, 2)  # Nose cone
    glPopMatrix()  # Restore

    glColor3f(0.62, 0.62, 0.66)  # Tail color
    glPushMatrix()  # Save
    glTranslatef(-44, 0, 0)  # Move to tail
    glRotatef(90, 0, 1, 0)  # Align cone
    glutSolidCone(8, 16, 10, 2)  # Tail cone
    glPopMatrix()  # Restore

    glColor3f(0.90, 0.22, 0.18)  # Wing color
    glPushMatrix()  # Save
    glTranslatef(0, 0, -2)  # Position wings
    glScalef(2.6, 0.20, 0.55)  # Flatten wing
    glutSolidCube(28)  # Wing as scaled cube
    glPopMatrix()  # Restore

    glPushMatrix()  # Save
    glTranslatef(-30, 0, 14)  # Tail wing position
    glScalef(0.45, 0.15, 0.30)  # Scale
    glutSolidCube(24)  # Tail wing
    glPopMatrix()  # Restore

    glColor3f(0.90, 0.22, 0.18)  # Tail fin color
    glPushMatrix()  # Save
    glTranslatef(-36, 0, 26)  # Tail fin position
    glScalef(0.10, 0.45, 0.55)  # Scale to fin
    glutSolidCube(30)  # Fin
    glPopMatrix()  # Restore

    glColor3f(0.18, 0.25, 0.40)  # Window strip color
    glPushMatrix()  # Save
    glTranslatef(-6, 0, 6)  # Window position
    glScalef(1.3, 0.12, 0.18)  # Scale
    glutSolidCube(24)  # Window strip
    glPopMatrix()  # Restore

    glColor3f(0.55, 0.55, 0.58)  # Engine pod color
    for wing_side in (-1, 1):  # Left and right
        glPushMatrix()  # Save
        glTranslatef(8, wing_side * 14, -11)  # Pod position
        glScalef(0.35, 0.65, 0.35)  # Pod scaling
        glutSolidCube(16)  # Pod cube
        glPopMatrix()  # Restore

    glColor4f(0.20, 0.35, 0.55, 0.55)  # Cockpit bubble (semi-transparent)
    glPushMatrix()  # Save
    glTranslatef(26, 0, 10)  # Bubble position
    glScalef(1.1, 0.75, 0.65)  # Bubble scale
    glutSolidSphere(10, 14, 14)  # Bubble sphere
    glPopMatrix()  # Restore

    glPopMatrix()  # Restore overall plane transform

# =============================================================================
# SECTION 21) Drift indicator (visual arrows)
# =============================================================================

def draw_drift_indicator():  # Draw an arrow showing velocity + wind
    if not jump_started:  # If you are still on plane
        return  # Do not draw drift indicator

    glLineWidth(2.0)  # Thicker arrow line

    mx = vx + (wind_vec[0] if wind_on else 0.0)  # Total movement X (player + wind)
    my = vy + (wind_vec[1] if wind_on else 0.0)  # Total movement Y

    mlen = math.sqrt(mx * mx + my * my)  # Magnitude of movement vector
    if mlen < 0.001:  # Avoid divide-by-zero
        mlen = 0.001

    arrow_len = min(160.0, mlen * 1.2)  # Scale arrow length, cap it
    af = arrow_len / mlen  # Scale factor to reach arrow_len

    glColor3f(1.0, 1.0, 0.12)  # Yellow for actual movement
    glBegin(GL_LINES)  # Draw line
    glVertex3f(player_x, player_y, player_z)  # Start at player
    glVertex3f(player_x + mx * af, player_y + my * af, player_z + 30)  # End point
    glEnd()  # Finish

    if wind_on:  # If wind is enabled
        glColor3f(0.25, 0.9, 1.0)  # Cyan for wind
        glBegin(GL_LINES)  # Draw wind arrow
        glVertex3f(player_x, player_y, player_z + 10)  # Start
        glVertex3f(player_x + wind_vec[0] * 6.0, player_y + wind_vec[1] * 6.0, player_z + 10)  # End
        glEnd()  # Finish

    ix = 0  # Input direction X
    iy = 0  # Input direction Y

    if GLUT_KEY_LEFT in active_special_keys:  # Left pressed
        ix -= 1
    if GLUT_KEY_RIGHT in active_special_keys:  # Right pressed
        ix += 1
    if GLUT_KEY_UP in active_special_keys:  # Up pressed
        iy += 1
    if GLUT_KEY_DOWN in active_special_keys:  # Down pressed
        iy -= 1

    if ix != 0 or iy != 0:  # If any arrow key pressed
        glColor3f(0.25, 1.0, 0.35)  # Green for input direction
        glBegin(GL_LINES)  # Draw input arrow
        glVertex3f(player_x, player_y, player_z + 20)  # Start
        glVertex3f(player_x + ix * 55, player_y + iy * 55, player_z + 20)  # End
        glEnd()  # Finish

    glLineWidth(1.0)  # Reset line width

# =============================================================================
# SECTION 22) Skydiver model + parachute (player)
# =============================================================================

def draw_skydiver():  # Draw the player body and the parachute
    if parachute_deployed:  # Under canopy, lean less
        lean_scale = 0.55
    else:  # In freefall/dive, lean changes with dive progress
        lean_scale = lerp(1.0, 0.45, dive_progress)

    lean_x = max(-18, min(18, -vy * 4.0 * lean_scale))  # Lean around X based on vy
    lean_y = max(-18, min(18, vx * 4.0 * lean_scale))  # Lean around Y based on vx

    glPushMatrix()  # Save transform
    glTranslatef(player_x, player_y, player_z)  # Move to player position

    if (not parachute_deployed) and dive_progress > 0.001:  # If in dive transition
        glRotatef(-180.0 * dive_progress, 1, 0, 0)  # Flip body head-down smoothly

    glRotatef(lean_x, 1, 0, 0)  # Apply lean X
    glRotatef(lean_y, 0, 1, 0)  # Apply lean Y

    if parachute_deployed:  # Body tilt under canopy
        body_tilt = -2
    else:  # Body tilt in freefall/dive
        body_tilt = lerp(15.0, 0.0, dive_progress)
    glRotatef(body_tilt, 1, 0, 0)  # Apply tilt

    glColor3f(0.25, 0.3, 0.85)  # Body color
    glPushMatrix()  # Save
    glScalef(0.6, 0.35, 1.0)  # Scale cube into torso shape
    glutSolidCube(30)  # Torso cube
    glPopMatrix()  # Restore

    glColor3f(1.0, 0.84, 0.68)  # Head skin color
    glPushMatrix()  # Save
    glTranslatef(0, 0, 28)  # Head above torso
    glutSolidSphere(9, 12, 12)  # Head sphere
    glPopMatrix()  # Restore

    glColor3f(0.95, 0.7, 0.15)  # Arm color

    if parachute_deployed:  # Arms out under canopy
        arm_ang = 95.0
    else:  # Arms tuck during a dive
        arm_ang = lerp(55.0, 20.0, dive_progress)

    glPushMatrix()  # Save
    glTranslatef(12, 0, 10)  # Right arm position
    glRotatef(arm_ang, 0, 1, 0)  # Arm angle
    glScalef(1.0, 0.22, 0.22)  # Arm shape
    glutSolidCube(20)  # Right arm
    glPopMatrix()  # Restore

    glPushMatrix()  # Save
    glTranslatef(-12, 0, 10)  # Left arm position
    glRotatef(-arm_ang, 0, 1, 0)  # Mirror angle
    glScalef(1.0, 0.22, 0.22)  # Arm shape
    glutSolidCube(20)  # Left arm
    glPopMatrix()  # Restore

    glColor3f(0.1, 0.1, 0.1)  # Legs color

    if parachute_deployed:  # Legs hang down slightly
        leg_ang = -5.0
    else:  # Legs change between freefall and dive
        leg_ang = lerp(-35.0, -10.0, dive_progress)

    glPushMatrix()  # Save
    glTranslatef(6, 0, -17)  # Right leg position
    glRotatef(leg_ang, 1, 0, 0)  # Leg angle
    glScalef(0.25, 0.25, 1.0)  # Leg shape
    glutSolidCube(18)  # Right leg
    glPopMatrix()  # Restore

    glPushMatrix()  # Save
    glTranslatef(-6, 0, -17)  # Left leg position
    glRotatef(leg_ang, 1, 0, 0)  # Same leg angle
    glScalef(0.25, 0.25, 1.0)  # Leg shape
    glutSolidCube(18)  # Left leg
    glPopMatrix()  # Restore

    if parachute_deployed:  # Draw parachute only if deployed
        t = clamp(parachute_open_progress, 0.0, 1.0)  # Inflation progress
        t = t * t * (3.0 - 2.0 * t)  # Smoothstep for nicer animation

        canopy_r = lerp(10.0, 48.0, t)  # Canopy radius
        canopy_h = lerp(4.0, 22.0, t)  # Canopy height
        rim_z = 62.0 + lerp(0.0, 10.0, t)  # Rim Z position

        harness_l = (-10.0, 0.0, 18.0)  # Left harness point
        harness_r = (10.0, 0.0, 18.0)  # Right harness point

        glColor3f(0.88, 0.88, 0.88)  # Line color
        glBegin(GL_LINES)  # Suspension lines
        line_count = 14  # Number of lines
        for i in range(line_count):  # Loop lines
            phi = (i / line_count) * (2.0 * math.pi)  # Around circle
            scallop = 1.0 + 0.06 * math.sin(phi * line_count)  # Slight wavy edge
            ax = math.cos(phi) * canopy_r * scallop  # Anchor X on rim
            ay = math.sin(phi) * canopy_r * scallop  # Anchor Y
            az = rim_z  # Anchor Z
            hx, hy, hz = harness_l if (i % 2 == 0) else harness_r  # Alternate left/right
            glVertex3f(hx, hy, hz)  # Line start at harness
            glVertex3f(ax, ay, az)  # Line end on canopy rim
        glEnd()  # Finish lines

        glLineWidth(3.0)  # Make risers thicker
        glColor3f(0.75, 0.75, 0.75)  # Riser color
        glBegin(GL_LINES)  # Draw risers
        glVertex3f(harness_l[0], harness_l[1], harness_l[2])  # Left riser start
        glVertex3f(-6.0, 0.0, rim_z - 6.0)  # Left riser end
        glVertex3f(harness_r[0], harness_r[1], harness_r[2])  # Right riser start
        glVertex3f(6.0, 0.0, rim_z - 6.0)  # Right riser end
        glEnd()  # Finish risers
        glLineWidth(1.0)  # Reset line width

        glPushMatrix()  # Save canopy transform
        glTranslatef(0.0, 0.0, rim_z)  # Move canopy to rim height

        panels = 12  # Number of colored panels
        slices = 36  # Angular resolution
        stacks = 9  # Vertical resolution

        for si in range(stacks):  # Build the canopy surface
            theta0 = (si / stacks) * (math.pi / 2.0)  # Lower stack angle
            theta1 = ((si + 1) / stacks) * (math.pi / 2.0)  # Upper stack angle
            r0 = math.cos(theta0) * canopy_r  # Radius at theta0
            r1 = math.cos(theta1) * canopy_r  # Radius at theta1
            z0 = math.sin(theta0) * canopy_h  # Height at theta0
            z1 = math.sin(theta1) * canopy_h  # Height at theta1

            glBegin(GL_TRIANGLE_STRIP)  # Strip between two stack rings
            for sj in range(slices + 1):  # Around full 360 degrees
                phi = (sj / slices) * (2.0 * math.pi)  # Angle
                panel = int((phi / (2.0 * math.pi)) * panels)  # Panel index
                base = (0.92, 0.18, 0.18) if (panel % 2 == 0) else (0.94, 0.94, 0.94)  # Red/white

                shade0 = 0.82 + 0.18 * (z0 / max(0.001, canopy_h))  # Shading lower
                shade1 = 0.82 + 0.18 * (z1 / max(0.001, canopy_h))  # Shading upper

                scallop = 1.0 + 0.06 * math.sin(phi * panels)  # Slight wavy rim

                x0 = math.cos(phi) * r0 * scallop  # X lower
                y0 = math.sin(phi) * r0 * scallop  # Y lower
                x1 = math.cos(phi) * r1  # X upper
                y1 = math.sin(phi) * r1  # Y upper

                glColor3f(base[0] * shade0, base[1] * shade0, base[2] * shade0)  # Color lower
                glVertex3f(x0, y0, z0)  # Vertex lower
                glColor3f(base[0] * shade1, base[1] * shade1, base[2] * shade1)  # Color upper
                glVertex3f(x1, y1, z1)  # Vertex upper
            glEnd()  # Finish strip

        glColor3f(0.20, 0.20, 0.22)  # Rim band color
        glBegin(GL_QUAD_STRIP)  # Rim thickness band
        for sj in range(slices + 1):  # Around circle
            phi = (sj / slices) * (2.0 * math.pi)  # Angle
            scallop = 1.0 + 0.06 * math.sin(phi * panels)  # Rim scallop
            x = math.cos(phi) * canopy_r * scallop  # Rim x
            y = math.sin(phi) * canopy_r * scallop  # Rim y
            glVertex3f(x, y, 0.0)  # Outer rim top
            glVertex3f(x, y, -2.0)  # Outer rim bottom
        glEnd()  # Finish rim strip

        glPopMatrix()  # Restore canopy transform

        glColor3f(0.08, 0.08, 0.10)  # Vent cap color
        glPushMatrix()  # Save
        glTranslatef(0.0, 0.0, rim_z + canopy_h)  # Move to canopy top
        glutSolidSphere(2.2, 10, 10)  # Vent cap sphere
        glPopMatrix()  # Restore

    glPopMatrix()  # Restore player transform

# =============================================================================
# SECTION 23) World drawing (all 3D objects)
# =============================================================================

def draw_world():  # Draw everything in the 3D scene
    draw_stars_and_sun()  # Background stars/sun
    draw_clouds()  # Clouds
    if not jump_started:  # Only show jump marker before jumping
        draw_jump_marker()
    draw_checkered_ground()  # Ground tiles
    draw_landing_target()  # Target board
    draw_player_ground_marker()  # Player ground marker
    draw_trees()  # Trees
    draw_drift_indicator()  # Drift vector
    if game_status != "LANDED":  # Hide plane after landing (optional)
        draw_plane()
    draw_skydiver()  # Player model + parachute

# =============================================================================
# SECTION 24) Camera setup
# =============================================================================

def apply_camera():  # Set camera projection and view depending on camera_mode
    glMatrixMode(GL_PROJECTION)  # Projection matrix
    glLoadIdentity()  # Reset projection
    gluPerspective(fovY, WINDOW_W / WINDOW_H, 0.1, 3000)  # Perspective projection

    glMatrixMode(GL_MODELVIEW)  # Modelview matrix
    glLoadIdentity()  # Reset modelview

    if camera_mode == 0:  # Follow camera
        target_x = player_x - 160  # Camera desired X
        target_y = player_y - 210  # Camera desired Y
        target_z = player_z + 90  # Camera desired Z

        if game_status == "LANDED":  # If landed, stop smoothing
            camera_follow[0] = target_x
            camera_follow[1] = target_y
            camera_follow[2] = target_z
        else:  # Smooth follow in air
            camera_follow[0] += (target_x - camera_follow[0]) * 0.12
            camera_follow[1] += (target_y - camera_follow[1]) * 0.12
            camera_follow[2] += (target_z - camera_follow[2]) * 0.12

        gluLookAt(  # Set camera view
            camera_follow[0], camera_follow[1], camera_follow[2],  # Camera position
            player_x, player_y, player_z,  # Look-at target (player)
            0, 0, 1,  # Up vector
        )

    elif camera_mode == 1:  # Top-down camera
        gluLookAt(
            player_x, player_y, player_z + 320,  # Camera above player
            player_x, player_y, player_z - 50,  # Look down
            0, 1, 0,  # Up vector
        )

    else:  # Free camera
        gluLookAt(
            free_cam_pos[0], free_cam_pos[1], free_cam_pos[2],  # Free camera position
            player_x, player_y, max(0, player_z - 40),  # Look at player/ground
            0, 0, 1,  # Up vector
        )

# =============================================================================
# SECTION 25) Jump + parachute controls
# =============================================================================

def try_deploy_parachute():  # Deploy the parachute
    global parachute_deployed, parachute_open_progress, game_status, jump_started  # Globals we change
    global diving, dive_progress  # Dive state also changes

    if game_status == "LANDED":  # Don’t deploy after landing
        return

    jump_started = True  # If not already, jumping starts
    parachute_deployed = True  # Mark parachute as deployed
    parachute_open_progress = 0.0  # Reset inflation

    diving = False  # Cancel diving when canopy opens
    dive_progress = 0.0  # Reset dive transition

    game_status = "CANOPY"  # Update HUD status


def trigger_jump_or_chute():  # Space/left-click behavior
    global jump_started  # We change jump_started

    if not jump_started:  # If still on plane
        jump_started = True  # Start jump
        return  # Do not deploy chute immediately

    if not parachute_deployed:  # If already jumped but chute not open
        try_deploy_parachute()  # Deploy it now

# =============================================================================
# SECTION 26) Input callbacks
# =============================================================================

def keyboardListener(key, x, y):  # Handle regular keyboard keys
    global camera_mode, wind_on, jump_started  # Globals modified
    global diving  # Dive mode toggle

    if key == b'c':  # Change camera mode
        camera_mode = (camera_mode + 1) % 3
    elif key == b'r':  # Reset game
        reset_game()
    elif key == b' ':  # Space toggles jump/chute
        trigger_jump_or_chute()
    elif key == b'x':  # Toggle dive
        if jump_started and (not parachute_deployed) and game_status != "LANDED":
            diving = not diving
    elif key == b'w' and camera_mode == 2:  # Free cam forward
        free_cam_pos[1] += 30
    elif key == b's' and camera_mode == 2:  # Free cam back
        free_cam_pos[1] -= 30
    elif key == b'a' and camera_mode == 2:  # Free cam left
        free_cam_pos[0] -= 30
    elif key == b'd' and camera_mode == 2:  # Free cam right
        free_cam_pos[0] += 30
    elif key == b'q' and camera_mode == 2:  # Free cam up
        free_cam_pos[2] += 30
    elif key == b'e' and camera_mode == 2:  # Free cam down
        free_cam_pos[2] -= 30
    elif key == b'v':  # Toggle wind from keyboard
        wind_on = not wind_on


def specialKeyListener(key, x, y):  # GLUT special key press handler (arrows)
    active_special_keys.add(key)  # Remember the key is held


def specialKeyUpListener(key, x, y):  # GLUT special key release handler
    if key in active_special_keys:  # If it was recorded
        active_special_keys.remove(key)  # Remove it


def mouseListener(button, state, x, y):  # Mouse click handler
    global wind_on  # We toggle wind

    if state != GLUT_DOWN:  # Only on press
        return

    if button == GLUT_LEFT_BUTTON:  # Left click jump/chute
        trigger_jump_or_chute()
    elif button == GLUT_RIGHT_BUTTON:  # Right click toggles wind
        wind_on = not wind_on

# =============================================================================
# SECTION 27) Landing evaluation (score + crash)
# =============================================================================

def evaluate_landing(impact_speed):  # Decide crash/survive and score points
    global game_status, outcome_text, score, last_impact_speed  # Globals to update

    game_status = "LANDED"  # Mark as landed
    last_impact_speed = impact_speed  # Save impact speed

    dx = player_x - TARGET_CENTER_X  # Distance from target center (x)
    dy = player_y - TARGET_CENTER_Y  # Distance from target center (y)
    drift = math.sqrt(dx * dx + dy * dy)  # Total distance from target center

    if (not parachute_deployed) or impact_speed > 12.0:  # Too fast → crash
        outcome_text = "Crash"  # Outcome string
        score = 0  # No points
        return

    points = 0  # Default points
    if drift <= TARGET_OUTER_RADIUS:  # Only score if inside outer ring
        for i in range(TARGET_RING_COUNT):  # Find which ring
            r = TARGET_INNER_RADIUS + TARGET_RING_STEP * i  # Radius of ring i
            if drift <= r:  # If inside this ring
                points = TARGET_RING_COUNT - i  # Points (10 at center)
                break

    score = points  # Store

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

# =============================================================================
# SECTION 28) Physics update loop (movement + fall)
# =============================================================================

def update_physics(dt=1 / 60):  # Update movement and fall each frame
    global player_x, player_y, player_z, vx, vy, fall_speed  # Globals updated
    global plane_x, plane_y, game_status, jump_started  # More globals
    global parachute_open_progress  # Chute inflation
    global diving, dive_progress  # Dive state
    global world_time  # Time

    world_time += dt  # Advance world time

    if game_status == "LANDED":  # Stop physics after landing
        return

    if not jump_started:  # Before jump, keep player near plane
        player_x = plane_x + 20  # Player attached to plane
        player_y = plane_y  # Player attached to plane
        player_z = plane_z - 10  # Player slightly below plane

        plane_x += 55 * dt  # Plane moves forward
        plane_y += 14 * dt  # Plane moves sideways a bit

        game_status = "ON PLANE"  # HUD status
        return

    plane_x += 90 * dt  # Plane flies away after jump
    plane_y += 24 * dt  # Plane flies away

    if parachute_deployed:  # Can’t dive under canopy
        diving = False
        dive_progress = 0.0
    else:  # Smooth dive transition
        if diving:
            dive_progress += dt * 2.2
        else:
            dive_progress -= dt * 2.6
        dive_progress = clamp(dive_progress, 0.0, 1.0)

    ix = 0  # Input direction X
    iy = 0  # Input direction Y

    if GLUT_KEY_LEFT in active_special_keys:
        ix -= 1
    if GLUT_KEY_RIGHT in active_special_keys:
        ix += 1
    if GLUT_KEY_UP in active_special_keys:
        iy += 1
    if GLUT_KEY_DOWN in active_special_keys:
        iy -= 1

    if ix != 0 or iy != 0:  # Normalize so diagonal isn’t faster
        ln = math.sqrt(ix * ix + iy * iy)
        ix /= ln
        iy /= ln

    if parachute_deployed:  # Under canopy
        max_h_speed = 200.0
        response = 10.0
    else:  # Freefall/dive
        max_h_speed = lerp(220.0, 180.0, dive_progress)  # Drift weaker during dive
        response = lerp(8.0, 6.0, dive_progress)  # Steering response weaker during dive

    desired_vx = ix * max_h_speed  # Desired velocity x from input
    desired_vy = iy * max_h_speed  # Desired velocity y from input

    vx += (desired_vx - vx) * response * dt  # Smoothly steer vx toward target
    vy += (desired_vy - vy) * response * dt  # Smoothly steer vy toward target

    air_damp = 0.988 if parachute_deployed else 0.994  # Damping for stability
    vx *= air_damp  # Apply damping
    vy *= air_damp  # Apply damping

    if parachute_deployed:  # Inflate chute when deployed
        parachute_open_progress += dt * 0.6
        if parachute_open_progress > 1.0:
            parachute_open_progress = 1.0
    else:
        parachute_open_progress = 0.0

    base_drag = FREEFALL_DRAG if parachute_deployed else lerp(FREEFALL_DRAG, DIVE_DRAG, dive_progress)  # Drag
    drag = base_drag + ((PARACHUTE_DRAG - base_drag) * parachute_open_progress)  # Blend with canopy drag

    fall_accel = GRAVITY - (drag * fall_speed)  # Gravity minus drag
    fall_speed += fall_accel * dt  # Integrate speed

    if fall_speed < 0.0:  # Prevent upward fall speed
        fall_speed = 0.0

    if parachute_deployed:
        game_status = "CANOPY"
    else:
        game_status = "DIVE" if dive_progress > 0.55 else "FREEFALL"

    wx, wy = wind_vec if wind_on else (0.0, 0.0)  # Wind vector

    player_x += (vx + wx) * dt  # Update X position
    player_y += (vy + wy) * dt  # Update Y position
    player_z -= fall_speed * dt  # Update altitude (downwards)

    player_x = max(-650, min(650, player_x))  # Clamp X inside world bounds
    player_y = max(-650, min(650, player_y))  # Clamp Y inside world bounds

    if player_z <= 0:  # If reached ground
        impact_speed = fall_speed  # Save impact speed
        player_z = 0  # Clamp to ground
        evaluate_landing(impact_speed)  # Evaluate score/crash

# =============================================================================
# SECTION 29) HUD drawing
# =============================================================================

def draw_hud():  # Draw the heads-up display
    altitude = player_z  # Current altitude
    drift = math.sqrt(player_x * player_x + player_y * player_y)  # Distance from origin

    wind_label = "ON" if wind_on else "OFF"  # Wind label
    chute_label = "DEPLOYED" if parachute_deployed else "NOT DEPLOYED"  # Chute label

    dive_label = "ON" if (game_status != "LANDED" and dive_progress > 0.55 and (not parachute_deployed) and jump_started) else "OFF"  # Dive label

    draw_text(12, 772, f"Altitude: {altitude:6.1f} m")  # Altitude line
    draw_text(12, 746, f"Fall Speed: {fall_speed:5.1f} m/s")  # Fall speed line
    draw_text(12, 720, f"Drift Distance: {drift:6.1f} m")  # Drift line
    draw_text(12, 694, f"Parachute: {chute_label}")  # Chute status line
    draw_text(12, 668, f"Dive (X): {dive_label}")  # Dive status line
    draw_text(12, 642, f"Wind: {wind_label}  Dir=({wind_vec[0]:.1f}, {wind_vec[1]:.1f})")  # Wind line

    camera_name = ["Follow", "Top-Down", "Free"]  # Camera name list
    draw_text(12, 616, f"Camera: {camera_name[camera_mode]} (press C to switch)")  # Camera line
    draw_text(12, 590, f"Status: {game_status}")  # Game status line

    draw_text(12, 20, "Controls: Arrow=Drift | Space/Left Click=Jump, press again to open chute | X=Dive | Right Click=Wind | C=Camera | R=Reset")  # Controls help
    draw_text(12, 48, "Tip: the yellow line shows your drift direction")  # Tip line

    active_c = (0.25, 1.0, 0.35)  # Active key color
    idle_c = (0.55, 0.55, 0.55)  # Idle key color

    draw_text(890, 140, "UP", font=GLUT_BITMAP_8_BY_13, color=active_c if GLUT_KEY_UP in active_special_keys else idle_c)  # Up indicator
    draw_text(850, 120, "LEFT", font=GLUT_BITMAP_8_BY_13, color=active_c if GLUT_KEY_LEFT in active_special_keys else idle_c)  # Left indicator
    draw_text(920, 120, "RIGHT", font=GLUT_BITMAP_8_BY_13, color=active_c if GLUT_KEY_RIGHT in active_special_keys else idle_c)  # Right indicator
    draw_text(885, 100, "DOWN", font=GLUT_BITMAP_8_BY_13, color=active_c if GLUT_KEY_DOWN in active_special_keys else idle_c)  # Down indicator

    if not jump_started:  # Prompt before jump
        draw_text(330, 770, "Press Space or Left Click to jump")
    elif not parachute_deployed:  # Prompt in freefall
        draw_text(350, 770, "Freefall: open the parachute at the right time")

    if game_status == "LANDED":  # Post-landing HUD
        draw_text(370, 760, f"Result: {outcome_text}")
        draw_text(390, 734, f"Impact Speed: {last_impact_speed:4.1f} m/s")
        draw_text(410, 708, f"Points: {score}/10")
        draw_text(345, 682, "Press R for another jump")

# =============================================================================
# SECTION 30) GLUT loop functions (idle + display)
# =============================================================================

def idle():  # Called repeatedly by GLUT
    update_physics(1 / 60)  # Update physics each frame
    glutPostRedisplay()  # Request redraw


def showScreen():  # GLUT display callback
    glViewport(0, 0, WINDOW_W, WINDOW_H)  # Set viewport to full window
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Clear color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear buffers

    draw_sky_gradient_overlay()  # Draw 2D background

    glClear(GL_DEPTH_BUFFER_BIT)  # Clear depth so 3D draws clean
    apply_camera()  # Set camera matrices
    draw_world()  # Draw the full 3D world

    draw_text(760, 770, "Skydiving Emulator")  # Title text
    draw_hud()  # HUD on top

    glutSwapBuffers()  # Swap front/back buffer

# =============================================================================
# SECTION 31) OpenGL initial settings
# =============================================================================

def setup_gl():  # Configure GL states
    glEnable(GL_DEPTH_TEST)  # Enable depth testing
    glDisable(GL_CULL_FACE)  # Don’t cull back faces

    glEnable(GL_BLEND)  # Enable alpha blending
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Standard transparency blending

    glEnable(GL_LINE_SMOOTH)  # Smooth lines
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)  # Highest quality line smoothing

    glEnable(GL_POINT_SMOOTH)  # Smooth points
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)  # Highest quality point smoothing

# =============================================================================
# SECTION 32) Program entry point
# =============================================================================

def main():  # Main function to create window and start GLUT loop
    glutInit()  # Initialize GLUT
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double-buffered, RGB, depth
    glutInitWindowSize(WINDOW_W, WINDOW_H)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    glutCreateWindow(b"Skydiving Emulator")  # Create window

    setup_gl()  # Set GL flags
    reset_game()  # Reset game state

    glutDisplayFunc(showScreen)  # Register display callback
    glutKeyboardFunc(keyboardListener)  # Register keyboard callback
    glutSpecialFunc(specialKeyListener)  # Register special keys (arrows)

    try:  # Some GLUT builds may not expose special key up callback
        glutSpecialUpFunc(specialKeyUpListener)  # Register arrow release callback
    except Exception:
        pass

    glutMouseFunc(mouseListener)  # Register mouse callback
    glutIdleFunc(idle)  # Register idle callback

    glutMainLoop()  # Start event loop


if __name__ == "__main__":  # Standard Python entry check
    main()  # Run the app
