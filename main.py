from time import perf_counter_ns
import alg_1, alg_2, alg_3


PRIME_X = 54713
PRIME_Y = 73637
TRIAL = 7


def data_generate(n):
    arr = []
    for i in range(n):
        x1, y1, x2, y2 = 10 * i, 10 * i, 10 * (2 * n - i), 10 * (2 * n - i)
        arr.append([x1, y1, x2, y2])
    return arr


def points_generate(n):
    arr = []
    for i in range(n):
        x = (i * PRIME_X) ** 31 % (20 * n)
        y = (i * PRIME_Y) ** 31 % (20 * n)
        arr.append([x, y])
    return arr


def tests():
    f = open('tests.txt', 'w')

    n_points = 40000
    points_arr = points_generate(n_points)
    for i in range(11):
        n_rectangles = 2 ** i
        rectangles_arr = data_generate(n_rectangles)

        prep_1, prep_2, prep_3 = 0, 0, 0
        res_1, res_2, res_3 = 0, 0, 0
        total_1, total_2, total_3 = 0, 0, 0
        start, finish = 0, 0
        for _ in range(TRIAL):
            start = perf_counter_ns()
            alg_1.brute_force(rectangles_arr, points_arr)
            finish = perf_counter_ns()
            res_1 += finish - start

            start = perf_counter_ns()
            compress_x, compress_y = alg_2.compress_coordinates(rectangles_arr)
            matrix_map = alg_2.create_map(rectangles_arr, compress_x, compress_y)
            finish = perf_counter_ns()
            prep_2 += finish - start
            start = perf_counter_ns()
            alg_2.map_algorithm(matrix_map, points_arr, compress_x, compress_y)
            finish = perf_counter_ns()
            res_2 += finish - start

            start = perf_counter_ns()
            compress_x, compress_y = alg_3.compress_coordinates(rectangles_arr)
            roots = alg_3.build_persistent_segment_tree(rectangles_arr, compress_x, compress_y)
            finish = perf_counter_ns()
            prep_3 += finish - start
            start = perf_counter_ns()
            alg_3.tree_algorithm(points_arr, compress_x, compress_y, roots)
            finish = perf_counter_ns()
            res_3 += finish - start

        total_1 = (res_1 + prep_1) // TRIAL
        total_2 = (res_2 + prep_2) // TRIAL
        total_3 = (res_3 + prep_3) // TRIAL
        res_1 //= TRIAL
        res_2 //= TRIAL
        res_3 //= TRIAL
        prep_1 //= TRIAL
        prep_2 //= TRIAL
        prep_3 //= TRIAL

        f.write(f'{prep_1}\t{prep_2}\t{prep_3}\t{res_1}\t{res_2}\t{res_3}\t{total_1}\t{total_2}\t{total_3}\n')
    f.close()


tests()
