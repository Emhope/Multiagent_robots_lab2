import pygame
import numpy as np
import random

from scene_tools import Field, Object


def main(width: int = 800, height: int = 600, fps: int = 30):

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))


    field = Field()

    # creating robots
    [
        field.append(
            Object(
                q=100,
                m=1,
                k=2,
                pos=np.array([random.randint(50, width-50), random.randint(50, height-50)], dtype=np.float64),
                r=25,
                width=4,
                color=(255, 0, 0),
                field=field
            )
        )
        for _ in range(random.randint(1, 1))
    ]

    # creating goals
    [
        field.append(
            Object(
                q=-1000,
                m=1000,
                k=1000,
                pos=np.array([random.randint(50, width-50), random.randint(50, height-50)], dtype=np.float64),
                r=25,
                width=4,
                color=(0, 0, 255),
                field=field
            )
        )
        for _ in range(random.randint(1,1))
    ]

    
    running = True
    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        screen.fill((255, 255, 255))

        for obj in field:
            obj.apply_force(dt=1/fps)
        field.draw(screen)
        pygame.display.flip()


    pygame.quit()


if __name__=='__main__':
    main()