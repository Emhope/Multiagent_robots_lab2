import pygame
import numpy as np



class Field:
    def __init__(self, objects: None | list['Object'] = None) -> None:
        if objects is None:
            self.objects = []
        else:
            self.objects = objects
    
    def __iter__(self):
        return iter(self.objects)
    
    def append(self, obj: 'Object'):
        self.objects.append(obj)
    
    def get_others(self, obj: 'Object'):
        obj_index = self.objects.index(obj)
        return self.objects[: obj_index] + self.objects[obj_index+1:]
    
    def draw(self, screen:pygame.display):
        for obj in self.objects:
            if obj.m < 10:
                obj.draw(screen, force_line=True)
            else:
                obj.draw(screen, force_line=False)



class Object:

    def __init__(
            self, q: float, 
            m:float, 
            k:float, 
            pos: np.ndarray[np.float64], 
            r:float, 
            width:float, 
            color: tuple[int], 
            field: Field
            ) -> None:
        self.q = q
        self.m = m
        self.k = k
        self.v = np.zeros((2,))
        self.f = np.zeros((2,))
        self.pos = pos
        self.field = field
        self.r = r
        self.width = width
        self.color = color
    
    def apply_force(self, dt):
        if self.m > 20:
            return
        
        force = np.zeros((2,))
        for obj in self.field.get_others(self):
            rad_vector = obj.pos - self.pos
            f = abs(self.q * obj.q) / rad_vector ** 2 * np.sign(rad_vector)

            if self.r > abs(rad_vector[0]):
                f[0] *= -1
            if self.r > abs(rad_vector[1]):
                f[1] *= -1

            if self.q > 0 and obj.q > 0 or self.q < 0 and obj.q < 0:
                force -= f
            else:
                force += f
        force *= 1 / self.k
        acceleration = force / self.m
        self.f = force # just for make possible to draw force line at any time
        self.v += acceleration * dt
        self.pos += self.v * dt
        

    def _draw_force_line(self, screen: pygame.display):
        pygame.draw.line(
            surface=screen,
            color=self.color,
            start_pos=self.pos,
            end_pos=self.pos+self.f,
            width=1,
        )

    def draw(self, screen: pygame.display, force_line: bool = False):
        pygame.draw.circle(surface=screen, 
                            color=self.color, 
                            center=self.pos,
                            radius=self.r, 
                            width=self.width,
                            )
        if force_line:
            self._draw_force_line(screen)


        
        

