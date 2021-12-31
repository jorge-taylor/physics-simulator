#JORGE TAYLOR FINAL CODE - PHYSICS SIMULATOR

#import libraries
import pygame, sys, math, os
from pygame.locals import *

#window size
width = 1920
height = 1080

#window mimimum dimensions
MIN_WIDTH = 1100
MIN_HEIGHT = 800

#colours used in the simulation
white = (250, 250, 250)
grey = (240, 245, 255)
black = (0, 0, 0)
trans = (1, 1, 1)
asphalt = (40, 43, 42)
blue = (10, 125, 150)
dark_blue = (10, 100, 150)
red = (100, 0, 0)
dark_red = (80, 0, 0)
green = (0, 98, 76)
dark_green = (0, 130, 90)
yellow = (212, 185, 12)
purple = (152, 0, 218)

#using theme 1 on startup
#starting theme (colours) used in startup
current_theme = 1
colour1 = asphalt
colour2 = white
colour3 = green
colour4 = dark_green
colour5 = yellow

#screenshots used in startup
pend_ss = pygame.image.load(os.path.join('assets/theme1/pend1.png'))
doub_ss = pygame.image.load(os.path.join('assets/theme1/doub1.png'))
wave_ss = pygame.image.load(os.path.join('assets/theme1/wave1.png'))
sand_ss = pygame.image.load(os.path.join('assets/theme1/sand1.png'))

#initialise pygame modules
pygame.init()
#create a canvas/window to draw upon and make it resizable
canvas = pygame.display.set_mode((width, height), FULLSCREEN)
#set the window caption
pygame.display.set_caption('Physics Simulator')
#create a clock to track time and edit fps
clock = pygame.time.Clock()

#fonts used in the simulation (big, medium and small sizes)
print(pygame.font.get_fonts())
font_b = pygame.font.SysFont('montserrat', 60)
font_m = pygame.font.SysFont('montserrat', 30)
font_s = pygame.font.SysFont('montserrat', 15)

#sub-routine for closing the program
def exit_sim():
    #close pygame
    pygame.quit()
    #exit python
    sys.exit()

#sub-routine for changing themes, works in a cycle and changes the main colours of the program and the main menu images
def themes():
    #use global variables as it is easier to code and we want the colours to change throughout the program regardless
    global current_theme, colour1, colour2, colour3, colour4, colour5, pend_ss, doub_ss, wave_ss, sand_ss

    #theme 1 to 2
    if current_theme == 1:
        #change program colours
        colour1 = asphalt
        colour2 = white
        colour3 = red
        colour4 = dark_red
        colour5 = green
        #update current theme ready for next button press
        current_theme = 2

        #update the main menu simulation images based on the theme
        pend_ss = pygame.image.load(os.path.join('assets/theme2/pend2.png'))
        doub_ss = pygame.image.load(os.path.join('assets/theme2/doub2.png'))
        wave_ss = pygame.image.load(os.path.join('assets/theme2/wave2.png'))
        sand_ss = pygame.image.load(os.path.join('assets/theme2/sand2.png'))

    #theme 2 to 3    
    elif current_theme == 2:
        #change program colours
        colour1 = grey
        colour2 = asphalt
        colour3 = blue
        colour4 = dark_blue
        colour5 = purple
        #update current theme ready for next button press
        current_theme = 3

        #update the main menu simulation images based on the theme
        pend_ss = pygame.image.load(os.path.join('assets/theme3/pend3.png'))
        doub_ss = pygame.image.load(os.path.join('assets/theme3/doub3.png'))
        wave_ss = pygame.image.load(os.path.join('assets/theme3/wave3.png'))
        sand_ss = pygame.image.load(os.path.join('assets/theme3/sand3.png'))

    #theme 3 to 1
    else:
        #change program colours
        colour1 = asphalt
        colour2 = white
        colour3 = green
        colour4 = dark_green
        colour5 = yellow
        #update current theme ready for next button press
        current_theme = 1

        #update the main menu simulation images based on the theme
        pend_ss = pygame.image.load(os.path.join('assets/theme1/pend1.png'))
        doub_ss = pygame.image.load(os.path.join('assets/theme1/doub1.png'))
        wave_ss = pygame.image.load(os.path.join('assets/theme1/wave1.png'))
        sand_ss = pygame.image.load(os.path.join('assets/theme1/sand1.png'))

#function for viewing all the events from the pygame module and handling certain events/taking action where needed
def events(width, height, buttons, sliders, screen):
    global paused
    #takes width of the window, height of the window, any buttons used in that window,
    #any sliders used in that window and the current screen which the user is on as parameters

    #for all pygame events in the system
    for event in pygame.event.get():
        #get the mouse coordinates
        pos = pygame.mouse.get_pos()
        #check for the user quitting the program
        if event.type == QUIT:
            #run the close program sub-routine
            exit_sim()

        #check for the user resizing the window
        elif event.type == VIDEORESIZE:
            #make sure that the screen dimensions are reasonable and not too small
            if event.w < MIN_WIDTH:
                event.w = MIN_WIDTH
            elif event.h < MIN_HEIGHT:
                event.h = MIN_HEIGHT
            #update the screen size
            canvas = pygame.display.set_mode((event.w, event.h), FULLSCREEN)
            #set the current window size equal to our width and height variables
            width = event.w
            height = event.h

        #check for the user clicking
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #check all the buttons on that screen
            for button in buttons:
                #if the click is inside a button
                if button.rect.collidepoint(pos):
                    #then call the buttons action sub-routine
                    button.call_back()

            #if the user is on a simulation screen, then check for slider clicks
            if screen in ['wave', 'pend', 'double', 'sand']:
                #check all the sliders on that screen
                for slider in sliders:
                    #if the click is inside a slider
                    if slider.button_rect.collidepoint(pos):
                        #set slider.hit to be true and therefore update the slider
                        slider.hit = True
                        
        #if the user is on a simulation screen, check for the user not clicking on the slider, so the simulation can be resumed
        if screen in ['wave', 'pend', 'double', 'sand']:
            #check that the user is not clicking
            if event.type == pygame.MOUSEBUTTONUP:
                #for every slider on that screen
                for slider in sliders:
                    #set slider.hit to be false so that the slider no longer tracks the cursor
                    slider.hit = False
                #resume the simulation if the mouse button is not pressed
                paused = False

    #return the dimensions of our screen
    return(width, height)

