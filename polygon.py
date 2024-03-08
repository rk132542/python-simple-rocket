import pygame

class Polygon:
    def __init__(self, verticies, color):
        self.verticies = verticies
        self.color = color
        self.points = []
        for verticie in verticies:
            # verticie -> ((x1, y1), (x2, y2))
            self.points.append(verticie[0])
        

    def draw(self, surface):
        pygame.draw.polygon(surface, self.color, self.points)
        
    def point_inside(self, point):
        # Check if the point is inside the polygon
        for verticie in self.verticies: 
            # verticie -> ((x1, y1), (x2, y2))
            x1, y1 = verticie[0]
            x2, y2 = verticie[1]
            # if x1 is smaller than x2, then x1 is the leftmost point
            if x1 > x2:
                x1, x2 = x2, x1
            # if y1 is smaller than y2, then y1 is the topmost point
            if y1 > y2:
                y1, y2 = y2, y1
            if x1 <= point[0] <= x2 and y1 <= point[1] <= y2:
                return True
        return False
    
    def collides_with(self, other_polygon):
        # Check if any of the points of the other polygon are inside this polygon
        for point in other_polygon.points:
            if self.point_inside(point):
                return True
        return False
        