import random
import time
import math
import app_config
import threading

# Позиции спавна
spawn_positions = [
    (app_config.point_position_0_X, app_config.point_position_0_Y),  # 0
    (app_config.point_position_1_X, app_config.point_position_1_Y),  # 1
    (app_config.point_position_2_X, app_config.point_position_2_Y),  # 2
    (app_config.point_position_3_X, app_config.point_position_3_Y),  # 3
    (app_config.point_position_4_X, app_config.point_position_4_Y),  # 4
    (app_config.point_position_5_X, app_config.point_position_5_Y),  # 5
    (app_config.point_position_6_X, app_config.point_position_6_Y),  # 6
    (app_config.point_position_7_X, app_config.point_position_7_Y)   # 7
]

# Базовые повороты
base_rotations = [
    app_config.point_rotation_0, app_config.point_rotation_1,
    app_config.point_rotation_2, app_config.point_rotation_3,
    app_config.point_rotation_4, app_config.point_rotation_5,
    app_config.point_rotation_6, app_config.point_rotation_7
]

active_points = [] 

SPAWN_INTERVAL = app_config.tik_rate / 100  # Раз в тик

number_point = 0

point_speed_x = 0
point_speed_y = 0

def spawn_point():
    global number_point
    global active_points
    
    # Случайная позиция
    position = random.randint(0, 7)
               
    # Базовые значения
    base_x, base_y = spawn_positions[position]
    base_rotation = base_rotations[position]
    
    # Рандом
    position_x = base_x + random.randint(app_config.point_X_random_min, app_config.point_X_random_max)
    position_y = base_y + random.randint(app_config.point_Y_random_min, app_config.point_Y_random_max)
    point_rotation = base_rotation + random.randint(app_config.point_rotation_min, app_config.point_rotation_max)
    
    point_speed_x = random.randint(app_config.point_speed_random_min, app_config.point_speed_random_max)
    point_speed_y = random.randint(app_config.point_speed_random_min, app_config.point_speed_random_max)
    
    # Обновление
    number_point += 1
    active_points.append((position_x, position_y, point_rotation, point_speed_x, point_speed_y))
    
    # Вывод
    print(f"--- Спавн точки #{number_point} (тартовая позиция: {position}) ---")
    print(f"Позиция: X={position_x}, Y={position_y}")
    print(f"Поворот: {point_rotation}")
    print(f"Скорость: X={point_speed_x}, Y={point_speed_y}")
    print(f"Всего точек: {len(active_points)}")
    print(f"Массив точек: {active_points}")
    print()
    
def update_position(dt):
    
    global active_points
    
    
    

while True:
    if number_point >= app_config.limit_point:
        break
        
    start_time = time.time()#---------------------------Засекаем время начала
    
    spawn_point()#--------------------------------------Запуск
    
    execution_time = time.time() - start_time#----------Считаем, сколько она шла
    
    # Считаем, сколько осталось спать (чтобы в сумме было 5 секунд)
    sleep_time = max(0, SPAWN_INTERVAL - execution_time) 
    time.sleep(sleep_time)
