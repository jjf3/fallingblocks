#created by jjf3

import pygame
import random

# Initialize pygame
pygame.init()

# Set up the game window
window_width = 400
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Falling Block Game")


# Clock to control the frame rate
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255),
RED = (255, 0, 0),
BROWN = (139, 69, 19),
STRAWBERRY = (252, 90, 141),
YELLOW= (255, 255, 0),

# Game variables
block_size = 50
falling_speed = 5
score = 0
lives = 4
level = 1
level_score = 200  # Initial score required to clear a level
score_factor = 2  # Factor to increase the score required to clear a level

# Define the level colors 
level_colors = {
    1: (252, 90, 141), # Level 1: Strawberry
    2: (0, 255, 0),    # Level 2: Green
    3: (0, 0, 255),    # Level 3: Blue
    
}

# Character
character_width = 50
character_height = 50
character_x = (window_width - character_width) // 2
character_y = window_height - character_height

# Load the font
font = pygame.font.Font(None, 36)


# Variables for tracking brown block hits
brown_block_hits = 0
max_brown_block_hits = 3

# Timer for spawning new blocks
spawn_timer = pygame.time.get_ticks()

# Create a list to store the falling blocks
falling_blocks = []

# Game loop
running = True
show_level_message = False # Variable to track if the level message should be shown
level_message_timer = 0  # Timer for level message display
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the window
    window.fill(WHITE)

    # Get the current position of the cursor
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Update the character's position based on the cursor's position
    character_x = mouse_x - character_width // 2
    character_y = mouse_y - character_height // 2

    # Check if it's time to spawn a new falling block
    current_time = pygame.time.get_ticks()
    if current_time - spawn_timer >= 1000:
        spawn_timer = current_time

        # Randomly generate a block type
        block_type = random.choice(['color', 'brown'])
        if block_type == 'color':
            if level == 1:
                block_color = (252, 90, 141) #strawberry color
            else:
                block_color = level_colors.get(level, STRAWBERRY)
            score_value = 10
        else:
            block_color = BROWN
            score_value = -10
            
            # If block_color is still RED, change it to the default strawberry color for level 1
        if block_color == RED and level == 1:
            block_color = (252, 90, 141)  # Strawberry color

        # Randomly generate a block position
        block_x = random.randint(0, window_width - block_size)
        block_y = -block_size

        # Add the block to the falling_blocks list
        falling_blocks.append({'x': block_x, 'y': block_y, 'color': block_color, 'score': score_value})

 # Check if the level is cleared
    if score >= level_score:
        level += 1
        level_score *= score_factor
        falling_speed += 1
        show_level_message = True
        level_message_timer = pygame.time.get_ticks()  # Start the timer

    # Move and draw the falling blocks
    for block in falling_blocks:
        block['y'] += falling_speed
        
      # Get the color based on the current level, or use brown color for brown blocks
        if block['score'] == -10:
            block_color = BROWN
        elif level > 1:
            block_color = level_colors.get(level, RED)
        else:
            block_color = RED

        pygame.draw.rect(window, block_color, (block['x'], block['y'], block_size, block_size))
        
        if block['y'] > window_height:
        falling_blocks.remove(block)

        # Check for collision with the character
        if block['y'] + block_size >= character_y and block['y'] <= character_y + character_height:
            if block['x'] + block_size >= character_x and block['x'] <= character_x + character_width:
                if block['score'] == -10:
                    brown_block_hits += 1
                    if brown_block_hits > max_brown_block_hits:
                        lives -= 1
                        brown_block_hits = 0
                        score = 0
                else:
                    score += block['score']
                falling_blocks.remove(block)
                
                # Check if the level message should be shown
    if show_level_message:
        elapsed_time = pygame.time.get_ticks() - level_message_timer
        if elapsed_time < 3000:  # Show the level message for 3 seconds
            level_message = font.render(f"Level {level}", True, RED)
            level_message_rect = level_message.get_rect(center=(window_width // 2, window_height // 2))
            window.blit(level_message, level_message_rect)
        else:
            show_level_message = False  # Reset the variable

    # Draw the character
    pygame.draw.rect(window, RED, (character_x, character_y, character_width, character_height))

    # Draw the score and lives
    score_text = font.render(f"Score: {score}", True, RED)
    window.blit(score_text, (10, 10))
    lives_text = font.render(f"Lives: {lives}", True, RED)
    window.blit(lives_text, (window_width - lives_text.get_width() - 10, 10))

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)
