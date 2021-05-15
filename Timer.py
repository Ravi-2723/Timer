import pygame
import time
from notifypy import Notify
from _thread import *

def notifier():
    global timer_started, timer_running, clock_values
    timer_started = False
    timer_running = -1
    clock_values = ['00','00','00']
    
    n = Notify()
    n.title = "Timer"
    n.message = "Timer is over"
    n.audio = 'notification.wav'
    n.icon = 'timer.png'

    n.send()

def timer(start_time, t):
    global clock_values

    while int(time.time()-start_time) != t:
        clock_values[0], clock_values[1], clock_values[2] = atod(t - int(time.time()-start_time))
    else:
        notifier()

def text_renderer(msg, font, rect):
    global surface

    text = font.render(msg, True, AQUA)
    surface.blit(text, rect)

def checker(x, y, m_x, m_y):
    global size
    if x < m_x < x+size[0] and y < m_y < y+size[1]:
        return True
    else:
        return False

def dtoa(clock_values):
    time_in_sec = int(clock_values[0])*3600 + int(clock_values[1])*60 + int(clock_values[2])

    return time_in_sec

def atod(time_in_sec):
    sec = '0'+str(time_in_sec%60)
    sec = sec[len(sec)-2:]
    minutes = time_in_sec//60
    minute = '0' + str(minutes%60)
    minute = minute[len(minute)-2:]
    hour = '0' + str(minutes//60)
    hour = hour[len(hour)-2:]

    return hour, minute, sec

pygame.init()

WIDTH = 500
HEIGHT = 300
FPS = 60

WHITE = (255, 255, 255)
AQUA = (0, 255, 255)
DARK_WHITE = (250, 250, 250)

size = [60, 100]
size_start = [150, 60]
x_start = 250 - size_start[0]//2
y_start = 225 - size_start[1]//2
color_start = WHITE
x = 40
y = 100 - size[1]//2
scroll_count = 0
clock_values = ['00', '00', '00']
timer_running = -1
timer_started = False

surface = pygame.display.set_mode((WIDTH, HEIGHT))
font_n = pygame.font.SysFont('Arial', 85)
font_t = pygame.font.SysFont('Arial', 64)
runLoop = True

while runLoop == True:
    scroll_count = 0
    color_start = WHITE
    click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runLoop = False
        elif event.type == pygame.MOUSEWHEEL:
            scroll_count = event.y
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                click = True

    x_m, y_m = pygame.mouse.get_pos()
   
    for i in range(3):
        if timer_running == -1:
            if checker(x+(i*150), y, x_m, y_m) and scroll_count != 0:
                clock_values[i] = '00'+str(int(clock_values[i])+scroll_count)
                clock_values[i] = clock_values[i][len(clock_values[i])-2:]
            elif checker(x+65+(i*150), y, x_m, y_m) and scroll_count != 0:
                clock_values[i] = '00'+str(int(clock_values[i])+scroll_count)
                clock_values[i] = clock_values[i][len(clock_values[i])-2:]
  
            if i != 0:
                if int(clock_values[i]) > 60:
                    clock_values[i] = '00'
                elif int(clock_values[i]) < 0:
                    clock_values[i] = '60'
            else:
                if int(clock_values[i]) > 24:
                    clock_values[i] = '00'
                elif int(clock_values[i]) < 0:
                    clock_values[i] = '24'
        
    if x_start < x_m < x_start + size_start[0] and y_start < y_m < y_start + size_start[1]:
        color_start = DARK_WHITE
        if click and timer_started == False:
            timer_running = -timer_running
    if timer_running == 1 and timer_started == False:
        start_new_thread(timer, (time.time(), dtoa(clock_values)))
        timer_started = True
        
    surface.fill(AQUA)
    for i in range(3):
        pygame.draw.rect(surface, WHITE, (x+(i*150), y, size[0], size[1]))
        pygame.draw.rect(surface, WHITE, (x+65+(i*150), y, size[0], size[1]))
        text_renderer(clock_values[i][0], font_n, pygame.Rect(x+(i*150)+8, y+5, size[0], size[1]))
        text_renderer(clock_values[i][1], font_n,pygame.Rect(x+65+(i*150)+8, y+5, size[0], size[1]))
                 
    for i in range(2):
        pygame.draw.rect(surface, WHITE, (x+132+(i*150), y+30, 10, 10))
        pygame.draw.rect(surface, WHITE, (x+132+(i*150), y+60, 10, 10))
    
    pygame.draw.rect(surface, color_start, (x_start, y_start, size_start[0], size_start[1]))
    if timer_running != 1:
        text_renderer('Start', font_t, pygame.Rect(x_start+7, y_start-5, size_start[0], size_start[1]))
    elif timer_running == 1:
        text_renderer('Stop', font_t, pygame.Rect(x_start+7, y_start-5, size_start[0], size_start[1]))
    pygame.display.flip()

pygame.quit()
quit()
