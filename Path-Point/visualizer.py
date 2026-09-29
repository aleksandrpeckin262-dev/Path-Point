import arcade
from logic import active_points, collision_pairs, points_lock, screen_width, screen_height
import app_config

class ConstellationWindow(arcade.Window):
    def __init__(self):
        super().__init__(screen_width, screen_height, app_config.NAME_WINDOW)
        self.point_radius = (screen_width + screen_height) / app_config.point_size
        
    def on_draw(self):
        self.clear(color=arcade.color.BLACK)
        
        with points_lock:
            # Рисуем линии
            for point1, point2 in collision_pairs:
                x1, y1 = point1[0], point1[1]
                x2, y2 = point2[0], point2[1]
                arcade.draw_line(x1, y1, x2, y2, arcade.color.WHITE, 2)
            
            # Рисуем точки
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