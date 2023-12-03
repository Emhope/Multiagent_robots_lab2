import pygame
import numpy as np



def crop_vector(vector: np.ndarray, max_len:float):
    vec_len = np.linalg.norm(vector)
    if vec_len > max_len:
        unit_vec = vector / np.linalg.norm(vector)
        return unit_vec * max_len
    return vector


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
    
    def get_roy(self) -> tuple['Object']:
        return tuple(obj for obj in self.objects if obj.m < 20)
    
    def get_roy_centre(self):
        roy = self.get_roy()
        roy_poses = np.array([obj.pos for obj in roy])
        return roy_poses.mean(axis=0)
    
    def get_roy_q(self):
        roy = self.get_roy()
        return sum(map(lambda obj: obj.q, roy))

    
    def draw(self, screen:pygame.display):
        for obj in self.objects:
            if obj.m < 10:
                obj.draw(screen, force_line=True)
            else:
                obj.draw(screen, force_line=False)



class Object:

    def __init__(
            self,
            q: float, 
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
    

    def _force_from_others(self):
        force = np.zeros((2,))
        for obj in self.field.get_others(self):
            rad_vector = obj.pos - self.pos
            f = abs(self.q * obj.q) / np.linalg.norm(rad_vector) ** 2

            if self.q > 0 and obj.q > 0 or self.q < 0 and obj.q < 0:
                f *= -1
            if self.r + obj.r > np.linalg.norm(rad_vector):
                f *= -0.5
            force += rad_vector / np.linalg.norm(rad_vector) * f
        return force


    def _force_from_roy(self, q_k:float):
        roy_q = self.field.get_roy_q() * q_k
        roy_centre = self.field.get_roy_centre()
        
        rad_vector = roy_centre - self.pos
        f = abs(self.q * roy_q) / np.linalg.norm(rad_vector) ** 2

        return rad_vector / np.linalg.norm(rad_vector) * f

    def apply_force(self, dt):
        if self.m > 20:
            return
        
        F1 = self._force_from_others() # force from others
        F2 = self._force_from_roy(q_k=0.5) # force from roy
        F2 = np.zeros_like(F1)
        force = crop_vector(F1 + F2, 30)


        force *= 1 / self.k
        
        acceleration = force / self.m
        self.f = force # just for make possible to draw force line at any time
        self.v += acceleration * dt
        
        for obj in self.field.get_others(self):
            if np.linalg.norm((self.pos+self.v*dt)-obj.pos) < self.r + obj.r:
                self.v = np.zeros_like(self.v)
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

