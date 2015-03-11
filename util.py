import math

# Colors
BLACK    = (   0,   0,   0) 
WHITE    = ( 255, 255, 255) 
BLUE     = (   0,   0, 128)
GREEN    = (   0, 128, 0)
RED      = ( 128,   0, 0)

DEG2RAD = 2.0 * math.pi / 360.0

def rad(angle):
    return angle * DEG2RAD

# maybe faster on some systems with weak FP hardware?
cos_table = [0] * 360
for i in range(360):
    cos_table[i] = math.cos(rad(i))

def cos(angle):
    try:
        return cos_table[int(angle % 360)]
    except:
        print("util.cos() of", angle)
def sin(angle):
    try:
        return cos_table[int((angle - 90) % 360)]
    except:
        print("util.sin() of", angle)
