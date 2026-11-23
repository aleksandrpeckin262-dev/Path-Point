# Значения загружаются из config.json

import json
import os
import sys

# Находим папку, в которой лежит сам файл запуска .exe на столе
if getattr(sys, 'frozen', False):
    _base_dir = os.path.dirname(sys.executable)
else:
    _base_dir = os.path.dirname(os.path.abspath(__file__))

# Загрузка конфигурации строго из внешней папки
_config_path = os.path.join(_base_dir, "config.json")
with open(_config_path, "r", encoding="utf-8") as _f:
    _cfg = json.load(_f)

# Вспомогательная функция для безопасного получения значений
def _get(key, default=None):
    return _cfg.get(key, default)

# Настройка спавна точек
point_speed_x = _get("point_speed_x", 0)
point_speed_y = _get("point_speed_y", 0)
tik_rate = _get("tik_rate", 0.001)
spawn_interval = _get("spawn_interval", 0.01)
video_FPS = _get("video_FPS", 30)
max_frames = _get("max_frames", 150)
screenshot_start_sleep = _get("scrinshot_start_sleep", 20) # Кадры

# Настройка позиций спавна точек
point_position_0_X = _get("point_position_0_X", 0)
point_position_0_Y = _get("point_position_0_Y", 50)

point_position_1_X = _get("point_position_1_X", 100)
point_position_1_Y = _get("point_position_1_Y", 50)

point_position_2_X = _get("point_position_2_X", 0)
point_position_2_Y = _get("point_position_2_Y", 100)

point_position_3_X = _get("point_position_3_X", 100)
point_position_3_Y = _get("point_position_3_Y", 100)

point_position_4_X = _get("point_position_4_X", 0)
point_position_4_Y = _get("point_position_4_Y", 0)

point_position_5_X = _get("point_position_5_X", 100)
point_position_5_Y = _get("point_position_5_Y", 0)

point_position_6_X = _get("point_position_6_X", 50)
point_position_6_Y = _get("point_position_6_Y", 0)

point_position_7_X = _get("point_position_7_X", 50)
point_position_7_Y = _get("point_position_7_Y", 100)

# Изначальные повороты точек
point_rotation_0 = _get("point_rotation_0", 0)
point_rotation_1 = _get("point_rotation_1", 180)
point_rotation_2 = _get("point_rotation_2", -45)
point_rotation_3 = _get("point_rotation_3", -135)
point_rotation_4 = _get("point_rotation_4", 45)
point_rotation_5 = _get("point_rotation_5", 135)
point_rotation_6 = _get("point_rotation_6", 90)
point_rotation_7 = _get("point_rotation_7", -90)

# Погрешность поворота (сектор разлёта)
point_rotation_0_max = _get("point_rotation_0_max", 90)
point_rotation_0_min = _get("point_rotation_0_min", -90)

point_rotation_1_max = _get("point_rotation_1_max", 90)
point_rotation_1_min = _get("point_rotation_1_min", -90)

point_rotation_2_max = _get("point_rotation_2_max", 45)
point_rotation_2_min = _get("point_rotation_2_min", -45)

point_rotation_3_max = _get("point_rotation_3_max", 45)
point_rotation_3_min = _get("point_rotation_3_min", -45)

point_rotation_4_max = _get("point_rotation_4_max", 45)
point_rotation_4_min = _get("point_rotation_4_min", -45)

point_rotation_5_max = _get("point_rotation_5_max", 45)
point_rotation_5_min = _get("point_rotation_5_min", -45)

point_rotation_6_max = _get("point_rotation_6_max", 90)
point_rotation_6_min = _get("point_rotation_6_min", -90)

point_rotation_7_max = _get("point_rotation_7_max", 90)
point_rotation_7_min = _get("point_rotation_7_min", -90)

# Настройка погрешности рандома позиций
point_X_random_max_0 = _get("point_X_random_max_0", 0)
point_X_random_min_0 = _get("point_X_random_min_0", 0)
point_Y_random_max_0 = _get("point_Y_random_max_0", 50)
point_Y_random_min_0 = _get("point_Y_random_min_0", -50)

point_X_random_max_1 = _get("point_X_random_max_1", 0)
point_X_random_min_1 = _get("point_X_random_min_1", 0)
point_Y_random_max_1 = _get("point_Y_random_max_1", 50)
point_Y_random_min_1 = _get("point_Y_random_min_1", -50)

point_X_random_max_2 = _get("point_X_random_max_2", 50)
point_X_random_min_2 = _get("point_X_random_min_2", 0)
point_Y_random_max_2 = _get("point_Y_random_max_2", 0)
point_Y_random_min_2 = _get("point_Y_random_min_2", 0)

point_X_random_max_3 = _get("point_X_random_max_3", 0)
point_X_random_min_3 = _get("point_X_random_min_3", -50)
point_Y_random_max_3 = _get("point_Y_random_max_3", 0)
point_Y_random_min_3 = _get("point_Y_random_min_3", 0)

point_X_random_max_4 = _get("point_X_random_max_4", 50)
point_X_random_min_4 = _get("point_X_random_min_4", 0)
point_Y_random_max_4 = _get("point_Y_random_max_4", 0)
point_Y_random_min_4 = _get("point_Y_random_min_4", 0)

point_X_random_max_5 = _get("point_X_random_max_5", 0)
point_X_random_min_5 = _get("point_X_random_min_5", -50)
point_Y_random_max_5 = _get("point_Y_random_max_5", 0)
point_Y_random_min_5 = _get("point_Y_random_min_5", 0)

point_X_random_max_6 = _get("point_X_random_max_6", 20)
point_X_random_min_6 = _get("point_X_random_min_6", 0)
point_Y_random_max_6 = _get("point_Y_random_max_6", 0)
point_Y_random_min_6 = _get("point_Y_random_min_6", 0)

point_X_random_max_7 = _get("point_X_random_max_7", 20)
point_X_random_min_7 = _get("point_X_random_min_7", -20)
point_Y_random_max_7 = _get("point_Y_random_max_7", 0)
point_Y_random_min_7 = _get("point_Y_random_min_7", 0)

# Настройка рандома скоростей точек
point_speed_random_max = _get("point_speed_random_max", 50)
point_speed_random_min = _get("point_speed_random_min", -50)

# Настройка GUI
NAME_WINDOW = _get("NAME_WINDOW", "Path-Point")

# Коэффициенты размеров UI
point_size = _get("point_size", 1000)
point_gravity = _get("point_gravity", 5)
limit_point = _get("limit_point", 200)
line_width = _get("line_width", 256)
point_collision = _get("point_collision", 15)

# Полупрозрачные линии от 1 до 255
line_alpha_near = _get("line_alpha_near", 255)
line_alpha_far = _get("line_alpha_far", 1)

# Очистка временных переменных
del _base_dir, _config_path, _f, _cfg, _get
