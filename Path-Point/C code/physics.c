#include <math.h>
#include <stdint.h> // Подключаем строгие типы данных

typedef struct {
    double x;
    double y;
    double rotation;
    double speed_x;
    double speed_y;
} Point;

// Используем гарантированно 32-битные числа, чтобы память не сдвигалась
typedef struct {
    int32_t index1;
    int32_t index2;
} CollisionPair;

__declspec(dllexport) void update_position_c(Point* points, int32_t count, double dt) {
    for (int32_t i = 0; i < count; i++) {
        points[i].x += points[i].speed_x * dt;
        points[i].y += points[i].speed_y * dt;
    }
}

__declspec(dllexport) int32_t detect_collisions_c(Point* points, int32_t count, double radius_sq, CollisionPair* pairs, int32_t max_pairs) {
    int32_t pair_count = 0;
    
    for (int32_t i = 0; i < count; i++) {
        for (int32_t j = i + 1; j < count; j++) {
            double dx = points[j].x - points[i].x;
            double dy = points[j].y - points[i].y;
            double dist_sq = dx * dx + dy * dy;
            
            if (dist_sq <= radius_sq) {
                if (pair_count < max_pairs) {
                    pairs[pair_count].index1 = i;
                    pairs[pair_count].index2 = j;
                    pair_count++;
                } else {
                    return pair_count;
                }
            }
        }
    }
    return pair_count;
}

