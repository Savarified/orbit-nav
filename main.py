import os
import time
import sys
import math
import pygame
import astropy
from astropy import units as u
from astropy.coordinates import EarthLocation, get_body, ITRS, GCRS
from astropy import constants as const
from astropy.time import Time

os.system('clear')
print('NASA, HOUSTON TX SPACE CENTER, FEB 2 9:00AM')
os.environ['SDL_VIDEO_WINDOW_POS'] = '1400, 0'
pygame.init()
WIDTH, HEIGHT = 600, 400
window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Orbital Navigation System')
pygame.display.set_icon(pygame.image.load('textures/icons/rocket-flight-icon.png'))
font = pygame.font.SysFont('monospace', 16)
clock = pygame.time.Clock()
FPS = 60
run = True
pygame.font.init()

debug_rocket_physics = True
debug_rocket_coordinates = True
timeStep = 10
class Camera():
    def __init__(self, x, y, z, rx, ry, rz):
        self.x = x
        self.y = y
        self.z = z
        self.rx = rx
        self.ry = ry
        self.rz = rz
cam = Camera(0,0,-6000,0,0,0)

solar_system = []
class Body():
    def __init__(self, x, y, z, mass, radius, texture_map, name):
        self.x = x
        self.y = y
        self.z = z
        self.mass = mass
        self.radius = radius
        self.texture_map = pygame.image.load(texture_map)
        self.name = name
        solar_system.append(self)

class Rocket():
    def __init__(self,x,y,z,dx,dy,dz,rx,ry,rz,mass,height,radius,surface_area,stage,fuel,texture_map, name):
        self.x = x
        self.y = y
        self.z = z
        
        self.dx = dx
        self.dy = dy
        self.dz = dz

        self.rx = rx
        self.ry = ry
        self.rz = rz

        self.mass = mass
        self.height = height
        self.radius = radius
        self.surface_area = surface_area

        self.stage = stage
        self.fuel = fuel

        self.texture_map = texture_map

APOLLO_17 = Rocket(0,0,0, 0,0,0, 0,0,0, 48609 + (2.7 * (10**6)), 110.6, 1.95, 1800, 1, 11261, 'textures/apollo17','Apollo 17 SATURN-V Rocket')
#Initialize celestial bodies
earth = Body(0,0,0, 5.9722 * (10**24), 6.378137 * (10**6), 'textures/earth/earth_textTEST.png', 'Earth')
mars = Body(0,0,0, 6.4169 * (10**23), 3.389500 * (10**6), 'textures/mars/mars.png', 'Mars')
def drop_unit(num):
    return float(str(num).split(' ')[0])

class gcs_coordinate():
    def __init__(self, longitude, latitude, altitude):
        self.longitude = longitude * u.deg
        self.latitude = latitude * u.deg
        self.altitude = altitude * u.m

def icrs_to_gcrs(coord, time):
    return coord.transform_to(GCRS(obstime=time))

def distance3D(b1, b2):
    return math.sqrt( (b2.x - b1.x)**2 + (b2.y - b1.y)**2 + (b2.z - b1.z)**2)

G = 6.6743 * (10**-11)
AU = 1.5 * (10**11)
def calculate_gravity(b1, b2):
    d = distance3D(b1, b2)
    return G * (b1.mass * b2.mass)/(d**2)

def update_system_positions(time):
    time = Time('2025-02-02 00:09:00')
    for body in solar_system:
        if ('mars' in body.name.lower()):
            _icrs = get_body('mars', time)
            _gcrs = icrs_to_gcrs(_icrs, time)
            body.x, body.y, body.z = drop_unit(_gcrs.cartesian.x), drop_unit(_gcrs.cartesian.y), drop_unit(_gcrs.cartesian.z)
            body.x, body.y, body.z = body.x*AU, body.y*AU, body.z*AU
def calculate_thrust(mass, mass_flow, velo):
    return float((mass/timeStep) * velo)/mass_flow

ATM_ALT = [0.006161571852060982, -0.18129834839074, 1.5459535573123]
def calculate_atmospheric_drag(altitude, velocity, sa, cd):
    p = ((ATM_ALT[0]*altitude)**2) + (ATM_ALT[1]*altitude) + (ATM_ALT[2])
    cd = 0.75
    drag = (1/2) * p * (velocity**2) * sa * cd
    return float(drag)
