import random
import time

matrix_size_x = 128
matrix_size_y = matrix_size_x // 2

point_ID = 0
point_anti_gravity = 10
points_list = []

planet_ID = 0
planet_total_mass = 13
planet_list = []

planet_limit = 5

# Для движения планет


# Функция создания точки
def create_point(matrix_size_x, matrix_size_y, point_anti_gravity):
    global point_ID
    
    point = {
        "point_x_ID": random.randint(0, matrix_size_x),
        "point_y_ID": random.randint(0, matrix_size_y),
        "point_ID": point_ID,
        "point_anti_gravity": point_anti_gravity,
    }
    point_ID += 1
    return point

# Функция создания планеты
def create_planet(planet_total_mass):
    global planet_ID
    
    planet = {
        "planet_mass": random.randint(1, planet_total_mass),
        "planet_x_ID": random.randint(0, matrix_size_x),
        "planet_y_ID": random.randint(0, matrix_size_y),
        "planet_ID": planet_ID
    }
    planet_ID += 1
    return planet

def update_matrix(planet, point):
    planet_X = planet_x_ID
    planet_Y = planet_y_ID
    
    
    

# цикл спавна точек
for i in range(matrix_size_x * matrix_size_y):
    new_point = create_point(matrix_size_x, matrix_size_y, point_anti_gravity)
    points_list.append(new_point)
    
print(f"Всего точек: {len(points_list)}")
print(f"Первая точка: {points_list[0]}")
print(f"Последняя точка: {points_list[-1]}")

# цикл спавна планет
for i in range(planet_limit):
    new_planet = create_planet(planet_total_mass)
    planet_list.append(new_planet)

print(f"Всего планет: {len(planet_list)}")
print(f"Первая планета: {planet_list[0]}")
print(f"Последняя планета: {planet_list[-1]}")
