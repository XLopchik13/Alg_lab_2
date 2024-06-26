# Лабораторная работа №2

### Задача
Даны прямоугольники на плоскости с углами в целочисленных координатах ([1..109],[1..109]).
Требуется как можно быстрее выдавать ответ на вопрос: «Скольким прямоугольникам принадлежит точка (x,y)?». При этом подготовка данных должна занимать мало времени.


### Цели лабораторной работы
- Реализовать три разных решения задачи

- Выяснить при каком объеме начальных данных и точек какой алгоритм эффективнее.

---
## Реализация алгоритмов:
### Алгоритм перебора


```Python
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
   ```

**Сложность:**

Не подразумевает подготовку данных.
Подготовка O(1), поиск O(N * M), где N - количество прямоугольников, M - количество точек.

---
### Алгоритм на карте

Требуется подготовка данных, которая происходит с помощью сжатия координат
всех угловых точек прямоугольников по осям x, y и создание карты с последующим
заполнением. Карта - это матрица i на j, где i - количество сжатых точек по оси 
х, j - количество сжатых точек по оси у, а её заполнение - это обход всех
прямоугольников и увеличение проекции каждого прямоугольника на сжатых координатах
на один в данной матрице.

Сам алгоритм - это запрос к матрице, где i - сжатая координата по x, а 
j - сжатая координата по y (сжатые координаты находятся с помощью бин.поиска).

```Python
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
```

**Сложность:**

Подготовка O(N^3), поиск O(M * logN), где M - количество точек, N - количество прямоугольников.

---

### Алгоритм на дереве

Требуется подготовка данных, которая подразумевает сжатие координат и построение 
персистентного дерева отрезков на сжатых координатах (при помощи дополнительной структуры
Event, подразумевающей начало или конец существования прямоугольника). Следующий шаг -
построение пустого дерева отрезков и добавление персистентных узлов.

Поиск с помощью этого алгоритма - это нахождение нужного корня дерева по 
сжатым координатам точки и осуществление обхода по дереву до нужного листа.


```Python
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
```

**Сложность:**

Подготовка O(N * logN), поиск  O(M * logN), где M - количество точек, N - количество прямоугольников

---

## Тестирование

### Генерация прямоугольников:

Вложенные друг в друга прямоугольники создаются по формуле:
`(10*i, 10*i), (10*(2*n-i), 10*(2*n-i))`

```Python
def data_generate(n):
    arr = []
    for i in range(n):
        x1, y1, x2, y2 = 10 * i, 10 * i, 10 * (2 * n - i), 10 * (2 * n - i)
        arr.append([x1, y1, x2, y2])
    return arr
 ```

### Генерация точек:

Набор координат точек, распределенных равномерно по ненулевому
пересечению прямоугольников - хэш функции от i с разным базисом для x и y:
`(i*p)^31%(20*n)`. Где p - случайное большое простое число (разное для x и y).

```Python
def points_generate(n):
    arr = []
    for i in range(n):
        x = (i * PRIME_X) ** 31 % (20 * n)
        y = (i * PRIME_Y) ** 31 % (20 * n)
        arr.append([x, y])
    return arr
```

### Данные для тестирования:

- Кол-во точек для каждого i = 40000

- Количество прямоугольников равно `2^i`, где `0<=i<=11`


### Измерение времени подготовки:

![](/graphics/prep.png)


Видно, что с ростом числа прямоугольников время обработки
алгоритма на карте начинает резко увеличиваться. Это связано
с большой асимптотикой построения карты - O(N^3).
В худшем случае требуется выполнить N итераций по всей матрице 
размером N * N.

Построение персистентного дерева на небольшом числе 
данных занимает примерно то же время, что и построение карты, однако 
рост времени работы алгоритма с увеличением количества данных намного медленнее. 
Это позволяет алгоритму на дереве эффективно производить предобработку 
даже при большом числе прямоугольников, в отличие от алгоритма на карте.


### Измерение времени поиска ответа:

![](/graphics/res.png)

На небольших данных алгоритм перебора показывает себя чуть
лучше остальных алгоритмов, но это лишь на уровне слишком незначительных
значений.

Однако при увеличении числа прямоугольников время 
выполнения алгоритма полного перебора резко возрастает, в то 
время как алгоритмы с подготовкой данных остаются более стабильными. 
Алгоритм на карте показывает более высокую эффективность в сравнении с 
алгоритмом на дереве, несмотря на равную асимптотику. Это 
связано с тем, что алгоритм на дереве требует двойной бинарный 
поиск для нахождения индексов x и y координат точки в массивах 
сжатых координат, а затем производит спуск по дереву - это приводит к
большей константе перед логарифмом по сравнению с алгоритмом на карте.


### Измерение общего времени:

![](/graphics/total.png)

Исходя из графика с итоговым временем, можно сделать вывод, 
что алгоритм на карте значительно отстает по времени выполнения 
от двух других. Несмотря на относительно быстрый поиск 
ответа, он проигрывает алгоритму полного перебора 
при обработке примерно сотни прямоугольников. 
Что касается алгоритма на дереве, он демонстрирует лучшую стабильность
и производительность (на больших данных).

---

## Вывод
Алгоритм перебора лучше показал себя на небольших данных, которые 
не требуют дополнительных затрат на подготовку данных.
Алгоритм на карте показал себя неплохо лишь на небольшом кол-ве прямоугольников и
любом кол-ве точек, однако реализовать его несколько проще, чем последний 
алгоритм. Алгоритм на персистентном дереве отрезков лучше всего раскрывается
во время работы с большими данными.
