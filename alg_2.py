def find_pos(arr, value):
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == value:
            return mid
        elif arr[mid] > value:
            right = mid - 1
        else:
            left = mid + 1
    return left - 1


def compress_coordinates(rectangles):
    set_compress_x = set()
    set_compress_y = set()

    for r in rectangles:
        set_compress_x.add(r[0])
        set_compress_y.add(r[1])
        set_compress_x.add(r[2])
        set_compress_y.add(r[3])

    compress_x = sorted(set_compress_x)
    compress_y = sorted(set_compress_y)
    return compress_x, compress_y


def create_map(rectangles, compress_x, compress_y):
    matrix_map = [[0] * len(compress_x) for _ in range(len(compress_y))]

    for r in rectangles:
        first_ind_x = find_pos(compress_x, r[0])
        first_ind_y = find_pos(compress_y, r[1])
        second_ind_x = find_pos(compress_x, r[2])
        second_ind_y = find_pos(compress_y, r[3])

        for i in range(first_ind_y, second_ind_y):
            for j in range(first_ind_x, second_ind_x):
                matrix_map[i][j] += 1
    return matrix_map


def map_algorithm(matrix_map, points, compress_x, compress_y):
    answer = []
    for p in points:
        pos_x = find_pos(compress_x, p[0])
        pos_y = find_pos(compress_y, p[1])
        if pos_x == -1 or pos_y == -1:
            answer.append(0)
        else:
            answer.append(matrix_map[pos_y][pos_x])
    return answer


# n = int(input())
# rectangles = []
# for _ in range(n):
#     rect = list(map(int, input().split()))
#     rectangles.append(rect)
#
# m = int(input())
# points = []
# for _ in range(m):
#     point = list(map(int, input().split()))
#     points.append(point)
#
# compress_x, compress_y = compress_coordinates(rectangles)
# matrix_map = create_map(rectangles, compress_x, compress_y)
# print(*map_algorithm(matrix_map, points, compress_x, compress_y))
