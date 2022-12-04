import tkinter
from math import sqrt, pi


class MSolid:
    """
    Класс описывет тело для гравитационного взаимодействия
    """

    def __init__(self, root: tkinter.Canvas, c_x, x_y, v_x, v_y, mass, color_self, color_track):
        self.mass = mass
        self.coordinate = [c_x, x_y]
        self.velocity = [v_x, v_y]
        self.density = 1
        self.root = root
        self.r = sqrt(abs(self.mass / self.density / pi))
        self.solid = root.create_oval(
            int(self.coordinate[0] - self.r), int(self.coordinate[1] - self.r),
            int(self.coordinate[0] + self.r), int(self.coordinate[1] + self.r),
            fill=color_self)
        self.track = list([root.create_line(0, 0, 1, 1, fill=color_track)]) + list(self.coordinate)
        root.tag_lower(self.track[0])

    def apply_force(self, F):
        if self.mass == 0:
            return
        self.velocity[0] = self.velocity[0] + F[0] / self.mass
        self.velocity[1] = self.velocity[1] + F[1] / self.mass

    def move(self):
        self.coordinate[0] += self.velocity[0]
        self.coordinate[1] += self.velocity[1]

    def update(self):
        self.track += list(self.coordinate)
        try:
            self.root.coords(self.solid,
                             self.coordinate[0] - self.r, self.coordinate[1] - self.r,
                             self.coordinate[0] + self.r, self.coordinate[1] + self.r)
        except tkinter.TclError:
            pass

    def update_track(self, relatively=None):
        try:
            if relatively is None:
                self.root.coords(*self.track)
            else:
                track = [self.track[0]]
                for i in range(1, len(self.track), 2):
                    track.append(self.track[i] - relatively.track[i] + relatively.track[-2])
                    track.append(self.track[i + 1] - relatively.track[i + 1] + relatively.track[-1])
                self.root.coords(*track)
        except tkinter.TclError:
            pass

    def resize(self, x, y):
        for i in range(1, len(self.track), 2):
            self.track[i] += x / 2
            self.track[i + 1] += y / 2
        self.coordinate[0] += x / 2
        self.coordinate[1] += y / 2


class BodyVector:
    def __init__(self, root: tkinter.Canvas, body: MSolid, vector):
        """
        :param root:
        :param body:
        :param vector:
        """
        x = body.coordinate[0]
        y = body.coordinate[1]
        self.line = root.create_line(body.coordinate, vector[0]+x, vector[1]+y)


def find_F(a: MSolid, b: MSolid) -> tuple:
    """
    Функция находит силу гравитационного притяжения действующую со стороны тела b на тело a и возвращает её в виде вектора.\n
    :param a: Тело a
    :param b: Тело b
    :return: Вектор силы притяжения
    """
    x1, y1 = a.coordinate
    x2, y2 = b.coordinate
    m1 = a.mass
    m2 = b.mass
    R = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if R > 40:
        F = 6.67 * (10 ** (-9)) * ((m1 * m2) / R ** 2)
    else:
        F = 6.67 * (10 ** (-11)) * ((m1 * m2) / R ** 2)
    return F * ((x2 - x1) / R), F * ((y2 - y1) / R)


def center_mass(*body) -> tuple:
    """
    Находит и вовращает координыты центра масс для body (MSolid)
    :param body: итератор MSolid
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