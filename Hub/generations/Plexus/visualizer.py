import arcade
import math
import os
import logic
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
        self.save_path = os.path.join(".", "video", logic.new_folder_name)

    def on_draw(self):
        self.clear(color=arcade.color.BLACK)
        with points_lock:
            max_distance = screen_size / app_config.point_collision
            # Рисуем линии с alpha
            for point1, point2 in collision_pairs:
                x1, y1 = point1[0], point1[1]
                x2, y2 = point2[0], point2[1]
                distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                ratio = distance / max_distance
                alpha = int(app_config.line_alpha_near - (app_config.line_alpha_near - app_config.line_alpha_far) * ratio)
                alpha = max(0, min(255, alpha))
                color = (255, 255, 255, alpha)
                arcade.draw_line(x1, y1, x2, y2, color, 2)
            # Отрисовка точек
            for point in active_points:
                x, y, rotation, speed_x, speed_y = point
                arcade.draw_circle_filled(x, y, self.point_radius, arcade.color.WHITE)

        # --- СОХРАНЕНИЕ КАДРА ЧЕРЕЗ ARCADE ---
        # Обращаемся к переменным через logic
        if (logic.video_flag == 1
                and logic.SCREENSHOT_START_SLEEP >= logic.SCREENSHOT_START_SLEEP_MAX
                and logic.frame_number < app_config.max_frames):
            image = arcade.get_image()
            screenshot_name = f"frame_{logic.frame_number:05d}.png"
            screenshot_path = os.path.join(self.save_path, screenshot_name)
            image.save(screenshot_path)
            print(f"Кадр {logic.frame_number} сохранён (arcade.get_image)")
            logic.frame_number += 1
        # -----------------------------------------------------------

    def on_update(self, delta_time):
        pass

def main():
    window = ConstellationWindow()
    arcade.run()

if __name__ == "__main__":
    main()