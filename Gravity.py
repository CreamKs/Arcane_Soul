def Gravity_World(o):
    if o.y > 90 and o.jump == True:
        d = (9.8 * o.g * 3)
        o.y -= d
        o.g += 0.07
    else:
        o.jump = False
        o.y = 90

