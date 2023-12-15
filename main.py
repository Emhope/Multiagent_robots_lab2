import pygame
import numpy as np
import random
from matplotlib import pyplot as plt

from scene_objects import Field, Object

def calc_robots_area(robots_areas: list[Object], width: int, height: int) -> int:
    areas_surf = pygame.Surface((width, height))
    areas_surf.fill((0, 0, 0))

    for area in robots_areas:
        pygame.draw.circle(
            surface=areas_surf,
            color=area.color,
            center=area.pos,
            radius=area.r,
            width=0
        )
    
    buff = areas_surf.get_buffer()
    pixel_map = np.fromstring(buff.raw, dtype='b').reshape(height, width, 4)[:, :, 0]
    sf = pixel_map != 0
    s = np.sum(sf)
    return(s / (np.pi * robots_areas[0].r ** 2 * len(robots_areas)))

    


def main(width: int = 800, height: int = 600, fps: int = 60, grid: tuple[int] = (10, 10)):

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    
    height_frame = (height - height * 0.9) / 2
    width_frame = (width - width * 0.9) / 2


    field = Field()
    areas_field = Field()

    # creating robots
    robots = [

        Object(
            q=500, # 500
            m=3,
            k=2, # 2
            pos=np.array([random.randint(50, width-50), random.randint(50, height-50)], dtype=np.float64),
            r=5,
            width=4,
            color=(255, 0, 0),
            field=field
        )
    
        for _ in range(random.randint(50, 55))
    ]
    for robot in robots:
        field.append(robot)

    # creating robots areas
    robot_area_r = robots[0].r * 3
    robot_areas = [
        Object(
            q=0, # 500
            m=1000,
            k=1000, # 2
            pos=robot.pos,
            r=robot_area_r,
            width=1,
            color=(255, 0, 255),
            field=field
        )
        for robot in robots
    ]
    for robot_area in robot_areas:
        robot_area_for_surf = robot_area
        areas_field.append(robot_area)
        field.append(robot_area)

    # creating goals
    goals = [
        Object(
            q=-2000,
            m=1000,
            k=1000,
            pos=np.array([random.randint(50, width-50), random.randint(50, height-50)], dtype=np.float64),
            r=25,
            width=4,
            color=(0, 0, 255),
            field=field
        )
    
        for _ in range(random.randint(3,4))
    ]
    for goal in goals:
        field.append(goal)

    # creating areas of goals
    
    area_r = int(goals[0].r + 0.02 * abs(goals[0].q))
    areas = [
        Object(
                q=0,
                m=1000,
                k=1000,
                pos=goal.pos,
                r=area_r,
                width=1,
                color=(0, 255, 0),
                field=field
            )
        for goal in goals
    ]
    for area in areas:
        field.append(area)
    

    # creating grid

    grid = [
        
            Object(
                q=-500,
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
        
            for y in range(int(height_frame), height - int(height_frame) + 2, int((height - 2 * height_frame) / grid[1]))
        for x in range(int(width_frame), width - int(width_frame) + 2, int((width - 2 * width_frame) / grid[0]))
    ]
    for point in grid:
        field.append(point)


    running = True
    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    

        screen.fill((255, 255, 255))

        robots_in_areas = 0

        for robot in robots:
            in_area = False
            for area in areas:
                if robot._approve_force(area):
                    in_area = True
            if in_area:
                robots_in_areas += 1

        for obj in field:
            obj.apply_force(dt=1/fps * 10)
                
        k2 = calc_robots_area(robots_areas=robot_areas, width=width, height=height)
        print(f'k_goals: {round(robots_in_areas / len(robots), 3)}, k_robots: {round(k2, 3)}', end='\r')        

        field.draw(screen, force_line=False)
        pygame.display.flip()


    pygame.quit()


if __name__=='__main__':
    main(
        width=500,
        height=500,
        fps=30,
        grid=(5, 5)
    )