import curses
from time import sleep
from math import pi, sin, cos, atan, acos
from collections import namedtuple

R1 = 4
R2 = 14

Xi = [x for x in range(-R1, R1 + 1)]
Yi = [(R1 ** 2 - x ** 2) ** (1/2) for x in Xi]
S = []

for i in range(len(Xi)):
    Z = [(Xi[i] + R2) * sin((n/10) * pi / R1) for n in range(0, 20 * R1 + 1)]
    X = [(Xi[i] + R2) * cos((n/10) * pi / R1) for n in range(0, 20 * R1 + 1)]

    for index, (x, z) in enumerate(zip(X, Z)):
        S.append((round(x) + 32, round(z)))

projec = []

for x, z in S:
    for y in Yi:
        projec.append((x, y, z))

def main(window):
    global projec

    Line = namedtuple('Line', 'a b c')

    lines, columns = window.getmaxyx()
    x0, y0 = columns // 2, lines // 2 + 10

    def write(x, y, string):
        xt = x0 + x
        yt = int((y0 + y) * 0.5)

        if 0 < xt < columns:
            x_p = xt
        else:
            return

        if 0 < yt < lines:
            y_p = yt
        else:
            return

        window.addstr(y_p, x_p, string)

    def get_lighting(x, z, y, index):
        xr = x + x0
        yr = y
        zr = (z + y0)  * 0.5

        xp = new_projec[index - 1][0] + x0
        yp = new_projec[index - 1][1]
        zp = (new_projec[index - 1][2] + y0) * 0.5

        xn = new_projec[index - 2][0] + x0
        yn = new_projec[index - 2][1]
        zn = (new_projec[index - 2][2] + y0) * 0.5
        
        arp = xp - xr
        brp = yp - yr
        crp = zp - zr
        
        arn = xn - xr
        brn = yn - yr
        crn = zn - zr
        
        ag = brp * crn - brn * crp
        bg = - (arp * crn - arn * crp)
        cg = arp * brn - arn * brp
        gradient = Line(ag, bg, cg)
        gradient_mod = (ag ** 2 + bg ** 2 + cg ** 2) ** (1/2)

        ad = xl - xr
        bd = yl - yr
        cd = zl - zr
        distance = Line(ad, bd, cd)
        distance_mod = (ad ** 2 + bd ** 2 + cd ** 2) ** (1/2)

        if distance_mod * gradient_mod != 0:
            cos_angle = sum(g * d for g, d in zip(gradient, distance)) / (gradient_mod * distance_mod)
        else:
            cos_angle = 1

        if cos_angle > 1:
            normal = 1
        elif cos_angle < -1:
            normal = -1
        else:
            normal = cos_angle
        
        if normal < 1/12:
            return '.'
        elif 1/12 <= normal < 2/12:
            return ','
        elif 2/12 <= normal < 3/12:
            return '-'
        elif 3/12 <= normal < 4/12:
            return '~'
        elif 4/12 <= normal < 5/12:
            return ':'
        elif 5/12 <= normal < 6/12:
            return ';'
        elif 6/12 <= normal < 7/12:
            return '*'
        elif 7/12 <= normal < 8/12:
            return '!'
        elif 8/12 <= normal < 9/12:
            return '='
        elif 9/12 <= normal < 10/12:
            return '#'
        elif 10/12 <= normal < 11/12:
            return '$'
        elif 11/12 <= normal:
            return '@'

    teta = 0
    alpha = 0
    while True:
        xo = int(1.75*R2)
        yl = 0
        xl = 30
        zl = 0

        l = int(lines * 0.4)

        window.addstr(int(lines * 0.3), int(columns * 0.05), f'ROSQUINHA ROTATÓRIA')
        window.addstr(int(lines * 0.9), int(columns * 0.05), f'Ass: Gustavo Nogueira {chr(0x2764)}')

        new_projec = []
        
        for index, (x, y, z) in enumerate(projec):
            new_x = xo - ((xo - x) * cos(teta) + y * sin(teta))
            new_y = x * sin(teta) + y * cos(teta)
            
            new_z = new_y * sin(alpha) / 2 + z * cos(alpha)
            new_y = new_y * cos(alpha) - z * sin(alpha)      

            new_projec.append((round(new_x), round(new_y), round(new_z)))

        for index, (x, y, z) in enumerate(new_projec):
            write(x, z, get_lighting(x, y, z, index))

        window.refresh()
        window.clear()
        teta += pi/23
        alpha += pi/29

curses.wrapper(main)
