import arcade
import random
import time
import app_config

screen_width, screen_height = arcade.get_display_size()

screen_size = screen_width + screen_height # Размер монитора

print(screen_size)

# Класс окна
class ConstellationWindow(arcade.Window):
    def __init__(self):
        # Инициализируем окно размерами и именем из твоего конфига
        super().__init__(screen_width, screen_height, app_config.NAME_WINDOW)
        
    # Отрисовка
    def on_draw(self):
        # Очистка экрана каждый кадр
        self.clear()
        

# Инициализация
def main():
    window = ConstellationWindow()
    
    # Тик рейт
    window.set_update_rate(1 / app_config.tik_rate)
    
    # Запуск цикла
    arcade.run()

if __name__ == "__main__":
    main()