path_verts = []
def update_rocket_position():
    #stage I:
    #calculate thrust - drag, find the initial vector, add matrix to coordinate
    thrust = 1200 #n //this value will be calculated
    thrust = calculate_thrust(APOLLO_17.mass, 120000, 56)
    gravity = calculate_gravity(APOLLO_17, earth)

    atm_drag = 0
    alt = distance3D(earth, APOLLO_17) - (earth.radius/1000)
    if(alt < 1000):
        vel = APOLLO_17.dx + APOLLO_17.dy + APOLLO_17.dz
        atm_drag = calculate_atmospheric_drag(alt, vel, APOLLO_17.surface_area, 0.75)
    if (gravity < thrust):thrust -= gravity
    thrust -= atm_drag
    thrust = max(0, thrust)
    
    c_sum = APOLLO_17.x + APOLLO_17.y +APOLLO_17.z
    launch_dir = [APOLLO_17.x/ c_sum, APOLLO_17.y/c_sum, APOLLO_17.z/c_sum]

    APOLLO_17.dx += thrust * launch_dir[0]
    APOLLO_17.dy += thrust * launch_dir[1]
    APOLLO_17.dz += thrust * launch_dir[2]

    APOLLO_17.x += APOLLO_17.dx
    APOLLO_17.y += APOLLO_17.dy
    APOLLO_17.z += APOLLO_17.dz


def gcs_to_gcrs_c(longitude, latitude, altitude):
    earth_loc = EarthLocation.from_geodetic(longitude, latitude, altitude)
    time = Time('2025-02-02 00:09:00')
    itrs = earth_loc.get_itrs(obstime=time)
    gcrs = itrs.transform_to(GCRS(obstime=time))
    return [drop_unit(gcrs.cartesian.y), drop_unit(gcrs.cartesian.x), drop_unit(gcrs.cartesian.z)]

nasa_houston = gcs_coordinate(-95.098228, 29.551811, 50)
launch_site = gcs_to_gcrs_c(nasa_houston.longitude, nasa_houston.latitude, nasa_houston.altitude)
APOLLO_17.x, APOLLO_17.y, APOLLO_17.z = launch_site
print(f'Launch Site (GCRS)[ x:{launch_site[0]} m, Y:{launch_site[1]} m, Z: {launch_site[2]} m ]')

_0, _90, _180, _270, _360 = 0, math.pi * 0.5, math.pi, math.pi*1.5, math.pi*2
def clipCheck(vert):
    return True
    [x,y,z] = vert
    x *= _scale
    y *= _scale
    z *= _scale
    lookDir = (cam.ry/(2*math.pi)) * 360
    lookDir *= (math.pi/180)
    clipPlane = (math.tan(lookDir)*(x-cam.x)) + ((0.1)/math.cos(lookDir))
    
    if(((_270 < lookDir)and(lookDir < _360)) or ((_0 < lookDir)and(lookDir < _90))):
        return ((z-cam.z) >= clipPlane)
    else:
        return ((z-cam.z) < clipPlane)

def rotate(vert):
    x = vert[0] - cam.x
    y = vert[1] - cam.y
    z = vert[2] - cam.z

    cosx, sinx = math.cos(cam.rx), math.sin(cam.rx)
    cosY, sinY = math.cos(cam.ry), math.sin(cam.ry)
    cosZ, sinZ = math.cos(cam.rz), math.sin(cam.rz)

    #z-axis
    x1 = x * cosZ - y * sinZ
    y1 = x * sinZ + y * cosZ
    #y-axis
    x2 = x1 * cosY + z * sinY
    z2 = -x1 * sinY + z * cosY
    #x-axis
    y3 = y1 * cosx - z2 * sinx
    z3 = y1 * sinx + z2 * cosx

    x2 += cam.x 
    y3 += cam.y
    z3 += cam.z 

    return [x2, y3, z3]

EPS = 0.0001
s =  [WIDTH, HEIGHT]
r = [400, 266, 400]
h_s = [WIDTH/2, HEIGHT/2]
_scale = 1 * (10**-4)
def project(vert):
    [x,y,z] = vert
    x *= _scale
    y *= -_scale
    z *= _scale

    [x,y,z] = rotate([x,y,z])

    x -= cam.x 
    y += cam.y 
    z -= cam.z - EPS

    xi = (x * s[0])/(z * r[0]) * r[2]
    yi = (y * s[1])/(z * r[1]) * r[2]

    xi += h_s[0]
    yi += h_s[1]

    return [xi, yi]

def render_sprite(img, r, x, y):
    tex = img
    tex = pygame.transform.scale(tex, (r*2, r*2))
    window.blit(tex, (x-r, y-r))

def debug_dot(point, radius, color):
    pygame.draw.circle(window, color, (point[0], point[1]), radius)