#sub-routine for drawing buttons to the screen
def button_draw(buttons):
    #accepts the list of buttons from the users screen and displays the buttons to the screen
    
    #goes through all the buttons listed on the screen
    for button in buttons:
        #draw the buttons on the screen
        button.draw()

#sub-routine for drawing sliders to the screen
def slider_draw(sliders):
    #accepts the list of sliders from the users screen and displays the sliders to the screen

    #goes through all the sliders listed on the screen
    for slider in sliders:
        #draw the sliders on the screen
        slider.draw()

#sub-routine for moving and updating the sliders on the screen
def slider_hit(sliders):
    #accepts the list of sliders from the users screen and checks if any have been pressed (slider has been hit)

    #goes through all the sliders listed on the screen
    for slider in sliders:
        #if the slider has been pressed on
        if slider.hit:
            #call the slider move function to update the slider values and graphical display
            slider.move()

#function to create the buttons on the starting screen and append them to a list, buttons
def start_buttons(width, height):
    #accept the width and height of the window as parameters to use for drawing buttons to areas that can scale with the screen

    #create the buttons
    start_button = Button('Start', (width/2, height/3), menu_screen)
    theme_button = Button('Themes', (width/2, height/2.25), themes)
    help_button = Button('Help', (width/2, height/1.8), help_screen)
    quit_button = Button('Quit', (width/2, height/1.5), exit_sim)
    #create a list which stores all the buttons on that screen
    buttons = [start_button, theme_button, help_button, quit_button]
    #return the list of buttons
    return(buttons)

#function to create the buttons on the help screen and append them to a list, buttons
def help_buttons(width, height):
    #accept the width and height of the window as parameters to use for drawing buttons to areas that can scale with the screen

    #create the buttons
    back_button = Button('Back', (100, 30), start_screen)
    #create a list which stores all the buttons on that screen
    buttons = [back_button]
    #return the list of buttons
    return(buttons)

#function to create the buttons on the menu screen and append them to a list, buttons
def menu_buttons(width, height):
    #accept the width and height of the window as parameters to use for drawing buttons to areas that can scale with the screen

    #create the buttons
    back_button = Button('Back', (100, 30), start_screen)
    pendulum_button = Button('Single Pendulum', (width/4, ((height/2-288)/2)+320), pendulum)
    double_button = Button('Double Pendulum', (width/2+width/4, ((height/2-288)/2)+320), double_pendulum)
    wave_button = Button('Waves', (width/4, (height/2+(height/2-288)/2)+320), wave)
    sand_button = Button('Sand Pendulum', (width/2+width/4, (height/2+(height/2-288)/2)+320), sand_pendulum)
    #create a list which stores all the buttons on that screen
    buttons = [back_button, pendulum_button, double_button, wave_button, sand_button]
    #return the list of buttons
    return(buttons)

#function to create the buttons on the information screen and append them to a list, buttons
def info_buttons(width, height):
    #accept the width and height of the window as parameters to use for drawing buttons to areas that can scale with the screen
    
    #create the buttons
    back_button = Button('Back', (100, 30), menu_screen)
    #create a list which stores all the buttons on that screen
    buttons = [back_button]
    #return the list of buttons
    return(buttons)

#function to create the buttons on any of the simulations and append them to a list, buttons
def sim_buttons(width, height):
    #accept the width and height of the window as parameters to use for drawing buttons to areas that can scale with the screen

    #create the buttons
    back_button = Button('Back', (100, 30), menu_screen)
    info_button = Button('More Info', (290, 30), more_info)
    #create a list which stores all the buttons on that screen
    buttons = [back_button, info_button]
    #return the list of buttons
    return(buttons)

#function to create the sliders on the wave simulation and append them to a list, sliders
def wave_sliders(width, height):
    #accept the width and height of the window as parameters to use for drawing sliders to areas that can scale with the screen

    #create the sliders
    thickness = Slider('Thickness', 3, 10, 1, 25)
    freq = Slider('Frequency', 20, 50, 10, 150)
    amplitude = Slider('Amplitude', 100, 250, 20, 275)
    phase = Slider('Phase', 1.5, 4, -1, 400)
    speed = Slider('Speed', 60, 144, 30, 525)
    angular_vel = Slider('Ang Vel', 0.125, 0.2, 0.05, 650)
    #create a list which stores all the sliders on that screen
    sliders = [thickness, freq, amplitude, phase, speed, angular_vel]
    #return the list of sliders
    return(sliders, thickness, freq, amplitude, phase, speed, angular_vel)

