# CSE423 Project — Skydiving + Parachute Landing Simulator (PyOpenGL)

## 1) Project overview
A simple 3D skydiving simulator made using Python + PyOpenGL + GLUT. The player starts on a moving plane, jumps, can freefall or head-down dive, opens a parachute with a realistic inflation delay, and lands on an archery-style target board where scoring depends on landing accuracy and impact speed.

## 2) Platform / tools
- Language: Python 3
- Graphics: PyOpenGL (OpenGL + GLU + GLUT)
- OS: macOS compatible (also cross-platform if PyOpenGL is installed)

## 3) Controls (user-facing)
- Movement (horizontal drift): Arrow keys
- Jump from plane: Space
- Deploy parachute: Left mouse click
- Toggle wind: W
- Toggle dive (head-down): X
- Change camera: C
- Reset / restart: R

## 4) Required gameplay features (final checklist)
- Plane visible + movement clearly understandable
- Jump is separate from parachute opening (cannot auto-open)
- Realistic falling: gravity + drag; speed builds up then approaches terminal velocity
- Parachute inflation is gradual (speed slows down slowly, not instantly)
- Diving feature: head-down mode increases fall rate and reduces steering
- Landing system:
  - Archery-style target rings
  - Rotating visual element at the landing area
  - Points depend on where you land (center = max)
  - Crash condition if impact speed is too high or parachute not deployed
- Parachute looks realistic: canopy inflation + suspension lines
- HUD shows status, speed, altitude, and score/outcome

---


# 5) Member-wise task distribution (2 members)

## Member 1 — Gameplay + logic
- Game flow/state transitions (plane → jump → freefall/dive → parachute → landing)
- Physics realism (gravity, drag/terminal speed, parachute slow-down, dive behavior)
- Input handling (movement, jump, chute, wind toggle, reset/camera)
- Landing rules + scoring (ring-based points, crash vs safe landing)

## Member 2 — Visuals + UI + documentation
- Rendering scene elements (sky, clouds, ground, plane)
- Character + parachute visuals (inflation + lines, dive pose)
- Landing target visuals (rings + rotating indicator, stable drawing/no flicker)
- HUD/text (status, altitude, speed, score)
- Documentation (explained file + built-in function glossary)

---

# 6) Integration plan (how both members combine work)
- Member 1 owns `update_physics()` + all state transitions + scoring calculation
- Member 2 owns drawing functions and HUD rendering
- Integration checkpoints:
  1) Base loop + camera works
  2) Physics + jump + chute logic works
  3) Target + scoring works
  4) Visual polish (parachute, drift marker, target stability)
  5) Documentation finalization

# 7) Deliverables
- Main runnable game file: 3D_OpenGL_Intro.py
- Explained/annotated file: 3D_OpenGL_Intro_explained.py
- Google Doc: member-wise specifications + feature list
- Google Sheet (or section in doc): link to Google Doc + member names
