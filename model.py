## @package model
#  Documentation for this module.
#
#  More details.


from math import sqrt, pi
from tkinter import TclError


## Класс описывет тело для гравитационного взаимодействия.
class MSolid:
    def __init__(self, root, c_x, c_y, v_x, v_y, mass, color_self="white", color_track="green",
                 f_x=0, f_y=0, density=1):
        self.mass = mass
        self.coordinate = [c_x, c_y]
        self.velocity = [v_x, v_y]
        self.force = [f_x, f_y]
        self.density = density
        self.root = root
        self.r = sqrt(abs(self.mass / self.density / pi))
        self.f = [0, 0]
        self.solid = root.create_oval(
            int(self.coordinate[0] - self.r), int(self.coordinate[1] - self.r),
            int(self.coordinate[0] + self.r), int(self.coordinate[1] + self.r),
            fill=color_self)
        self.track = list([root.create_line(0, 0, 0, 0, fill=color_track)]) + list(self.coordinate)
        root.tag_lower(self.track[0])

    def apply_force(self, F):
        self.force[0] = self.force[0] + F[0]
        self.force[1] = self.force[1] + F[1]

    def move(self):
        if self.mass == 0:
            return
        self.velocity[0] += self.force[0] / self.mass
        self.velocity[1] += self.force[1] / self.mass
        self.f = list(self.force)
        self.force = [0, 0]
        self.coordinate[0] += self.velocity[0]
        self.coordinate[1] += self.velocity[1]

    def update(self):
        self.track += list(self.coordinate)
        try:
            self.root.coords(self.solid,
                             int(self.coordinate[0] - self.r), int(self.coordinate[1] - self.r),
                             int(self.coordinate[0] + self.r), int(self.coordinate[1] + self.r))
        except TclError:
            pass

    def update_track(self, relatively=None):
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
        for i in range(1, len(self.track), 2):
            self.track[i] += x
            self.track[i + 1] += y
        self.coordinate[0] += x
        self.coordinate[1] += y

    def resize(self, delta, x, y):
        for i in range(1, len(self.track), 2):
            self.track[i] = x + (self.track[i] - x) * (1 + delta)
            self.track[i + 1] = y + (self.track[i + 1] - y) * (1 + delta)
        self.coordinate[0] = x + (self.coordinate[0] - x) * (1 + delta)
        self.coordinate[1] = y + (self.coordinate[1] - y) * (1 + delta)
        self.mass *= 1 + delta

        self.density /= 1 + delta
        self.r = sqrt(abs(self.mass / self.density / pi))


# # Класс отрисовывает рядом с телом на холсте root некий вектор vector (одномерный массив длинной 2),
# который принадлежит телу body.
class BodyVector:
    def __init__(self, root, body: MSolid, vector: str, color="red"):
        ## @brief Тип Canvas, холст на котором будет рисоваться тело
        self.root = root
        ## @brief Тип MSolid, вектор, которого будет отривовываться
        self.body = body
        ## @brief Строка - название двумерный вектора (одномерный массив длинной 2) в body, который будет отрисовываться
        self.vector = vector
        try:
            if len(eval("self.body." + self.vector)) != 2:
                raise AttributeError("При создании BodyVector передан не вектор")
        except AttributeError:
            raise AttributeError("Попытка обратится к несуществующему вектору при создании BodyVector")
        except TypeError:
            raise AttributeError("При создании BodyVector передан не вектор")
        x = self.body.coordinate[0]
        y = self.body.coordinate[1]
        self.a = 10 ** (len(str(
            int(30 / sqrt(eval("self.body." + self.vector)[0] ** 2 + eval("self.body." + self.vector)[1] ** 2)))) - 1)

        self.line = self.root.create_line(x, y, eval("self.body." + self.vector)[0] + x,
                                          eval("self.body." + self.vector)[1] + y, width=1, fill=color)

    ## Метод обновления и переотрисовки
    def update(self):
        x = self.body.coordinate[0]
        y = self.body.coordinate[1]
        try:
            self.root.coords(self.line, x, y, eval("self.body." + self.vector)[0] * self.a + x,
                             eval("self.body." + self.vector)[1] * self.a + y)
        except TclError:
            pass

    ## Деструктор
    def __del__(self):
        self.root.delete(self.line)


## Функция находит силу гравитационного притяжения действующую со стороны тела b на тело a и возвращает её в виде вектора.
def find_F(a: MSolid, b: MSolid) -> tuple:
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
    """
    Находит и вовращает координыты центра масс для тел переданных в функцию
    :param body:
    :return:
    """
    M = [0, 0]
    for a in body:
        M[0] += a.mass * a.coordinate[0]
        M[1] += a.mass * a.coordinate[1]
    m = 0
    for a in body:
        m += a.mass

    return M[0] / m, M[1] / m
