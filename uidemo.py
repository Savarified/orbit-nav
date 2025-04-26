#UI Example created with PyGame
#https://www.pygame.org/docs/index.html
import pygame
pygame.init()
window = pygame.display.set_mode((600,400))
font = pygame.font.SysFont('monospace', 16)
title_font = pygame.font.SysFont('monospace', 48)
def render():
    window.fill([0,0,0]) #fills the entire window with a solid color (black in this case)

    #COLORS
    color = [255,0,0]
    shaded_color = [200, 0,0]

    #RECTS
    square = pygame.Rect(30, 30, 400, 60)
    pygame.draw.rect(window, shaded_color, square, border_radius= 10)
    square.left += 10
    square.top += 10
    pygame.draw.rect(window, color, square, border_radius= 10)

    #TEXT
    title = title_font.render('Example Title', True, [255,255,255])
    titleRect = title.get_rect()
    titleRect.top = 45
    titleRect.left = 50
    window.blit(title, titleRect)

    #VECTOR GRAPHICS
    pygame.draw.circle(window, shaded_color, (200, 200), 60)
    pygame.draw.circle(window, color, (200+10, 200+10), 60)

    #IMAGES
    icon = pygame.image.load('textures/icons/rocket-flight-icon.png')
    icon = pygame.transform.scale(icon, (128,128))
    window.blit(icon, (200,200))


# MAIN LOOP
run = True 
while run:
    render()
    pygame.display.flip() #updates the content of the display surface (window) to the screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()