#function to create the sliders on the single pendulum simulation and append them to a list, sliders
def pend_sliders(width, height):
    #accept the width and height of the window as parameters to use for drawing sliders to areas that can scale with the screen

    #create the sliders
    r = Slider('Length', height/3, height/2, height/12, 25)
    g = Slider('Gravity', 0.05, 0.3, 0.01, 150)
    #create a list which stores all the sliders on that screen
    sliders = [r, g]
    #return the list of sliders
    return(sliders, r, g)

#function to create the sliders on the double pendulum simulation and append them to a list, sliders
def double_sliders(width, height):
    #accept the width and height of the window as parameters to use for drawing sliders to areas that can scale with the screen

    #create the sliders
    L1 = Slider('Length 1', height/4, height/3, height/8, 25)
    L2 = Slider('Length 2', height/4, height/3, height/8, 150)
    g = Slider('Gravity', 0.05, 0.1, 0.01, 275)
    m1 = Slider('Mass 1', 2.5, 5, 0.1, 400)
    m2 = Slider('Mass 2', 2.5, 5, 0.1, 525)
    #create a list which stores all the sliders on that screen
    sliders = [L1, L2, g, m1, m2]
    #return the list of sliders
    return(sliders, L1, L2, g, m1, m2)

#function for updating and calculating the coordinates of the points on the wave
def update_wave(start_ang, freq, amplitude, phase, angular_vel, thickness):
    #accepts the starting angle, amplitude, phase difference, angular velocity and thickness of the wave as parameters

    #increment the starting angle each main loop so the wave moves
    start_ang += 0.03
    #set the angle equal to the starting angle
    angle = start_ang

    #loops from 0 to the width of the window and increments by the value of the frequency of the wave
    for x in range(0, width, int(freq.val)):
        #calculates the y coordinates given the amplitude and the angle
        y = amplitude.val*math.sin(angle)+height/2
        y2 = amplitude.val*math.cos(angle+phase.val)+height/2
        #run the draw wave function which draws the variable values and the wave
        draw_wave(thickness, freq, amplitude, x, y, y2)
        #increment the value of the angle
        angle += angular_vel.val

    #return our parameter values
    return(start_ang, freq, amplitude, phase, angular_vel, thickness)

#function to update and calculate the values used in the single pendulum simulation
def update_single(t, px, py, r, g, v, c):
    #accepts the angle between the rod and the vertical axis, theta. It also accepts the pivot coordinates,
    #the rod length, the acceleration due to gravity, the angular velocity of the bob and the damping value

    #keep the values of theta 1 and 2 between 0 and 2π
    if t > math.pi*2:
        t -= math.pi*2

    if t < -math.pi*2:
        t += math.pi*2

    #find the new coordinates of the bob
    x = px + r.val * math.sin(t)
    y = py + r.val * math.cos(t)   

    #calculate the angular acceleration and angular velocity of the bob
    a = ((-1 * g.val) / r.val) * math.sin(t)
    v += a
    #add in a factor of damping
    v *= c
    #update the angle theta
    t += v

    #return the angular acceleration, angular velocity, theta, and the coordinates of the bob
    return(a, v, t, x, y)

#function to update and calculate the values used in the double pendulum simulation
def update_double(t1, t2, v1, v2, px, py, L1, L2, g, m1, m2, c):
    #accepts the angular velocities of the bobs, the angles they have from the vertical axis, the pivot coordinates,
    #the rod lengths, the value of acceleration due to gravity, the masses of the bobs and the damping value 

    #keep the values of theta 1 and 2 between 0 and 2π
    if t1 > math.pi*2:
        t1 -= math.pi*2
        
    elif t1 < -math.pi*2:
        t1 += math.pi*2

    elif t2 > math.pi*2:
        t2 -= math.pi*2
        
    elif t2 < -math.pi*2:
        t2 += math.pi*2

    #calculates the bob positions based on the angle theta
    x1 = px + L1.val * math.sin(t1)
    y1 = py + L1.val * math.cos(t1)

    x2 = x1 + L2.val * math.sin(t2)
    y2 = y1 + L2.val * math.cos(t2)

    #calculate the angular acceleration of the bobs
    n = -g.val * (2 * m1.val + m2.val) * math.sin(t1) - m2.val * g.val * math.sin(t1 - 2 * t2) + (-2 * math.sin (t1 - t2) * m2.val) * (v2 * v2 * L2.val + v1 * v1 * L1.val * math.cos(t1 - t2))
    d = L1.val * (2 * m1.val + m2.val - m2.val * math.cos(2 * t1 - 2 * t2))
    a1 = n/d

    n = 2 * math.sin(t1 - t2) * (v1 * v1 * L1.val * (m1.val + m2.val) + g.val * (m1.val + m2.val) * math.cos(t1) + v2 * v2 * L2.val * m2.val * math.cos(t1 - t2))
    d = L2.val * (2 * m1.val + m2.val - m2.val * math.cos(2 * t1 - 2 * t2))
    a2 = n/d

    #update values of angular velocity and the angle theta
    v1 += a1
    v2 += a2
    t1 += v1
    t2 += v2

    #add in a factor of damping
    v1 *= c
    v2 *= c

    #returns angular accelerations, angular velocities, angles from the vertical axis and coordinates of the bobs   
    return(a1, a2, v1, v2, t1, t2, x1, y1, x2, y2)

