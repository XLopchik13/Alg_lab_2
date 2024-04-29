def brute_force(rectangles, points):
    counts = []
    for point in points:
        x, y = point
        count = 0
        for rect in rectangles:
            x1, y1, x2, y2 = rect
            if x1 <= x < x2 and y1 <= y < y2:
                count += 1
        counts.append(count)
    return counts


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
# print(*brute_force(rectangles, points))
