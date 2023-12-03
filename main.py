import pygame
import numpy as np
import random

from scene_objects import Field, Object


def main(width: int = 800, height: int = 600, fps: int = 60, grid: tuple[int] = (10, 10)):

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    height_frame = (height - height * 0.5) / 2
    width_frame = (width - width * 0.5) / 2


    field = Field()

    # creating robots
    [
        field.append(
            Object(
                q=50,
                m=3,
                k=2,
                pos=np.array([random.randint(50, width-50), random.randint(50, height-50)], dtype=np.float64),
                r=5,
                width=4,
                color=(255, 0, 0),
                field=field
            )
        )
        for _ in range(random.randint(30, 35))
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
        for _ in range(random.randint(3,4))
    ]

    # creating grid

    [
            field.append(
                Object(
                    q=-100,
                    m=1000,
                    k=1000,
                    pos=np.array(
                        [x, y],
                        dtype=np.float64
                    ),
                    r=5,
                    width=4,
                    color=(0, 0, 255),
                    field=field
                )
            )
            for y in range(int(height_frame), height - int(height_frame) + 2, int((height - 2 * height_frame) / grid[1]))
        for x in range(int(width_frame), width - int(width_frame) + 2, int((width - 2 * width_frame) / grid[0]))
    ]


    
    running = True
    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        screen.fill((255, 255, 255))

        for obj in field:
            obj.apply_force(dt=1/fps * 10)
        field.draw(screen)
        pygame.display.flip()


    pygame.quit()


if __name__=='__main__':
    main(
        width=500,
        height=500,
        fps=30,
        grid=(5, 5)
    )