#sub-routine which draws the wave simualtion and shows the variable values in the system
def draw_wave(thickness, freq, amplitude, x, y, y2):
    #accepts the thickness, frequency and amplitude of the wave aswell as the
    #x coordinate of the point on the wave and the two respective y values (for both waves)

    #create a variable to store the render of the font to
    t = font_s.render(('Circle Thickness: '+str(round(thickness.val))),True,colour2)        
    f = font_s.render(('Frequency: '+str(round(freq.val))),True,colour2)
    a = font_s.render(('Amplitude: '+str(round(amplitude.val))),True,colour2)

    #draw the render to the screen
    canvas.blit(t,(10,60))
    canvas.blit(f,(10,90))
    canvas.blit(a,(10,120))  

    #draw wave to the screen
    pygame.draw.circle(canvas, colour3, (x, int(y)), int(thickness.val), 1)
    pygame.draw.circle(canvas, colour5, (x, int(y2)), int(thickness.val), 1)

#sub-routine which draws the single pendulum simualtion and shows the variable values in the system
def draw_single(t, mx, my, x, y, px, py, radius, r):  
    #accepts the angle theta (angle from the vertical axis to the bob), the mouse coordinates, the bob coordinates,
    #the pivot coordinates, the radius of the bob and the length of the rod

    #create a variable to store the render of the font to
    t = font_s.render(('Angle: '+str(round(math.degrees(t)))),True,colour2)        
    m = font_s.render(('Mouse: ('+str(round(mx))+', '+str(round(my))+')'),True,colour2)
    b = font_s.render(('Bob: ('+str(round(x))+', '+str(round(y))+')'),True,colour2)
    L = font_s.render(('Length: '+str(round(r.val))),True,colour2)

    #draw the render to the screen
    canvas.blit(t,(10,60))
    canvas.blit(m,(10,90))
    canvas.blit(b,(10,120))
    canvas.blit(L,(10,150))

    #draw single pendulum to the screen
    pygame.draw.line(canvas, colour2, (px, py), (x, y), 1)
    pygame.draw.circle(canvas, colour2, (int(x), int(y)), radius)

#sub-routine which draws the double pendulum simualtion and shows the variable values in the system
def draw_double(t1, t2, mx, my, x1, x2, y1, y2, L1, L2, m1, m2, px, py, radius):
    #accepts the angles of the bobs to the vertival axis, the mouse coordinates, the bobs coordinates,
    #the masses of the bobs, the pivot coordinates and the radius size of the bobs

    #create a variable to store the render of the font to
    t1 = font_s.render(('Angle 1: '+str(round(math.degrees(t1)))),True,colour2)
    t2 = font_s.render(('Angle 2: '+str(round(math.degrees(t2)))),True,colour2) 
    m = font_s.render(('Mouse: ('+str(round(mx))+', '+str(round(my))+')'),True,colour2)
    b1 = font_s.render(('Bob 1: ('+str(round(x1))+', '+str(round(y1))+')'),True,colour2)
    b2 = font_s.render(('Bob 2: ('+str(round(x2))+', '+str(round(y2))+')'),True,colour2)
    L1 = font_s.render(('Length 1: '+str(round(L1.val))),True,colour2)
    L2 = font_s.render(('Length 2: '+str(round(L2.val))),True,colour2)
    m1 = font_s.render(('Mass 1: '+str(round(m1.val, 1))),True,colour2)
    m2 = font_s.render(('Mass 2: '+str(round(m2.val, 1))),True,colour2)

    #draw the render to the screen
    canvas.blit(t1,(10, 60))
    canvas.blit(t2,(10, 90))
    canvas.blit(m,(10, 120))
    canvas.blit(b1,(10, 150))
    canvas.blit(b2,(10, 180))
    canvas.blit(L1, (10, 210))
    canvas.blit(L2, (10, 240))
    canvas.blit(m1, (10, 270))
    canvas.blit(m2, (10, 300))

    #draw double pendulum to the screen
    pygame.draw.circle(canvas, colour2, (int(x1), int(y1)), radius)
    pygame.draw.circle(canvas, colour2, (int(x2), int(y2)), radius)
    pygame.draw.line(canvas, colour2, (px, py), (x1, y1), 1)
    pygame.draw.line(canvas, colour2, (x1, y1), (x2, y2), 1)

#function which draws the trail of the second bob by drawing lines between the points where the bob is each frame and stores the values in an array
def update_trail(x2, y2, trail_on, trail):
    #accepts the second bob coordinates, the trail list and whether the trail is on as parameters    

    #if the trail is on
    if trail_on:
        #going through the array one value at a time
        for i in trail:
            #if the it is not the first value in the array
            if i != trail[0]:
                #draw a line between the previous frames value for the bobs coordinates and the current value for the bobs coordinates
                pygame.draw.line(canvas, colour5, (prevx, prevy),(int(i[0]), int(i[1])), 3)
                #set the previous coordinates to the current ones, ready for the next iteration
                prevx = int(i[0])
                prevy = int(i[1])
            #when it is the first value in the array, set the previous coordinates to the current ones (first frame only)
            prevx = int(i[0])
            prevy = int(i[1])

    #save each new cycle of the math for the coordinate position of the bob to new
    new = [x2, y2]
    #append new to our array trail where it can be used in the next cycle
    trail.append(new)

    #keep the trail to 100 elements long to keep a good framerate
    if len(trail) > 100:
        del(trail[0])

