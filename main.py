import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TIMED_MISSION
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import sys

def main():
    pygame.init()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)
    asteroid_field = AsteroidField()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    clock = pygame.time.Clock()
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    main_player = Player(x, y)
    timer = TIMED_MISSION
    game_over = False


    dt = 0

    font = pygame.font.Font(None, 64)
    font2 = pygame.font.Font(None, 32)
    game_over_text = font.render("Game over", True, (255, 255, 255))
    over_text_pos = game_over_text.get_rect(centerx=background.get_width() / 2, y = background.get_height() / 2)



    while True:
        if game_over == False:
            if int(timer) == 210:
                game_over = True

            log_state()
            screen.blit(background, (0, 0))
            for d in drawable:
                d.draw(screen)

            updatable.update(dt)
            for asteroid in asteroids:
                if asteroid.collides_with(main_player):
                    log_event("player_hit")
                    print("Game over!")
                    game_over = True
                    break
            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collides_with(shot):
                        log_event("asteroid_shot")
                        shot.kill()
                        asteroid.split()
                        main_player.score += 1
            timer -= clock.get_time() / 1000
            dt = clock.tick(60) / 1000
            timer_text = font2.render(f"{int(timer)}", True,  (10, 10, 10))
            timer_text_pos = timer_text.get_rect(centerx=background.get_width() / 2, y = 10)
            screen.blit(timer_text, timer_text_pos)
        else:
            score_text = font2.render(f"{main_player.score}", True, (255, 255, 255))
            score_text_pos = score_text.get_rect(centerx=background.get_width() / 2, y = (background.get_height() / 2) + 64 )
            screen.blit(background, (0, 0))
            background.blit(game_over_text, over_text_pos)
            background.blit(score_text, score_text_pos)
            game_over = True
            


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        pygame.display.flip()


    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")


if __name__ == "__main__":
    main()
