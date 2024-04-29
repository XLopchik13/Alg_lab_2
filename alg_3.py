class Event:
    def __init__(self, x, begin_y, end_y, status):
        self.x = x
        self.begin_y = begin_y
        self.end_y = end_y
        self.status = status


class Node:
    def __init__(self, value, left, right, left_ind, right_ind):
        self.value = value
        self.left = left
        self.right = right
        self.left_ind = left_ind
        self.right_ind = right_ind


def build_tree(left_ind, right_ind):
    if left_ind >= right_ind:
        return Node(0, None, None, left_ind, right_ind)

    mid = (left_ind + right_ind) // 2
    left = build_tree(left_ind, mid)
    right = build_tree(mid + 1, right_ind)

    return Node(left.value + right.value, left, right, left_ind, right.right_ind)


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


def insert(node, begin, end, value):
    if begin <= node.left_ind and node.right_ind <= end:
        return Node(node.value + value, node.left, node.right, node.left_ind, node.right_ind)
    if node.right_ind < begin or end < node.left_ind:
        return node
    new_node = Node(node.value, node.left, node.right, node.left_ind, node.right_ind)
    new_node.left = insert(new_node.left, begin, end, value)
    new_node.right = insert(new_node.right, begin, end, value)
    return new_node


def build_persistent_segment_tree(rectangles, compress_x, compress_y):
    events = []
    if not rectangles:
        return None

    for r in rectangles:
        begin_y = find_pos(compress_y, r[1])
        end_y = find_pos(compress_y, r[3])

        events.append(Event(r[0], begin_y, end_y - 1, 1))
        events.append(Event(r[2], begin_y, end_y - 1, -1))
    events.sort(key=lambda event: event.x)

    roots = []
    root = build_tree(0, len(compress_y) - 1)

    end_x = events[0].x
    for event in events:
        if end_x != event.x:
            roots.append(root)
            end_x = event.x
        root = insert(root, event.begin_y, event.end_y, event.status)
    roots.append(root)
    return roots


def get_answer(node, target):
    if node:
        mid = (node.left_ind + node.right_ind) // 2
        if target <= mid:
            return node.value + get_answer(node.left, target)
        else:
            return node.value + get_answer(node.right, target)
    return 0


def tree_algorithm(points, compress_x, compress_y, roots):
    answer = []
    if roots is None:
        return answer

    for p in points:
        pos_x = find_pos(compress_x, p[0])
        pos_y = find_pos(compress_y, p[1])

        if pos_x == -1 or pos_y == -1:
            answer.append(0)
        else:
            answer.append(get_answer(roots[pos_x], pos_y))
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
# roots = build_persistent_segment_tree(rectangles, compress_x, compress_y)
# print(*tree_algorithm(points, compress_x, compress_y, roots))
