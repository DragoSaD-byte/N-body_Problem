"""! Модуль математического моделирования задачи
"""
from math import sqrt, pi
from tkinter import TclError


class MSolid:
    """! Класс описывет круглое тело с равномерным распределением массы для гравитационного взаимодействия.
    """
    def __init__(self, root, c_x, c_y, v_x, v_y, mass, color_self="white", color_track="green",
                 f_x=0, f_y=0, density=1):
        """! Метод инициализации.
        @param root: Холст на котором будет находиться тело.
        @param c_x: Координата тела по х.
        @param c_y: Координата тела по у.
        @param v_x: Проекция вектора скорости тела на ось х.
        @param v_y: Проекция вектора скорости тела на ось y.
        @param mass: Масса тела.
        @param color_self: Опциональный. Цвет самого тела (по умолчанию белый).
        @param color_track: Опциональный. Цвет трека тела (по умолчанию зелёный).
        @param f_x: Опциональный. Проекция вектора равнодействующей силы тела на ось х (по умолчанию 0).
        @param f_y: Опциональный. Проекция вектора равнодействующей силы тела на ось х (по умолчанию 0).
        @param density: Опциональный. Плотность тела (по умолчанию 1).
        @return: Экземпляр класса с указанными параметрами.
        """
        ## Масса тела.
        self.mass = mass
        ## Координата тела
        self.coordinate = [c_x, c_y]
        ## Вектор скорости тела
        self.velocity = [v_x, v_y]
        ## Равнодействующая сила
        self.force = [f_x, f_y]
        ## Плотность тела
        self.density = density
        ## Холст, на котором рисуеться тело
        self.root = root
        ## Радиус тела
        self.r = sqrt(abs(self.mass / self.density / pi))
        ## Равнодействующая сила на прошлом шаге
        self.f = [0, 0]
        ## Переменная для хранения индекса тела на холсте.
        self.solid = root.create_oval(
            int(self.coordinate[0] - self.r), int(self.coordinate[1] - self.r),
            int(self.coordinate[0] + self.r), int(self.coordinate[1] + self.r),
            fill=color_self)
        ## Список, содержащий индекс линии трека на холсте и трек тела.
        self.track = list([root.create_line(0, 0, 0, 0, fill=color_track)]) + list(self.coordinate)
        root.tag_lower(self.track[0])

    def apply_force(self, F):
        """! Метод обработки применения силы у телу.
        @param F: Вектор силы переданный в виде (Fx, Fy).
        """
        self.force[0] = self.force[0] + F[0]
        self.force[1] = self.force[1] + F[1]

    def move(self):
        """! Метод движения тела.
        Расситывает ускорение на основе силы, которая действует на тело, изменяет скорость, а потом обнуляет силу.
        В зависимости от скорости изменяет координату тела.
        """
        if self.mass == 0:
            return
        self.velocity[0] += self.force[0] / self.mass
        self.velocity[1] += self.force[1] / self.mass
        self.f = list(self.force)
        self.force = [0, 0]
        self.coordinate[0] += self.velocity[0]
        self.coordinate[1] += self.velocity[1]

    def update(self):
        """! Метод обновления отрисовки тела.
        На основе координат и радиуса перемещяает тело на холсте.
        Добавляет текущие координаты в трек.
        """
        self.track += list(self.coordinate)
        try:
            self.root.coords(self.solid,
                             int(self.coordinate[0] - self.r), int(self.coordinate[1] - self.r),
                             int(self.coordinate[0] + self.r), int(self.coordinate[1] + self.r))
        except TclError:
            pass

    def update_track(self, relatively=None):
        """! Метод обновления отрисовки трека тела.
        На основе координат в треке рисует тракеторию двидения относительно начала координат или иного тела.
        @param relatively: Опциональный. Относительно какого тела будет рисоваться траектоия (по умолчанию относительно никакого (центр координат).
        """
        try:
            if relatively is None:
                self.root.coords(*self.track)
            else:
                track = [self.track[0]]
                for i in range(1, len(self.track), 2):
                    track.append(int(self.track[i] - relatively.track[i] + relatively.track[-2]))
                    track.append(int(self.track[i + 1] - relatively.track[i + 1] + relatively.track[-1]))
                self.root.coords(*track)
        except TclError:
            pass

    def replace(self, x, y):
        """! Метод сдвига тела по координатам.
        @param x: Сдвиг по х.
        @param y: Сдвиг по у.
        """
        for i in range(1, len(self.track), 2):
            self.track[i] += x
            self.track[i + 1] += y
        self.coordinate[0] += x
        self.coordinate[1] += y

    def resize(self, delta, x, y):
        """! Метод мастабирования тела относительно какой-то точки.
        @param delta: Изменение мастаба.
        @param x: Х координата точки.
        @param y: У координата точки.
        """
        if delta > 0:
            delta += 1
        else:
            delta = 1 / (1-delta)
        for i in range(1, len(self.track), 2):
            self.track[i] = x + (self.track[i] - x) * delta
            self.track[i + 1] = y + (self.track[i + 1] - y) * delta
        self.coordinate[0] = x + (self.coordinate[0] - x) * delta
        self.coordinate[1] = y + (self.coordinate[1] - y) * delta
        self.mass *= delta

        self.density /= delta
        self.r = sqrt(abs(self.mass / self.density / pi))


