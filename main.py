import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Toxic Dodge")

# make the image fit the screen
BG = pygame.transform.scale(pygame.image.load("tdback.jfif"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5
TOXIN_VEL = 3
TOXIC_WIDTH = 10
TOXIC_HEIGHT = 30

FONT = pygame.font.SysFont("Gill Sans", 30)

# doing all the drawing(images, etc) makes the code more organized


def draw(player, elapsed_time, toxins):
    # draws image or whtv onto the the screen
    # bracket for the coordanites for your image
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    # refreshes the drawings on the screen and applies new drawings
    pygame.draw.rect(WIN, "white", player)
    
    for toxin in toxins:
        pygame.draw.rect(WIN, "light blue", toxin)

    pygame.display.update()


def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,
                         PLAYER_WIDTH, PLAYER_HEIGHT)

    # setting up a clock object to maintain the speed of the players movement across all computers
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    # when we should add the next star
    toxic_add_increment = 2000
    toxic_count = 0

    toxins = []
    hit = False

    while run:
        # max num of frames
        toxic_count += clock.tick(100)

        elapsed_time = time.time() - start_time
        
        if toxic_count > toxic_add_increment:
            #add three stars
            for _ in range(3):
                toxic_x = random.randint(0, WIDTH - TOXIC_WIDTH)
                #negative height so that the toxins can fall slightly above the screen 
                toxin = pygame.Rect(toxic_x, -TOXIC_HEIGHT, TOXIC_WIDTH, TOXIC_HEIGHT)
                toxins.append(toxin)
            
            toxic_add_increment = max(200, toxic_add_increment-50)
            toxic_count = 0

        # x button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            # gives a list of the keys the user pressed
        keys = pygame.key.get_pressed()
        # K_LEFT code for left arrow key
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL

        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:

            player.x += PLAYER_VEL
            
        for toxin in toxins[:]:
            toxin.y += TOXIN_VEL
            if toxin.y > HEIGHT:
                toxins.remove(toxin)
            elif toxin.y + toxin.height >= player.y and toxin.colliderect(player):
                toxins.remove(toxin)
                hit = True
                break
        if hit:
            lost_text = FONT.render("YOU LOST!", 1, "white")
            #place the text in the middle of the screen
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2)) 
            pygame.display.update()
            pygame.time.delay(400)
            break
            
        draw(player, elapsed_time, toxins)

    pygame.quit()


if __name__ == "__main__":
    main()