def debug_coordinates():
    for body in solar_system:
        print(f'{body.name} [ x:{body.x} m, y: {body.z} m, z: {body.z} m]')
    print(f'Apollo 17 [ x: {APOLLO_17.x} m, y: {APOLLO_17.y} m, z: {APOLLO_17.z} m]')

def debug_rocket_physics():
    thrust = calculate_thrust(APOLLO_17.mass, 120000, 56)
    gravity = calculate_gravity(APOLLO_17, earth)

    atm_drag = 0
    alt = distance3D(earth, APOLLO_17) - (earth.radius/1000)
    if(alt < 1000):
        vel = APOLLO_17.dx + APOLLO_17.dy + APOLLO_17.dz
        atm_drag = calculate_atmospheric_drag(alt, vel, APOLLO_17.surface_area, 0.75)
    if (gravity < thrust):thrust -= gravity
    thrust -= atm_drag
    thrust = max(0, thrust)
    print(f'Gravitational pull: {gravity}')
    print(f'Atmospheric drag: {atm_drag}')
    print(f'Thrust vector: {thrust}')

def debug_text(txt, x, y, color):
    surf = font.render(str(txt), True, color)
    rect = surf.get_rect()
    rect.left = x
    rect.bottom = y
    window.blit(surf, rect)

def render():
    for body in solar_system: # render celestial bodies
        pt = [body.x,body.y,body.z]
        if(not clipCheck(pt)): continue
        vert = project(pt)
        dist = distance3D(body, cam)
        r = (body.radius)/((dist/20)**2)+1
        render_sprite(body.texture_map, r, vert[0], vert[1])
        #debug_text(body.name, vert[0]+r, vert[1]-r, [255,255,255])
        #debug_dot(vert, r, [255,255,255])

    for vert in path_verts: # render rocket path
        pt = project(vert)
        debug_dot(pt, 1.5, [25,0,255])

    vert = project([APOLLO_17.x, APOLLO_17.y, APOLLO_17.z]) # render rocket
    debug_dot(vert, 1.5, [255,255,255])

cam_controls = [0,0,0,0]
cam_rot_speed = 1/360
def move_camera(cam_controls):
    c = cam_controls
    if (c[0]): cam.rx += cam_rot_speed
    if (c[1]): cam.rx -= cam_rot_speed
    if (c[2]): cam.ry += cam_rot_speed
    if (c[3]): cam.ry -= cam_rot_speed


def quit_app(msg):
    if(msg != ''): print(msg)
    run = False
    pygame.quit()
    sys.exit()

t = 0
j = 0
while run:
    window.fill([0,0,0])
    if(t > 8): 
        t = 0
        path_verts.append([APOLLO_17.x, APOLLO_17.y, APOLLO_17.z])
        if(len(path_verts) > 90): path_verts.remove(path_verts[0])
    j += 1/10
    update_system_positions(Time('2025-02-02 00:09:00'))
    move_camera(cam_controls)
    update_rocket_position()
    render()
    APOLLO_17.dy -= j
    debug_text(round(clock.get_fps()), 0, 20, [255,255,255])
    pygame.display.flip()
    clock.tick(FPS)
    t += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_app('')
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_app('')
            if event.key == pygame.K_x:
                print('Awaiting command')
                command = input()
                args = command.split(' ')
                if('kill' in command): quit_app('Processes terminated manually')
                if('fuel loss' in command): print('Expected fuel loss over 132,016.284 m: \n435,002 kg Aerozine 50 : Nitrogen 1.6:1, 0.2245% capacity left for return mission LEM.') # TEMP
                if('thrust' in command):
                    m, mf, v = float(args[1]), float(args[2]), float(args[3])
                    print(f'Thrust at {m} kg, {mf} kg/s, {v} m/s: {calculate_thrust(m, mf, v)}')
                print('Exitted command mode (x)')
            if event.key == pygame.K_c:
                debug_coordinates()
            if event.key == pygame.K_p:
                debug_rocket_physics()

            if event.key == pygame.K_DOWN:
                cam_controls[0] = True
            if event.key == pygame.K_UP:
                cam_controls[1] = True
            if event.key == pygame.K_LEFT:
                cam_controls[2] = True
            if event.key == pygame.K_RIGHT:
                cam_controls[3] = True
            #if event.key == pygame.K_SPACE:

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                cam_controls[0] = False
            if event.key == pygame.K_UP:
                cam_controls[1] = False
            if event.key == pygame.K_LEFT:
                cam_controls[2] = False
            if event.key == pygame.K_RIGHT:
                cam_controls[3] = False