#function to check whether an item in a simulation is being interacted with, and move appropriately
def check_drag(mx, my, x, y, radius, paused, item):
    #accpets the mouse coordinates, x and y position of the item being checked, the radius of the item,
    #whether the simulation is currently paused and the variable name of the item

    #check that the mouse coordinates are within the items hitbox (multiplied by 8 to make it easier to drag)
    if mx >= x-(radius*8) and mx <= x+(radius*8):
        if my >= y-(radius*8) and my <= y+(radius*8):
            #for all pygame events in the system
            for event in pygame.event.get():
                #check for the user clicking
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #pause the simulation and choose the appropriate action for the item
                    paused = True
                    item = True
                #check that the user is not clicking
                elif event.type == pygame.MOUSEBUTTONUP:
                    #unpause the simulation
                    paused = False

    #return the paused status and the item which is being checked
    return(paused, item)

#sub-routine which runs to start the start screen loop which displays the initial screen                      
def start_screen():
    #set the width and height to be global
    global width, height
    #set our current screen to be the starting screen
    screen = 'start'

    #run indefinitely
    while True:
        
        #fill in the background
        canvas.fill(colour1)
        #create our buttons for the start screen
        buttons = start_buttons(width, height)
        #draw the start screen buttons
        button_draw(buttons)
        #create a render for the title of the program and assign a variable to it
        text = font_b.render(('Physics Simulator'), True, colour2)
        #display the render to the screen
        canvas.blit(text,(width/2-text.get_width()/2, height/8))
        #check all pygame events
        width, height = events(width, height, buttons, None, screen)
        #update the display
        pygame.display.flip()
        #run at 144 frames per second
        clock.tick(144)

#sub-routine which runs to start the help screen loop which displays help screen information 
def help_screen():
    #set the width and height to be global
    global width, height
    #set our current screen to be the help screen
    screen = 'help'

    #run indefinitely
    while True:
        
        #fill in the background
        canvas.fill(colour1)
        #create our buttons for the help screen
        buttons = help_buttons(width, height)
        #draw the help screen buttons
        button_draw(buttons)
        
        #create a render for the help screen information
        text = font_b.render(('Help'), True, colour2)
        text2 = font_m.render(('Welcome to the physics simulator!'), True, colour2)
        text3 = font_m.render(('This program is relatively simple to use, but'), True, colour2)
        text4 = font_m.render(('here are a few instructions to get you started.'), True, colour2)
        text5 = font_m.render(('Once you choose a simulation in the main menu,'), True, colour2)
        text6 = font_m.render(('you can manipulate your chosen system by '), True, colour2)
        text7 = font_m.render(('changing certain variables such as gravity or'), True, colour2)
        text8 = font_m.render(('the mass of an object. Changing variables'), True, colour2)
        text9 = font_m.render(('alters the system in different ways. Just go'), True, colour2)
        text10 = font_m.render(('into a simulation and have a play with them!'), True, colour2)

        #display the renders to the screen
        canvas.blit(text,(width/2-text.get_width()/2, height/15))
        canvas.blit(text2,(width/2-text2.get_width()/2, 200))
        canvas.blit(text3,(width/2-text3.get_width()/2, 300))
        canvas.blit(text4,(width/2-text4.get_width()/2, 350))
        canvas.blit(text5,(width/2-text5.get_width()/2, 400))
        canvas.blit(text6,(width/2-text6.get_width()/2, 450))
        canvas.blit(text7,(width/2-text7.get_width()/2, 500))
        canvas.blit(text8,(width/2-text8.get_width()/2, 550))
        canvas.blit(text9,(width/2-text9.get_width()/2, 600))
        canvas.blit(text10,(width/2-text10.get_width()/2, 650))

        #check all the pygame events
        width, height = events(width, height, buttons, None, screen)
        #update the display
        pygame.display.flip()
        #run at 144 frames per second
        clock.tick(144)

def menu_screen():
    #set the width and height to be global
    global width, height
    #set the current screen to the menu screen
    screen = 'menu'

    #run indefinitely
    while True:
        
        #fill in the background
        canvas.fill(colour1)
        #create our buttons for the menu screen 
        buttons = menu_buttons(width, height)
        #draw the menu screen buttons
        button_draw(buttons)

        #display pendulum, double pendulum, wave and sand pendulum images (these scale with the dimensions of the screen)
        pygame.draw.rect(canvas, black, (width/4-256, (height/2-288)/2, 512+4, 288+4))
        canvas.blit(pend_ss, ((width/4-256)+2, ((height/2-288)/2)+2))
        pygame.draw.rect(canvas, black, (width/2+width/4-256, (height/2-288)/2, 512+4, 288+4))
        canvas.blit(doub_ss, ((width/2+width/4-256)+2, ((height/2-288)/2)+2))
        pygame.draw.rect(canvas, black, (width/4-256, height/2+(height/2-288)/2, 512+4, 288+4))
        canvas.blit(wave_ss, ((width/4-256)+2, (height/2+(height/2-288)/2)+2))
        pygame.draw.rect(canvas, black, (width/2+width/4-256, height/2+(height/2-288)/2, 512+4, 288+4))
        canvas.blit(sand_ss, ((width/2+width/4-256)+2, (height/2+(height/2-288)/2)+2))

        #check all the pygame events
        width, height = events(width, height, buttons, None, screen)
        #update the display
        pygame.display.flip()
        #run at 144 frames per second
        clock.tick(144)

