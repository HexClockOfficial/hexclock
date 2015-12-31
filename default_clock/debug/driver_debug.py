from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import colorsys
import threading
import re
import math

G_WIDTH = 314.415194029
G_HEIGHT = 283.440063052

W_WIDTH = 314*1
W_HEIGHT = 283*1

S_D1 = 'M 140.0 0.0 L 142.4 17.3 L 127.2 35.0 L 40.3 35.0 L 13.8 12.0 A 35.0 35.0 0 0 0 40.3 0.0 L 140.0 0.0'
S_H = 'M 66.2 219.3 L 69.4 242.3 L 92.6 242.3 L 147.5 179.1 L 144.3 156.1 L 121.1 156.1 L 66.2 219.3'
S_D2 = 'M 140.0 0.0 L 249.6 0 A 35.0 35.0 0 0 0 272.5 8.6 L 249.6 35.0 L 162.6 35.0 L 142.4 17.3 L 140.0 0.0'
S_G2 = 'M 266.6 156.1 L 281.8 138.6 L 261.7 121.1 L 197.9 121.1 L 174.7 121.1 L 159.5 138.6 L 179.6 156.1 L 206.3 156.1 L 266.6 156.1'
S_K = 'M 252.0 242.3 L 278.7 242.3 L 275.0 215.9 L 206.3 156.1 L 179.6 156.1 L 183.3 182.6 L 252.0 242.3'
S_C = 'M 299.5 138.6 L 281.8 138.6 L 261.7 121.1 L 249.6 35.0 L 272.5 8.6 A 35.0 35.0 0 0 0 284.2 30.1 L 299.5 138.6'
S_B = 'M 266.6 156.1 L 281.8 138.6 L 299.5 138.6 L 313.4 237.4 A 35.0 35.0 0 0 0 305.1 265.2 L 278.7 242.3 L 266.6 156.1'
S_J = 'M 156.4 242.3 L 176.5 259.9 L 191.7 242.3 L 183.3 182.6 L 179.6 156.1 L 159.5 138.6 L 144.3 156.1 L 147.5 179.1 L 156.4 242.3'
S_A2 = 'M 278.7 242.3 L 191.7 242.3 L 176.5 259.9 L 179.0 277.3 L 278.7 277.3 A 35.0 35.0 0 0 1 305.1 265.2 L 278.7 242.3'
S_G1 = 'M 52.4 121.1 L 37.2 138.6 L 57.3 156.1 L 121.1 156.1 L 144.3 156.1 L 159.5 138.6 L 139.4 121.1 L 112.7 121.1 L 52.4 121.1'
S_F = 'M 34.7 247.1 L 19.5 138.6 L 37.2 138.6 L 57.3 156.1 L 69.4 242.3 L 46.4 268.7 A 35.0 35.0 0 0 0 34.7 247.1'
S_A1 = 'M 69.4 277.3 L 179.0 277.3 L 176.5 259.9 L 156.4 242.3 L 69.4 242.3 L 46.4 268.7 A 35.0 35.0 0 0 1 69.4 277.3'
S_N = 'M 66.9 35.0 L 40.3 35.0 L 44.0 61.4 L 112.7 121.1 L 139.4 121.1 L 135.6 94.7 L 66.9 35.0'
S_M = 'M 139.4 121.1 L 159.5 138.6 L 174.7 121.1 L 171.5 98.2 L 162.6 35.0 L 142.4 17.3 L 127.2 35.0 L 135.6 94.7 L 139.4 121.1'
S_L = 'M 252.8 58.0 L 249.6 35.0 L 226.4 35.0 L 171.5 98.2 L 174.7 121.1 L 197.9 121.1 L 252.8 58.0'
S_E = 'M 52.4 121.1 L 37.2 138.6 L 19.5 138.6 L 5.6 39.9 A 35.0 35.0 0 0 0 13.8 12.0 L 40.3 35.0 L 52.4 121.1'

segments = [S_A1, S_A2, S_B, S_C, S_D1, S_D2, S_E, S_F, S_G1, S_G2, S_H, S_J, S_K, S_L, S_M, S_N]
segment_colors = [(0, 0, 0)]*16


def push(colors):
    global segment_colors
    segment_colors = [(r/255.0, g/255.0, b/255.0) for (r, g, b) in colors]


def get_intersections((x0, y0), (x1, y1), r0, r1):
    d = math.hypot(x1-x0, y1-y0)
    a = (math.pow(r0, 2) - math.pow(r1, 2) + math.pow(d, 2))/(d*2.0)
    h = math.sqrt(abs(math.pow(r0, 2) - math.pow(a, 2)))

    x2, y2 = x0+((x1-x0)/d)*a, y0+((y1-y0)/d)*a

    x3off, y3off = ((y1-y0)/d)*h, ((x1-x0)/d)*h
    return (x2+x3off, y2-y3off), (x2-x3off, y2+y3off)


def elliptical_arc(s_point, arc):
    split = arc.split(' ')
    r = float(split[1])
    e_point = (float(split[6]), float(split[7]))

    c_a, c_b = get_intersections(s_point, e_point, r, r)
    cx, cy = c_a if int(split[5]) else c_b

    s_angle = math.atan2(s_point[1]-cy, s_point[0]-cx)
    e_angle = math.atan2(e_point[1]-cy, e_point[0]-cx)

    if abs(e_angle-s_angle) > abs(e_angle - (s_angle+math.pi*2.0)):
        s_angle += math.pi*2.0
    if abs(e_angle-s_angle) > abs((e_angle+math.pi*2.0) - s_angle):
        e_angle += math.pi*2.0

    cx -= 2.276636
    cy += 3.082502052

    step = (math.pi*2.0) / 40.0 if (e_angle > s_angle) else (math.pi*2.0) / -40.0
    num_steps = (e_angle-s_angle) / step
    for i in range(1, int(num_steps)):
        x, y = cx + math.cos(s_angle + (i*step))*r, cy + math.sin(s_angle + (i*step))*r
        glVertex2f(float(x), float(y))

    glVertex2f(e_point[0]-2.276636, e_point[1]+3.082502052)


def vertices_from_path_syntax(path):
    commands = re.split('(M\s\S+\s\S+\s)|(L\s\S+\s\S+\s)|(A\s\S+\s\S+\S+\s\S+\s\S+\s\S+\s\S+\s\S+\s)', path)
    commands = filter(None, commands)

    point = ('', '')
    for cmd in commands:
        if cmd[0] == 'M' or cmd[0] == 'L':
            point = cmd.split(' ')[1:3]
            glVertex2f(float(point[0])-2.276636, float(point[1])+3.082502052)
        if cmd[0] == 'A':
            elliptical_arc((float(point[0]), float(point[1])), cmd)


def display():
    global segment_colors
    glClear(GL_COLOR_BUFFER_BIT)

    for i in range(16):
        r, g, b = segment_colors[i]
        glColor3f((r*0.75)+0.25, (g*0.75)+0.25, (b*0.75)+0.25)
        glBegin(GL_POLYGON)
        vertices_from_path_syntax(segments[i])
        glEnd()
        glDisable(GL_DEPTH_TEST)

    glFlush()


def init_thread():
    glutInit()
    glutInitWindowSize(W_WIDTH, W_HEIGHT)
    glutCreateWindow("HEX Debugger")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(display)
    glutIdleFunc(display)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, G_WIDTH, 0.0, G_HEIGHT)

    glutMainLoop()


def init():
    t = threading.Thread(target=init_thread)
    t.start()
