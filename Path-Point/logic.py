import random
import time
import math
import app_config
import threading
import arcade

screen_width, screen_height = arcade.get_display_size()

screen_size = screen_width + screen_height

spawn_positions = [
    (app_config.point_position_0_X, app_config.point_position_0_Y),
    (app_config.point_position_1_X, app_config.point_position_1_Y),
    (app_config.point_position_2_X, app_config.point_position_2_Y),
    (app_config.point_position_3_X, app_config.point_position_3_Y),
    (app_config.point_position_4_X, app_config.point_position_4_Y),
    (app_config.point_position_5_X, app_config.point_position_5_Y),
    (app_config.point_position_6_X, app_config.point_position_6_Y),
    (app_config.point_position_7_X, app_config.point_position_7_Y)
]

base_rotations = [
    app_config.point_rotation_0, app_config.point_rotation_1,
    app_config.point_rotation_2, app_config.point_rotation_3,
    app_config.point_rotation_4, app_config.point_rotation_5,
    app_config.point_rotation_6, app_config.point_rotation_7
]

active_points = [] 
SPAWN_INTERVAL = app_config.tik_rate / 1000
UPDATE_INTERVAL = app_config.tik_rate / 100

points_lock = threading.Lock()

def spawn_point():
    position = random.randint(0, 7)
    base_x, base_y = spawn_positions[position]
    base_rotation = base_rotations[position]
    
    position_x = base_x + random.randint(app_config.point_X_random_min, app_config.point_X_random_max)
    position_y = base_y + random.randint(app_config.point_Y_random_min, app_config.point_Y_random_max)
    point_rotation = base_rotation + random.randint(app_config.point_rotation_min, app_config.point_rotation_max)
    
    point_speed_x = random.randint(app_config.point_speed_random_min, app_config.point_speed_random_max)
    point_speed_y = random.randint(app_config.point_speed_random_min, app_config.point_speed_random_max)
    
    with points_lock:
        active_points.append((position_x, position_y, point_rotation, point_speed_x, point_speed_y))
    
    print(f"--- Спавн точки (тартовая позиция: {position}) ---")
    print(f"Позиция: X={position_x}, Y={position_y}")
    print(f"Поворот: {point_rotation}")
    print(f"Скорость: X={point_speed_x}, Y={point_speed_y}")
    print(f"Всего точек: {len(active_points)}")
    print()
    
def update_position():
    with points_lock:
        for i in range(len(active_points)):
            x, y, rotation, speed_x, speed_y = active_points[i]
            new_x = x + speed_x
            new_y = y + speed_y
            active_points[i] = (new_x, new_y, rotation, speed_x, speed_y)
        
def delete_point():
    with points_lock:
        i = 0
        while i < len(active_points):
            x, y, rotation, speed_x, speed_y = active_points[i]
            
            if x > screen_width or y > screen_height or x < 0 or y < 0:
                active_points.pop(i)
                print(f"УДАЛЕНА точка: X={x}, Y={y}")
            else:
                i += 1
    
def spawn_loop():    
    while True:
        with points_lock:
            current_count = len(active_points)
        
        # Спавним, пока точек меньше лимита
        if current_count < app_config.limit_point:
            start_time = time.time()
            spawn_point()
            execution_time = time.time() - start_time
            sleep_time = max(0, SPAWN_INTERVAL - execution_time) 
            time.sleep(sleep_time)
        else:
            # Ждём, пока точки удалятся
            time.sleep(0.1)

def move_loop(): 
    while True:
        start_time = time.time()
        update_position()
        sleep_time = max(0, UPDATE_INTERVAL - (time.time() - start_time))
        time.sleep(sleep_time)

def delete_loop():  
    while True:
        start_time = time.time()
        delete_point()
        sleep_time = max(0, UPDATE_INTERVAL - (time.time() - start_time))
        time.sleep(sleep_time)
        
t1 = threading.Thread(target=spawn_loop, daemon=True)
t2 = threading.Thread(target=move_loop, daemon=True)
t3 = threading.Thread(target=delete_loop, daemon=True)

t1.start()
t2.start()
t3.start()