def more_info():
    #set the width and height to be global
    global width, height
    #set the current screen to the information screen
    screen = 'info'
    
    #run indefinitely
    while True:
        
        #fill in the background
        canvas.fill(colour1)
        #create our buttons for the info screen 
        buttons = info_buttons(width, height)
        #draw the info screen buttons
        button_draw(buttons)

        #create a render for the info screen information
        text = font_b.render(('More Information'), True, colour2)
        text2 = font_m.render(('Waves'), True, colour2)
        text3 = font_s.render(('This is a simple wave simulator which is used to explore the nature of a wave. For example you'), True, colour2)
        text4 = font_s.render(('can look at how changing the wavelength, frequency and amplitude (for example) alters the pattern'), True, colour2)
        text5 = font_s.render(('of the wave. It is useful to use this to visualise waves and their changing properties.'), True, colour2)
        text6 = font_m.render(('Single Pendulum'), True, colour2)
        text7 = font_s.render(('This is a simple pendulum simulator which works by looking at the acceleration of the bob, to'), True, colour2)
        text8 = font_s.render(('calculate the coordinates of the bob (similar to double pendulum). You can modify gravity'), True, colour2)
        text9 = font_s.render(('and the length of the rod, as well as dragging the pendulum to change the starting position'), True, colour2)
        text10 = font_m.render(('Double/Sand Pendulum'), True, colour2)
        text11 = font_s.render(('This simulation is chaotic which means different initial conditions will cause the bobs to take'), True, colour2)
        text12 = font_s.render(('a unique path. You can change parameters in the simulation such as mass or gravity and you can'), True, colour2)
        text13 = font_s.render(('drag the pendulum with your mouse to change the starting position. The differrence between this'), True, colour2)
        text14 = font_s.render(('and the sand pendulum is that the sand pendulum loses mass over time (in bob 2) like an hourglass.'), True, colour2)

        #display the renders to the screen
        canvas.blit(text,(width/2-text.get_width()/2, height/15))
        canvas.blit(text2,(width/2-text2.get_width()/2, 150))
        canvas.blit(text3,(width/2-text3.get_width()/2, 200))
        canvas.blit(text4,(width/2-text4.get_width()/2, 250))
        canvas.blit(text5,(width/2-text5.get_width()/2, 300))
        canvas.blit(text6,(width/2-text6.get_width()/2, 350))
        canvas.blit(text7,(width/2-text7.get_width()/2, 400))
        canvas.blit(text8,(width/2-text8.get_width()/2, 450))
        canvas.blit(text9,(width/2-text9.get_width()/2, 500))
        canvas.blit(text10,(width/2-text10.get_width()/2, 550))
        canvas.blit(text11,(width/2-text11.get_width()/2, 600))
        canvas.blit(text12,(width/2-text12.get_width()/2, 650))
        canvas.blit(text13,(width/2-text13.get_width()/2, 700))
        canvas.blit(text14,(width/2-text14.get_width()/2, 750))

        #check all the pygame events
        width, height = events(width, height, buttons, None, screen)
        #update the display
        pygame.display.flip()
        #run at 144 frames per second
        clock.tick(144) 

def wave():
    #set the width and height to be global
    global width, height
    #set the current screen to the wave screen
    screen = 'wave'

    #create our starting variables
    start_ang = 0

    #create the sliders
    sliders, thickness, freq, amplitude, phase, speed, angular_vel = wave_sliders(width, height)      

    #run indefinitely
    while True:
        
        #fill in the background
        canvas.fill(colour1)
        #create our buttons for the wave
        buttons = sim_buttons(width, height)
        #draw the wave buttons
        button_draw(buttons)
        #draw the wave sliders
        slider_draw(sliders)
        
        #update the wave values
        start_ang, freq, amplitude, phase, angular_vel, thickness = update_wave(start_ang, freq, amplitude, phase, angular_vel, thickness)

        #check all the pygame events
        width, height = events(width, height, buttons, sliders, screen)
        #check for any sliders that have been pressed
        slider_hit(sliders)
        #update the display
        pygame.display.flip()
        #run the simulation at the designated frames per second
        clock.tick(speed.val)

