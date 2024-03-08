import pygame

class Polygon:
    def __init(self, verticies, color):
        self.verticies = verticies
        self.color = color
        self.points = [] # convert verticies to points

    def draw(self, surface):
        pygame.draw.polygon(surface, self.color, self.points)
        
    def point_inside(self, point):
        # Check if the point is inside the polygon
        
        pass
    
    def collides_with(self, other_polygon):
        # Check if any of the points of the other polygon are inside this polygon
        for point in other_polygon.points:
            if self.point_inside(point):
                return True
        return False
        