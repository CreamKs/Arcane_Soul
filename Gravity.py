def Gravity_World(o):
    if o.y > 90:
        d = (9.8 * o.g * 3) / 2
        o.y -= int(d)
        o.g += 0.01
    else:
        o.jump = False
        o.y = 90

