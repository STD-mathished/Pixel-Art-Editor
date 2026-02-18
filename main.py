import pygame
from config import *
import sys 
from PIL import Image

ACTIVE_COLOR = (0,0,0) # BLACK

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pixel Art Editor")
font = pygame.font.SysFont(None, 24)


#Initialize the grid with bg color
grid = []
for row in range(GRID_SIZE):
    grid.append([BG_COLOR] * GRID_SIZE)


# Displays the grid on the screen
def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(
                col * PIXEL_SIZE + MARGIN,
                row * PIXEL_SIZE + MARGIN,
                PIXEL_SIZE -2 * MARGIN,
                PIXEL_SIZE -2 * MARGIN
            )
            pygame.draw.rect(screen, grid[row][col], rect)
            pygame.draw.rect(screen, GRID_LINE_COLOR, rect, 1)


#Displays the palette on the screen
def draw_palette():
    for i, color in enumerate(PALETTE_COLORS):
        rect = pygame.Rect(i * 55 + 5, GRID_SIZE * PIXEL_SIZE + 10, 45, 40)
        pygame.draw.rect(screen, color, rect)
        border_color = (255, 255, 255) if color == ACTIVE_COLOR else (0, 0, 0)
        border_width = 4 if color == ACTIVE_COLOR else 2
        pygame.draw.rect(screen, border_color, rect, border_width)

#Returns the clear button
def draw_clear_button():
    rect = pygame.Rect(WINDOW_WIDTH - 60, GRID_SIZE * PIXEL_SIZE + 15, 50, 30)
    pygame.draw.rect(screen, (240,240,240), rect)
    pygame.draw.rect(screen, (0,0,0), rect, 2)
    text = font.render("Clear", True, (0,0,0))
    text_rect = text.get_rect(center = rect.center)
    screen.blit(text, text_rect)
    return rect

#Clears the sreen
def clear_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            grid[row][col] = BG_COLOR

# Save the grid as a PNG
def export_image(grid, filename="The art.png"):
    image = Image.new("RGB", (GRID_SIZE, GRID_SIZE))
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            image.putpixel((col, row), grid[row][col])
    image = image.resize((GRID_SIZE * 20, GRID_SIZE * 20), Image.NEAREST)
    image.save(filename)
    print("exported successfully !")

clock = pygame.time.Clock()
running = True

while running:

    screen.fill((BG_COLOR))
    draw_grid()
    draw_palette()
    clear_button_rect = draw_clear_button()
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]: # if left click is pressed
            x, y = pygame.mouse.get_pos()
            if y < GRID_SIZE * PIXEL_SIZE:
                col = x // PIXEL_SIZE
                row = y // PIXEL_SIZE
                if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
                    grid[row][col] = ACTIVE_COLOR
            
            # Click on the palette or clear button 
            elif y >= GRID_SIZE * PIXEL_SIZE:
                # Handle Palette click
                for i, color in enumerate(PALETTE_COLORS):
                    rect = pygame.Rect(i * 55 + 5, GRID_SIZE * PIXEL_SIZE + 10, 45, 40)
                    if rect.collidepoint(x,y):
                        ACTIVE_COLOR = color
                    
                # Clear button event
                if clear_button_rect.collidepoint(x,y):
                    clear_grid()

            # SAVE THE IMAGE
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                export_image(grid)


    
    



    pygame.display.flip()
    clock.tick(60)  

pygame.quit()