def pendulum():
    #set the width and height to be global
    global width, height, paused
    #set the current screen to the pendulum screen
    screen = 'pend'
    
    #establish the variables in the system
    moving_pivot = False
    moving_bob = False
    paused = False
    t = math.pi/2
    v = 0
    radius = 8
    c = 0.9999
    trail = []
    trail_on = True
    px = width/2
    py = height/3

    #create the sliders
    sliders, r, g = pend_sliders(width, height)

    #run indefinitely
    while True:
        
        #find the mouse coordinates
        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1]

        #if the simulation is paused
        if paused:
            #turn the trail off
            trail_on = False
            #set the trail list to be empty
            trail = []
            #set the velocity of the bob to be 0; so it starts from rest
            v = 0

            #if you are moving the bob
            if moving_bob:
                #calculate the difference in x and y from the pivot
                dx = mx - px
                dy = my - py
                #calculate the angle which the rod should be at
                t = math.atan2(dx, dy)       

            #if you are moving the pivot
            elif moving_pivot:
                #set the pivot coordinates equal to the mouse coordinates
                px = mx
                py = my

        #update the variables for the simulation
        a, v, t, x, y = update_single(t, px, py, r, g, v, c)

        #if the simulation is not paused
        if not paused:
            #unpause the bob and pivot, turn the trail back on and update the simulation
            moving_bob = False
            moving_pivot = False
            trail_on = True
            a, v, t, x, y = update_single(t, px, py, r, g, v, c)

        #fill in the background
        canvas.fill(colour1)
        #create our buttons for the pendulum
        buttons = sim_buttons(width, height)
        #draw the pendulum buttons
        button_draw(buttons)
        #draw the pendulum sliders
        slider_draw(sliders)

        #draw and save trail
        update_trail(x, y, trail_on, trail)
        #draw pendulum
        draw_single(t, mx, my, x, y, px, py, radius, r)
        
        #checking for the user dragging the bob or pivot
        paused, moving_bob = check_drag(mx, my, x, y, radius, paused, moving_bob)
        paused, moving_pivot = check_drag(mx, my, px, py, radius, paused, moving_pivot) 
        #check all the pygame events         
        width, height = events(width, height, buttons, sliders, screen)
        #check for any sliders that have been pressed
        slider_hit(sliders)
        #update the display
        pygame.display.flip()
        #run the simulation at 144 frames per second
        clock.tick(144)

def double_pendulum():
    #set the width and height to be global
    global width, height, paused
    #set the current screen to the double pendulum screen
    screen = 'double'
    
    #establish the variables in the system
    paused = False
    moving_bob1 = False
    moving_bob2 = False
    moving_pivot = False
    t1 = math.pi/2
    t2 = math.pi/2
    v1 = 0
    v2 = 0
    radius = 8
    c = 0.9999
    trail = []
    trail_on = True
    px = width/2
    py = height/8

    #create the sliders
    sliders, L1, L2, g, m1, m2 = double_sliders(width, height)

    #run indefinitely
    while True:
        
        #find the mouse coordinates
        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1]

        #if the simulation is paused
        if paused:
            #turn the trail off
            trail_on = False
            #set the trail list to be empty
            trail = []
            #set the velocity of the bobs to be 0; so the system starts from rest
            v1 = 0
            v2 = 0

            #if you are moving the bob                
            if moving_bob1:
                #calculate the difference in x and y from the pivot
                dx = mx - px
                dy = my - py
                #calculate the angle which rod 1 should be at
                t1 = math.atan2(dx, dy)

            elif moving_bob2:
                #calculate the difference in x and y from the first bob
                dx2 = mx - x1
                dy2 = my - y1
                #calculate the angle which rod 2 should be at
                t2 = math.atan2(dx2, dy2)

            #if you are moving the pivot
            elif moving_pivot:
                #set the pivot coordinates equal to the mouse coordinates
                px = mx
                py = my

            #update the variables for the simulation
            a1, a2, v1, v2, t1, t2, x1, y1, x2, y2 = update_double(t1, t2, v1, v2, px, py, L1, L2, g, m1, m2, c)

        #if the simulation is not paused    
        if not paused:
            #unpause the bobs and pivot, turn the trail back on and update the simulation
            moving_bob1 = False
            moving_bob2 = False
            moving_pivot = False
            trail_on = True
            a1, a2, v1, v2, t1, t2, x1, y1, x2, y2 = update_double(t1, t2, v1, v2, px, py, L1, L2, g, m1, m2, c)

        #fill in the background
        canvas.fill(colour1)
        #create our buttons for the double pendulum
        buttons = sim_buttons(width, height)
        #draw the double pendulum buttons
        button_draw(buttons)
        #draw the double pendulum sliders
        slider_draw(sliders) 
               
        #draw and save trail
        update_trail(x2, y2, trail_on, trail)
        #draw simulation
        draw_double(t1, t2, mx, my, x1, x2, y1, y2, L1, L2, m1, m2, px, py, radius)

        #checking for the user dragging the bob or pivot
        paused, moving_bob1 = check_drag(mx, my, x1, y1, radius, paused, moving_bob1)
        paused, moving_bob2 = check_drag(mx, my, x2, y2, radius, paused, moving_bob2)
        paused, moving_pivot = check_drag(mx, my, px, py, radius, paused, moving_pivot)       
        #check all the pygame events 
        width, height = events(width, height, buttons, sliders, screen)
        #check for any sliders that have been pressed
        slider_hit(sliders)
        #update the display
        pygame.display.flip()
        #run the simulation at 144 frames per second
        clock.tick(144)

