import arcade
import random
import time
import app_config

# Позиции спавна
spawn_positions = [
    (app_config.point_position_1_X, app_config.point_position_1_Y),  # 1
    (app_config.point_position_2_X, app_config.point_position_2_Y),  # 2
    (app_config.point_position_3_X, app_config.point_position_3_Y),  # 3
    (app_config.point_position_4_X, app_config.point_position_4_Y),  # 4
    (app_config.point_position_5_X, app_config.point_position_5_Y),  # 5
    (app_config.point_position_6_X, app_config.point_position_6_Y),  # 6
    (app_config.point_position_7_X, app_config.point_position_7_Y),  # 7
    (app_config.point_position_8_X, app_config.point_position_8_Y)   # 8
]

# Класс окна
class ConstellationWindow(arcade.Window):
    def __init__(self):
        # Инициализируем окно размерами и именем из твоего конфига
        super().__init__(app_config.WINDOW_SIZE_X, app_config.WINDOW_SIZE_Y, app_config.NAME_WINDOW)
        
        # Список точек
        self.active_points = [] 

    #  Основная логика
    def update(self, delta_time):

        pass

    # Отрисовка
    def on_draw(self):
        # Очистка экрана каждый кадр
        self.clear()
        
        pass

# Инициализация
def main():
    window = ConstellationWindow()
    
    # Тик рейт
    window.set_update_rate(1 / app_config.tik_rate)
    
    # Запуск цикла
    arcade.run()

if __name__ == "__main__":
    main()
