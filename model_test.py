from math import sqrt, pi
from model import *
import pytest
from unittest.mock import Mock


# def test_fun():
#     fun = Mock()
#     fun.return_value = 1
#     # fun.side_effect = Exeption()
#     # fun.assert_called_with(args)


class Test_find_F:
    c = Mock()

    def test_find_F_1(self):
        ## Проверка на второй закон Ньютона (сила десйствия = -силе противодействия)
        a = MSolid(self.c, 10, 10, 0, 0, 100)
        b = MSolid(self.c, -10, -10, 0, 0, 100)
        assert find_F(a, b)[0] == -find_F(b, a)[0]
        assert find_F(a, b)[1] == -find_F(b, a)[1]

    def test_find_F_2(self):
        ## Проверка на то, что сила гравитации не зависит от скорости каждого тела.
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
        ## Проверка получаемых значений.
        # G (-6.67e-11) - Гравитационная постоянная.
        # Если тела будут на расстоянии 1 и оба массой 1, то сила будет равна в точности G.
        assert find_F(MSolid(self.c, 1, 0, 0, 0, 1), MSolid(self.c, 0, 0, 0, 0, 1)) == (-6.67e-11, 0)
        assert find_F(MSolid(self.c, 0, 1, 0, 0, 1), MSolid(self.c, 0, 0, 0, 0, 1)) == (0, -6.67e-11)

    def test_find_F_4(self):
        ## Проверка исключительной ситуации R=0 (в формуле происходит деление на квадрат R).
        with pytest.raises(ZeroDivisionError, match="Центры масс сошлись. Ошибка колизии"):
            assert find_F(MSolid(self.c, 0, 0, 0, 0, 1), MSolid(self.c, 0, 0, 0, 0, 1))


class Test_center_mass:
    c = Mock()

    def test_center_mass_1(self):
        for i in range(100):
            assert center_mass([MSolid(self.c, i, 0, 0, 0, 1), MSolid(self.c, -i, 0, 0, 0, 1),
                                MSolid(self.c, 0, i, 0, 0, 1), MSolid(self.c, 0, -i, 0, 0, 1)]) == (0, 0)

    def test_center_mass_2(self):
        for i in range(100):
            assert center_mass([MSolid(self.c, i, 0, 0, 0, 1), MSolid(self.c, 0, 0, 0, 0, 1)]) == (i/2, 0)

    def test_center_mass_3(self):
        for i in range(1, 100):
            assert center_mass([MSolid(self.c, 2, 0, 0, 0, i), MSolid(self.c, 0, 0, 0, 0, 1)]) == ((2*i)/(i+1), 0)
            assert center_mass([MSolid(self.c, 0, 2, 0, 0, i), MSolid(self.c, 0, 0, 0, 0, 1)]) == (0, (2*i)/(i+1))


class Test_MSolid:
    c = Mock()
    c.create_oval = Mock()
    c.create_line = Mock()
    c.create_oval.return_value = 1
    c.create_line.return_value = 2

    def test_MSolid_init_1(self):
        for i in range(200):
            for j in range(200):
                t = MSolid(self.c, i - 100, j - 100, 0, 0, 0)
                assert t.coordinate == [i - 100, j - 100]
                self.c.create_oval.assert_called_with(i - 100, j - 100, i - 100, j - 100, fill='white')
                self.c.create_line.aassert_called_with(0, 0, 0, 0, fill="green")

    def test_MSolid_init_2(self):
        for i in range(200):
            t = MSolid(self.c, 0, 0, 0, 0, i)
            assert t.mass == i
            self.c.create_oval.assert_called_with(-int(sqrt(abs(i / pi))), -int(sqrt(abs(i / pi))),
                                                  int(sqrt(abs(i / pi))), int(sqrt(abs(i / pi))), fill='white')

    def test_MSolid_init_3(self):
        for i in ('white', 'green', 'red', "FFFFFF", "000000"):
            MSolid(self.c, 0, 0, 0, 0, 0, color_self=i, color_track=i)
            self.c.create_oval.assert_called_with(0, 0, 0, 0, fill=i)
            self.c.create_line.assert_called_with(0, 0, 0, 0, fill=i)

    def test_MSolid_apply_force(self):
        for i in range(200):
            a = MSolid(self.c, 10, 10, 0, 0, 0)
            a.apply_force((i - 100, 100 - i))
            assert a.force == [i - 100, 100 - i]
            a.apply_force((i - 100, 100 - i))
            assert a.force == [2* (i - 100), 2 *(100 - i)]

    def test_MSolid_move_1(self):
        for i in range(200):
            a = MSolid(self.c, 0, 0, i - 100, 100 - i, 1)
            a.move()
            assert a.coordinate == [i - 100, 100 - i]

    def test_MSolid_move_2(self):
        for i in range(200):
            a = MSolid(self.c, 0, 0, 0, 0, 1)
            a.apply_force((i - 100, 100 - i))
            a.move()
            assert a.coordinate == [i - 100, 100 - i]
            assert a.velocity == [i - 100, 100 - i]

    def test_MSolid_move_3(self):
        for i in range(1, 200):
            a = MSolid(self.c, 0, 0, 0, 0, i)
            a.apply_force((100, 100))
            a.move()
            assert a.coordinate == [100 / i, 100 / i]

    def test_MSolid_update(self):
        for i in range(200):
            for j in range(200):
                t = MSolid(self.c, i - 100, j - 100, 0, 0, 0)
                t.update()
                self.c.coords.assert_called_with(1, i - 100, j - 100, i - 100, j - 100)

    def test_MSolid_update_trak(self):
        t = MSolid(self.c, 0, 0, 0, 0, 0)
        for i in range(1, 200):
            t.update()
            t.update_track()
            self.c.coords.assert_called_with(2, *[0, 0]*(1+i))

    def test_MSolid_replace(self):
        for i in range(-100, 100):
            t = MSolid(self.c, 0, 0, 0, 0, 0)
            t.replace(i, 0)
            assert t.coordinate == [i, 0]
            t.replace(0, i)
            assert t.coordinate == [i, i]

    def test_MSolid_resize(self):
        for i in range(1, 10):
            t = MSolid(self.c, 100, 100, 0, 0, 100)
            t.resize(i, 0, 0)
            assert t.mass == 100 * (i + 1)
            assert t.coordinate[0] == 100 * (i + 1)
            assert t.coordinate[1] == 100 * (i + 1)