class BodyVector:
    """! Класс отрисовывает рядом с телом на холсте root некий вектор vector (одномерный массив длинной 2), который принадлежит телу body.
    """
    def __init__(self, root, body: MSolid, vector: str, color="red"):
        """! Инициализация
        @param root: Холст, на который будет рисоваться вектор.
        @param body: Тело, для которого будет рисоваться вектор
        @param vector: Строка с названием вектора, который нужно отрисовать.
        @return: Экземпляр класса.
        @throw TypeError: Возникает, если атрибута с передонным названием не является 2-мерным вектором.
        @throw AttributeError: Возникает, если не существует атрибута с передонным названием.
        """
        ## Холст, на который рисуется вектор.
        self.root = root
        ## Тело, вектор которого рисуется.
        self.body = body
        ## Названия атрибута тела, который содержит вектор.
        self.vector = vector
        try:
            if len(eval("self.body." + self.vector)) != 2:
                raise TypeError("При создании BodyVector передан не вектор")
            float(eval("self.body." + self.vector)[0])
            float(eval("self.body." + self.vector)[1])
        except AttributeError:
            raise AttributeError("Попытка обратится к несуществующему вектору при создании BodyVector")
        except TypeError:
            raise TypeError("При создании BodyVector передан не вектор")
        x = self.body.coordinate[0]
        y = self.body.coordinate[1]
        ## Переменная для мастабирования вектора.
        self.scale = 10 ** (len(str(
            int(30 / sqrt(eval("self.body." + self.vector)[0] ** 2 + eval("self.body." + self.vector)[1] ** 2)))) - 1)
        ## Переменная для хранения индекса тега вектора на холсте.
        self.line = self.root.create_line(x, y, eval("self.body." + self.vector)[0] + x,
                                          eval("self.body." + self.vector)[1] + y, width=1, fill=color)

    def update(self):
        """! Метод обновления и переотрисовки
        """
        x = self.body.coordinate[0]
        y = self.body.coordinate[1]
        try:
            self.root.coords(self.line, x, y, eval("self.body." + self.vector)[0] * self.scale + x,
                             eval("self.body." + self.vector)[1] * self.scale + y)
        except TclError:
            pass

    def __del__(self):
        """! Деструктор
        """
        self.root.delete(self.line)


class CentrMass(MSolid):
    """! Класс для отображения центра масс.
    """
    def __init__(self, root):
        """! Инициализация.
        Масса, скоость и координата устанавливаються на 0. Цвет трека - Чёрный. Цвет тела - Серый. Радиус = 10
        @param root: Холст, на котором будет рисоваться центр масс
        """
        super().__init__(root, 0, 0, 0, 0, 0, color_self="grey", color_track="black")
        self.root.tag_raise(self.solid)
        self.r = 10

    def set_coords(self, coords):
        """! Метод установки координат.
        При обновлении координат обновляет своё положение на холсте.
        """
        self.coordinate = coords
        self.update()

    def visible(self, option):
        """! Метод установки видимости центра масс.
        """
        try:
            if option:
                self.root.tag_raise(self.solid)
                self.root.tag_raise(self.track[0])
                self.root.itemconfig(self.solid, fill="grey")
            else:
                self.root.tag_lower(self.solid)
                self.root.tag_lower(self.track[0])
                self.root.itemconfig(self.solid, fill="black")
        except TclError:
            pass




def find_F(a: MSolid, b: MSolid) -> tuple:
    """! Функция находит силу гравитационного притяжения действующую со стороны тела b на тело a и возвращает её в виде вектора
    @param a: Тело на которое действует сила.
    @param b: Тело, которое вызывает силу.
    @return: Вектор силы гравитации.
    """
    x1, y1 = a.coordinate
    x2, y2 = b.coordinate
    m1 = a.mass
    m2 = b.mass
    R = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if R == 0:
        raise ZeroDivisionError("Центры масс сошлись. Ошибка колизии")
    F = 6.67 * (10 ** (-11)) * ((m1 * m2) / R ** 2)
    return F * ((x2 - x1) / R), F * ((y2 - y1) / R)


def center_mass(body: list[MSolid]) -> tuple:
    """! Находит и вовращает координыты центра масс для тел переданных в функцию
    @param body: Итератор, который включает в себя тела, для которых надо найти центр масс
    @return: Координаты центра масс в виде (х, y)
    """
    if len(body) == 0:
        return (0, 0)
    M = [0, 0]
    for a in body:
        M[0] += a.mass * a.coordinate[0]
        M[1] += a.mass * a.coordinate[1]
    m = 0
    for a in body:
        m += a.mass

    return M[0] / m, M[1] / m
