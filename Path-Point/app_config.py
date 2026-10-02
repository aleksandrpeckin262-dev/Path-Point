# Настройка спавна точек
point_speed_x = 0
point_speed_y = 0
tik_rate = 2

# Настройка позиций спавна точек (проценты от размеров монитора)
# ВАЖНО: В arcade Y=0 — это НИЗ экрана, Y=100 — это ВЕРХ!
point_position_0_X = 0    # Левый край, центр
point_position_0_Y = 50

point_position_1_X = 100  # Правый край, центр
point_position_1_Y = 50

point_position_2_X = 0    # Левый ВЕРХ (Y=100 — это верх!)
point_position_2_Y = 100

point_position_3_X = 100  # Правый ВЕРХ
point_position_3_Y = 100

point_position_4_X = 0    # Левый НИЗ (Y=0 — это низ!)
point_position_4_Y = 0

point_position_5_X = 100  # Правый НИЗ
point_position_5_Y = 0

point_position_6_X = 50   # Центр НИЗА
point_position_6_Y = 0

point_position_7_X = 50   # Центр ВЕРХА
point_position_7_Y = 100

# Изначальные повороты точек (ПРАВИЛЬНЫЕ УГЛЫ для arcade)
# Угол 0° = вправо, 90° = вверх, 180° = влево, -90° = вниз
point_rotation_0 = 0      # Левый центр → ВПРАВО
point_rotation_1 = 180    # Правый центр → ВЛЕВО
point_rotation_2 = -45    # Левый ВЕРХ → ВПРАВО-ВНИЗ
point_rotation_3 = -135   # Правый ВЕРХ → ВЛЕВО-ВНИЗ
point_rotation_4 = 45     # Левый НИЗ → ВПРАВО-ВВЕРХ
point_rotation_5 = 135    # Правый НИЗ → ВЛЕВО-ВВЕРХ
point_rotation_6 = 90     # Центр НИЗА → ВВЕРХ
point_rotation_7 = -90    # Центр ВЕРХА → ВНИЗ

# Погрешность поворота (сектор разлёта)
point_rotation_0_max = 90   # База 0: от -90° до 90° (вправо)
point_rotation_0_min = -90

point_rotation_1_max = 90   # База 1: от 90° до 270° (влево)
point_rotation_1_min = -90

point_rotation_2_max = 45   # База 2: от -90° до 0° (вправо-вниз)
point_rotation_2_min = -45

point_rotation_3_max = 45   # База 3: от -180° до -90° (влево-вниз)
point_rotation_3_min = -45

point_rotation_4_max = 45   # База 4: от 0° до 90° (вправо-вверх)
point_rotation_4_min = -45

point_rotation_5_max = 45   # База 5: от 90° до 180° (влево-вверх)
point_rotation_5_min = -45

point_rotation_6_max = 90   # База 6: от 0° до 180° (вверх)
point_rotation_6_min = -90

point_rotation_7_max = 90   # База 7: от -180° до 0° (вниз)
point_rotation_7_min = -90  # ИСПРАВЛЕНО: было 0

# Настройка погрешности рандома позиций
point_X_random_max_0 = 0
point_X_random_min_0 = 0
point_Y_random_max_0 = 50
point_Y_random_min_0 = -50

point_X_random_max_1 = 0
point_X_random_min_1 = 0
point_Y_random_max_1 = 50
point_Y_random_min_1 = -50

point_X_random_max_2 = 50
point_X_random_min_2 = 0
point_Y_random_max_2 = 0
point_Y_random_min_2 = 0

point_X_random_max_3 = 0
point_X_random_min_3 = -50
point_Y_random_max_3 = 0
point_Y_random_min_3 = 0

point_X_random_max_4 = 50
point_X_random_min_4 = 0
point_Y_random_max_4 = 0
point_Y_random_min_4 = 0

point_X_random_max_5 = 0
point_X_random_min_5 = -50
point_Y_random_max_5 = 0
point_Y_random_min_5 = 0

point_X_random_max_6 = 20   # ИСПРАВЛЕНО: было 180
point_X_random_min_6 = 0
point_Y_random_max_6 = 0
point_Y_random_min_6 = 0

point_X_random_max_7 = 20
point_X_random_min_7 = -20
point_Y_random_max_7 = 0
point_Y_random_min_7 = 0

# Настройка рандома скоростей точек
point_speed_random_max = 8
point_speed_random_min = -8

# Настройка GUI
NAME_WINDOW = "Path-Point"

# Коэффициенты размеров UI
point_size = 150
point_gravity = 5
limit_point = 200
line_width = 256
point_collision = 15