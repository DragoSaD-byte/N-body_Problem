import tkinter
from model import *
from random import randint
import pytest


class Test_find_F:
    c = tkinter.Canvas()

    def test_find_F_1(self):
        """
        Проверка на второй закон Ньютона (сила десйствия = -силе противодействия).
        """
        a = MSolid(self.c, 10, 10, 0, 0, 100)
        b = MSolid(self.c, -10, -10, 0, 0, 100)
        assert find_F(a, b)[0] == -find_F(b, a)[0]
        assert find_F(a, b)[1] == -find_F(b, a)[1]

    def test_find_F_2(self):
        """
        Проверка на то, что сила гравитации не зависит от скорости каждого тела.
        """
        a = MSolid(self.c, 10, 10, 0, 0, 100)
        b = MSolid(self.c, -10, -10, 0, 0, 100)
        test = find_F(a, b)
        for i1 in range(100):
            for i2 in range(100):
                a = MSolid(self.c, 10, 10, i1, 0, 100)
                b = MSolid(self.c, -10, -10, i2, 0, 100)
                assert find_F(a, b)[0] == test[0]
                assert find_F(a, b)[1] == test[1]
                a = MSolid(self.c, 10, 10, 0, i1, 100)
                b = MSolid(self.c, -10, -10, 0, i2, 100)
                assert find_F(a, b)[0] == test[0]
                assert find_F(a, b)[1] == test[1]

    def test_find_F_3(self):
        """
        Проверка получаемых значений.
        """
        # G (-6.67e-11) - Гравитационная постоянная.
        # Если тела будут на расстоянии 1 и оба массой 1, то сила будет равна в точности G.
        assert find_F(MSolid(self.c, 1, 0, 0, 0, 1), MSolid(self.c, 0, 0, 0, 0, 1)) == (-6.67e-11, 0)
        assert find_F(MSolid(self.c, 0, 1, 0, 0, 1), MSolid(self.c, 0, 0, 0, 0, 1)) == (0, -6.67e-11)

    def test_find_F_4(self):
        """
        Проверка исключительной ситуации R=0 (в формуле происходит деление на квадрат R).
        """
        with pytest.raises(ZeroDivisionError, match="Центры масс сошлись. Ошибка колизии"):
            assert find_F(MSolid(self.c, 0, 0, 0, 0, 1), MSolid(self.c, 0, 0, 0, 0, 1))


class Test_MSolid:
    c = tkinter.Canvas()

    def test_MSolid_init(self):
        """
        Проверка иициализации
        """
        pass

    def test_MSolid_apply_force(self):
        """
        Проверка
        """
        for i in range(200):
            a = MSolid(self.c, 10, 10, 0, 0, 0)
            a.apply_force((i-100, 100-i))
            assert a.force == [i-100, 100-i]

    def test_MSolid_move_1(self):
        """
        Проверка, что при вызове функции тело движется с заданной скоростью
        """
        for i in range(200):
            a = MSolid(self.c, 0, 0, i-100, 100-i, 1)
            a.move()
            assert a.coordinate == [i-100, 100-i]

    def test_MSolid_move_2(self):
        """
        Проверка
        """
        for i in range(200):
            a = MSolid(self.c, 0, 0, 0, 0, 1)
            a.apply_force((i-100, 100-i))
            a.move()
            assert a.coordinate == [i-100, 100-i]

    def test_MSolid_move_3(self):
        """
        Проверка
        """
        for i in range(1, 200):
            a = MSolid(self.c, 0, 0, 0, 0, i)
            a.apply_force((100, 100))
            a.move()
            assert a.coordinate == [100/i, 100/i]