def sand_pendulum():
    #set the width and height to be global
    global width, height, paused
    #set the current screen to be the sand pendulum screen
    screen = 'sand'
    
    #establish the variables in the system
    paused = False
    moving_bob1 = False
    moving_bob2 = False
    moving_pivot = False
    t1 = math.pi/2
    t2 = math.pi/2
    v1 = 0
    v2 = 0
    radius = 8
    c = 0.9999
    trail = []
    trail_on = True
    px = width/2
    py = height/8

    #create the sliders
    sliders, L1, L2, g, m1, m2 = double_sliders(width, height)

    #run indefinitely
    while True:
        
        #find the mouse coordinates
        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1]

        #if the simulation is paused
        if paused:
            #turn the trail off
            trail_on = False
            #set the trail list to be empty
            trail = []
            #set the velocity of the bobs to be 0; so the system starts from rest
            v1 = 0
            v2 = 0

            #if you are moving the bob                
            if moving_bob1:
                #calculate the difference in x and y from the pivot
                dx = mx - px
                dy = my - py
                #calculate the angle which rod 1 should be at
                t1 = math.atan2(dx, dy)

            elif moving_bob2:
                #calculate the difference in x and y from the first bob
                dx2 = mx - x1
                dy2 = my - y1
                #calculate the angle which rod 2 should be at
                t2 = math.atan2(dx2, dy2)

            #if you are moving the pivot
            elif moving_pivot:
                #set the pivot coordinates equal to the mouse coordinates
                px = mx
                py = my

            #update the variables for the simulation
            a1, a2, v1, v2, t1, t2, x1, y1, x2, y2 = update_double(t1, t2, v1, v2, px, py, L1, L2, g, m1, m2, c)

        #if the simulation is not paused    
        if not paused:
            #unpause the bobs and pivot, turn the trail back on and update the simulation
            moving_bob1 = False
            moving_bob2 = False
            moving_pivot = False
            trail_on = True

            #decrease the mass of the second bob to imitate the sand dripping out the bob (like an hourglass)
            m2.val -= 0.001           
            if m2.val < 0.1:
                m2.val = 0.1
            
            a1, a2, v1, v2, t1, t2, x1, y1, x2, y2 = update_double(t1, t2, v1, v2, px, py, L1, L2, g, m1, m2, c)

        #fill in the background
        canvas.fill(colour1)
        #create our buttons for the sand pendulum
        buttons = sim_buttons(width, height)
        #draw the sand pendulum buttons
        button_draw(buttons)
        #draw the sand pendulum sliders
        slider_draw(sliders) 
               
        #draw and save trail
        update_trail(x2, y2, trail_on, trail)
        #draw simulation
        draw_double(t1, t2, mx, my, x1, x2, y1, y2, L1, L2, m1, m2, px, py, radius)

        #checking for the user dragging the bob or pivot
        paused, moving_bob1 = check_drag(mx, my, x1, y1, radius, paused, moving_bob1)
        paused, moving_bob2 = check_drag(mx, my, x2, y2, radius, paused, moving_bob2)
        paused, moving_pivot = check_drag(mx, my, px, py, radius, paused, moving_pivot)       
        #check all the pygame events 
        width, height = events(width, height, buttons, sliders, screen)
        #check for any sliders that have been pressed
        slider_hit(sliders)
        #update the display
        pygame.display.flip()
        #run the simulation at 144 frames per second
        clock.tick(144)

class Button():
    def __init__(self, txt, location, action):
        #generating the object 'Button' with the text on the button, the coordinates of
        #the button and the action that the button carries out when clicked

        #background, size and text on the button
        self.bg = colour3
        self.size = (180, 40)
        self.txt = txt
        
        #creating a new surface for the button and calculating text coordinates
        self.txt_surf = font_s.render(self.txt, 1, colour2)
        self.txt_rect = self.txt_surf.get_rect(center=[s//2 for s in self.size])
        self.surface = pygame.surface.Surface(self.size)
        self.rect = self.surface.get_rect(center=location)
        self.call_back_ = action

    def draw(self):
        #setting the blackground to white and grey when the mouse is hovering over the button
        self.bg = colour3
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = colour4

        #drawing the button
        self.surface.fill(self.bg)
        self.surface.blit(self.txt_surf, self.txt_rect)
        canvas.blit(self.surface, self.rect)

    def call_back(self):
        #calling the function/action
        self.call_back_()
            
class Slider():
    def __init__(self, name, val, maxi, mini, x):
        #generating the object 'Slider' with the name of the slider, the starting value,
        #the maximum value, minimum value and the x coordinate of the slider (y is fixed)

        #starting value, maximum value, minimum value, x coordinate, y coordinate,
        #surface for the slider to be drawn on and whether the slider is held
        self.val = val  
        self.maxi = maxi  
        self.mini = mini 
        self.x = x  
        self.y = height-75
        self.surf = pygame.surface.Surface((100, 50))
        self.hit = False 

        #creating a new surface for the slider, finding the centre for the text and filling it
        self.txt_surf = font_s.render(name, 1, colour2)
        self.txt_rect = self.txt_surf.get_rect(center = (50, 15))
        self.surf.fill(colour1)

        #drawing the slider background and blitting the background and text
        pygame.draw.rect(self.surf, colour2, [10, 30, 80, 5], 0)
        self.surf.blit(self.txt_surf, self.txt_rect)

        #creating a new surface for the slider button, and drawing it
        self.button_surf = pygame.surface.Surface((20, 20))
        self.button_surf.fill(trans)
        self.button_surf.set_colorkey(trans)
        pygame.draw.circle(self.button_surf, black, (10, 10), 8, 0)
        pygame.draw.circle(self.button_surf, colour3, (10, 10), 6, 0)

    def draw(self):
        #controls how the slider is updated when interacted with
        surf = self.surf.copy()
        pos = (10+int((self.val-self.mini)/(self.maxi-self.mini)*80), 33)
        self.button_rect = self.button_surf.get_rect(center = pos)
        surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.x, self.y) 
        canvas.blit(surf, (self.x, self.y))

    def move(self):
        #controls the limits of the slider and where the slider moves to when dragged
        self.val = (pygame.mouse.get_pos()[0] - self.x - 10) / 80 * (self.maxi - self.mini) + self.mini
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi

start_screen()

