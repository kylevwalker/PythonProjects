""" File: 120_graphics_proj6.py
    Author: Kyle Walker
    Purpose: An animated graphic of a solar system with recursive
    orbiting planets and moons. The background shows space with stars,
    and in the center is a galaxy with large solar systems orbiting around it.
"""
import graphics
import math
# Window for graphic display
win = graphics.graphics(800, 800, "Animated Graphic")

def bg_stars():
    ''' Creates the star ellipses in the background layer.
        No parameters, returns, or special conditions
        besides the requirement of the opened graphic window.
    '''
    win.rectangle(0, 0, 800, 800, "black")
    win.ellipse(200, 150, 10, 10, "snow")
    win.ellipse(50, 50, 10, 10, "snow")
    win.ellipse(230, 70, 10, 10, "snow")
    win.ellipse(500, 50, 10, 10, "snow")
    win.ellipse(700, 180, 10, 10, "snow")
    win.ellipse(640, 250, 10, 10, "snow")
    win.ellipse(290, 600, 10, 10, "snow")
    win.ellipse(150, 650, 10, 10, "snow")
    win.ellipse(500, 530, 10, 10, "snow")
    win.ellipse(375, 180, 10, 10, "snow")
    win.ellipse(418, 700, 10, 10, "snow")
    win.ellipse(590, 600, 10, 10, "snow")
    win.ellipse(150, 450, 10, 10, "snow")

def orbit(x, y, scale, color, ang):
    ''' A recursive function that creates solar systems that follow
        the orbit paths of the central star. The function recurses until
        the scale is too small, giving layers of orbit around each
        astral body.
        Parameters:
        x = x position of central star determined when calling
        y = y position of central star determined when calling
        scale = scale factor for each body inside of function,
        scale decreases after each pass through recursion
        color: only determines colors of planets, giving each planet
        a unique color when called.
        ang: angle of circle in circle loop, used with sin and cos
        operators to calculate circular positioning of each body in orbit.
        Returns: None
        Pre-Conditions: Opened window, angle of circle must be within (0,360)
        (exlusive)
    '''
    # Creates orbit path lines around each sun/planet
    # This central star is displayed each call, so some orbit collections
    # can appear behind the galaxy's orbit for the illusion of depth

    win.ellipse(x, y, scale, scale, "white")
    win.ellipse(x, y, scale - (scale * .05), scale - (scale * .05), "black")

    # Chooses color based on size to represent star, suns, planets, or moons
    if scale > 200:
        # Massive star
        win.ellipse(x, y, scale - (scale * .4), scale - (scale * .4), "pale turquoise")
        win.ellipse(x, y, scale - (scale * .5), scale - (scale * .5), "azure")
    elif scale > 120:
        # Suns
        win.ellipse(x, y, scale - (scale * .4), scale - (scale * .4), "gold")
        win.ellipse(x, y, scale - (scale * .5), scale - (scale * .5), "light goldenrod")
    elif scale > 50:
        # Planets
        win.ellipse(x, y, scale - (scale * .4), scale - (scale * .4), "DodgerBlue")
        win.ellipse(x, y, scale - (scale * .5), scale - (scale * .5), color)
    elif scale < 50:
        # Moons
        win.ellipse(x, y, scale - (scale * .4), scale - (scale * .4), "khaki1")

    # Uses sine and cosine to draw circular path for orbit
    # Scale decreases for each iteration in recursion
    rot_x = math.cos(ang)
    rot_y = math.sin(ang)
    x = (x + rot_x * (scale * .6))
    y = (y + rot_y * (scale * .6))
    scale = scale - (scale * .6)
    win.ellipse(x, y, scale, scale, "light goldenrod")

    # Breaks recursion after reaching size limit of 20
    if scale > 20:
        orbit(x, y, scale, color, ang * 1.5)

while not win.is_destroyed():
    # Resets angle for circle loop
    ang = 0
    # Repeats pattern of function calls for every angle in the circle,
    # the angle repeats from 0 to 360 until program ends
    while ang < 360:
        win.clear()
        bg_stars()
        rot_x = math.cos(ang * 0.5)
        rot_y = math.sin(ang * 0.5)
        orbit((rot_x * 400) + 400, (rot_y * 250) + 400, 150, "olive drab", ang)
        orbit(400, 400, 300, "pale green", ang)
        orbit(400, 400, 300, "orangeRed2", ang + 180)
        orbit(400, 400, 300, "orchid4", ang + 90)


        orbit((-rot_x * 250) + 400, (-rot_y * 400) + 400, 150, "coral1", ang)
        ang += 0.05
        win.update_frame(30)