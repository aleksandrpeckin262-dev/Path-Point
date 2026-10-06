import arcade
import math
from logic import active_points, collision_pairs, points_lock, screen_width, screen_height
import app_config

screen_size = screen_width + screen_height

class ConstellationWindow(arcade.Window):
    def __init__(self):
        super().__init__(
            screen_width, 
            screen_height, 
            app_config.NAME_WINDOW,
            antialiasing=True
        )
        self.point_radius = (screen_width + screen_height) / app_config.point_size
    
    def on_draw(self):
        self.clear(color=arcade.color.BLACK)
        
        with points_lock:
            max_distance = screen_size / app_config.point_collision
            
            # Рисуем линии с alpha
            for point1, point2 in collision_pairs:
                x1, y1 = point1[0], point1[1]
                x2, y2 = point2[0], point2[1]
                
                distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                
                # Отношение текущего расстояния к максимальному
                ratio = distance / max_distance
                
                # Линейная интерполяция прозрачности
                alpha = int(app_config.line_alpha_near - (app_config.line_alpha_near - app_config.line_alpha_far) * ratio)
                
                # Границы от 0 до 255
                alpha = max(0, min(255, alpha))
                
                color = (255, 255, 255, alpha)
                arcade.draw_line(x1, y1, x2, y2, color, 2)
            
            # Отрисовка точек
            for point in active_points:
                x, y, rotation, speed_x, speed_y = point
                arcade.draw_circle_filled(x, y, self.point_radius, arcade.color.WHITE)
    
    def on_update(self, delta_time):
        pass

def main():
    window = ConstellationWindow()
    arcade.run()

if __name__ == "__main__":
    main()