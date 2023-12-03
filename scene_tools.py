import numpy as np
import random
import pickle
from collections import namedtuple

from scene_objects import Field, Object

class scene(namedtuple):
    field: Field
    grid: tuple[int]
    widht: int
    height: int
    fps: int

class obj_params(namedtuple):
    q: float
    m:float
    k:float
    r:float
    width:float
    color: tuple[int]


def _add_objects(
        width: int,
        height: int,
        robot_params: obj_params,
        robots_count: int,
        field: Field
        ) -> list[Object]:
    
    return [
        Object(
            pos=np.array([random.randint(50, width-50), random.randint(50, height-50)], dtype=np.float64),
            **robot_params
        )
        for _ in range(robots_count)
    ]

def _add_grid(
        width: int,
        height: int,
        grid_point_params: obj_params,
        grid: tuple[int],
        ) -> list[Object]:
    
    height_frame = (height - height * 0.9) / 2
    width_frame = (width - width * 0.9) / 2
    return [
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
            for y in range(int(height_frame), height - int(height_frame) + 2, int((height - 2 * height_frame) / grid[1]))
        for x in range(int(width_frame), width - int(width_frame) + 2, int((width - 2 * width_frame) / grid[0]))
    ]

def _add_goals()

def create_field(
        width: int,
        height: int,
        robot_params: obj_params,
        robots_count: int,
        goal_params: obj_params,
        goals_count: int,
        grid_point_params: obj_params,        
        grid: tuple[int],
        ) -> scene:
    
    field = Field()
    _add_robots()
    _add_grid()

    

