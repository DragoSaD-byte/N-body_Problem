import tkinter as tk
from tkinter import colorchooser, messagebox
from model import *


class App(tk.Tk):
    """
    Класс основного приложения.
    """

    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.config(height=288, width=730)
        self.mainmenu = tk.Menu(self)
        self.config(menu=self.mainmenu)
        self.mainmenu.add_command(label="Запуск симуляции", command=self.start_sim)
        self.mainmenu.add_command(label="Добавить тело", command=self.add_body)
        self.mainmenu.add_command(label="Убрать тело", command=self.pop_body)
        self.bot_frame = tk.LabelFrame(self, text="Тела:", )
        self.bot_frame.place(x=10, y=0)
        self.outputs = []
        self.sims = set()

        # Задание стартовых настроек
        self.add_body((250, 200, -0.000022, 0, 3000, "white", "green"))
        self.add_body((250, 300, 0.000022, 0, 3000, "white", "green"))
        # self.add_body((250, 250, -0.00000022, 0, 3000, "white", "green"))
        # self.add_body((253, 50, 0.000033, -0.000002, 10, "white", "green"))
        # self.add_body((247, 50, 0.000033, 0.000002, 10, "white", "green"))

    def add_body(self, inputs=tuple([0, 0, 0, 0, 0, "white", "green"])):
        """! Метод добавления дополниельного поля ввода для параметров тела.
        @param inputs: Опцианально. Начальные значения полей.
        """
        if len(self.outputs) == 9:
            return
        frame = tk.LabelFrame(self.bot_frame, text=f"Тело {len(self.outputs) + 1}")
        output = [frame]
        for i in inputs[:-2]:
            output.append(tk.Text(frame, width=7, height=1))
            output[-1].insert(1.0, i)
        output.append(tk.Button(frame, text="Тело", width=3, height=1, bg=inputs[5]))
        output.append(tk.Button(frame, text="Трек", width=3, height=1, bg=inputs[6]))

        tk.Label(frame, text="Coord").grid(row=0, column=0, columnspan=2)
        tk.Label(frame, text="X:").grid(row=1, column=0)
        tk.Label(frame, text="Y:").grid(row=2, column=0)
        output[1].grid(row=1, column=1)
        output[2].grid(row=2, column=1)

        tk.Label(frame, text="V").grid(row=0, column=3, columnspan=2)
        tk.Label(frame, text="X:").grid(row=1, column=3)
        tk.Label(frame, text="Y:").grid(row=2, column=3)
        output[3].grid(row=1, column=4)
        output[4].grid(row=2, column=4)

        tk.Label(frame, text="Mass, Color").grid(row=0, column=5, columnspan=3)
        tk.Label(frame, text="M:").grid(row=1, column=5)
        output[5].grid(row=1, column=6, columnspan=2)

        output[6].config(command=lambda: output[6].config(bg=colorchooser.askcolor()[1]))
        output[7].config(command=lambda: output[7].config(bg=colorchooser.askcolor()[1]))

        output[6].grid(row=2, column=5, columnspan=2)
        output[7].grid(row=2, column=7)

        frame.grid(row=len(self.outputs) // 3, column=len(self.outputs) % 3)
        self.outputs.append(output)

    def pop_body(self):
        """! Метод удаления последнего поля конфигурации тела.
        """
        if len(self.outputs) > 1:
            self.outputs[-1][0].destroy()
            self.outputs.pop(-1)

    def start_sim(self):
        """! Метод создания окна симуляции.
        """
        try:
            self.sims.add(sim(self.read_conf()))
        except ValueError:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены числами")

    def read_conf(self):
        """! Метод считывания настроек.
        @throw ValueError: Возникает, если в одном из полей конфигурации тела было введено не число.
        """
        ret = []
        try:
            for i in self.outputs:
                a = list(float(j.get('1.0', tk.END)) for j in i[1:-2])
                a.append(i[-2].cget('bg'))
                a.append(i[-1].cget('bg'))
                ret.append(tuple(a))
            return tuple(ret)
        except ValueError:
            raise ValueError("В одном из полей не число")


class sim(tk.Toplevel):
    """! Класс окна симуляции.
    """

    def __init__(self, conf):
        """! Метод инициализации.
        @param conf: Итератор, в котором находятся стартовые параметры для тел симуляции.
        """
        super().__init__()
        self.canvas = tk.Canvas(self, height=500, width=500, background="black")
        tk.Scrollbar(self.canvas)
        self.body = tuple(MSolid(self.canvas, *i) for i in conf)
        self.canvas.pack()
        self.resizable(False, False)
        self.vectors = tuple(
            {
                "velocity": None,
                "f": None
            } for _ in range(len(self.body)))

        def click(event):
            """! Метод обработчик нажатия на левую кнопку мышки.
            @args: Событие клика.
            """
            self.last_cords = (event.x, event.y)

        def motion(event):
            """! Метод обработки передвижения курсора вместе с нажатием левой кнопки мыши.
            @args: Событие передвижения миши с нажатой левой кнопкой мыши.
            """
            dx = event.x - self.last_cords[0]
            dy = event.y - self.last_cords[1]
            for i in self.body:
                i.replace(dx, dy)
            self.last_cords = (event.x, event.y)

        def mouse_wheel(event):
            """! Метод обработки движения колеса.
            @args: Событие прокрутки колёсика.
            """

            x = event.x
            y = event.y
            for i in self.body:
                i.resize(event.delta // 120, x, y)

        self.last_cords = (0, 0)
        self.bind("<Button-1>", click)
        self.bind_all("<B1-Motion>", motion)
        self.bind("<MouseWheel>", mouse_wheel)

        self.create_menu()
        self.update_sim()

    def create_menu(self):
        """! Метод создания меню. Вспомогательный метод для инициализации.
        """
        menu = tk.Menu(self, tearoff=0)

        self.bind("<Button-3>", lambda event: menu.post(event.x_root, event.y_root))

        self.relatively = tk.IntVar()
        self.relatively.set(-1)
        relatively_menu = tk.Menu(menu, tearoff=0)
        relatively_menu.add_radiobutton(label="Начала координат", value=-1, variable=self.relatively)
        for i in range(len(self.body)):
            relatively_menu.add_radiobutton(label="Тела " + str(i + 1), value=i, variable=self.relatively)
        menu.add_cascade(label="Траектория относительно", menu=relatively_menu)
        menu.add_separator()

        self.vectors_settings = tuple(
            {
                "velocity": tk.IntVar(name=str(i) + " velocity"),
                "f": tk.IntVar(name=str(i) + " f")
            } for i in range(len(self.body)))

        for i in range(len(self.body)):
            self.vectors_settings[i]["velocity"].trace("w", self.change_processing)
            self.vectors_settings[i]["f"].trace("w", self.change_processing)
            body_menu = tk.Menu(menu, tearoff=0)
            body_menu.add_checkbutton(label="Скорость", variable=self.vectors_settings[i]["velocity"])
            body_menu.add_checkbutton(label="Сила", variable=self.vectors_settings[i]["f"])
            menu.add_cascade(label="Тело " + str(i), menu=body_menu)

    def change_processing(self, args):
        """! Функция обработки изменения флагов отображения векторов.
        @args: Событие изменения флага.
        """
        i, v = args[0].split()
        if self.vectors_settings[int(i)][v].get():
            self.vectors[int(i)][v] = BodyVector(self.canvas, self.body[int(i)], v)
        else:
            self.vectors[int(i)][v] = None


    def update_sim(self):
        """!Метод обновления симуляции.
        Симулирует 10000 шагов симуляции, после чего отрисовывает изменения.
        Метод после выполнения ставит задачу выполнить самого себя ещё раз.
        """
        # Шаги симуляции
        for _ in range(10000):
            # Рассчет сил для каждого тела
            for i in range(len(self.body)):
                for j in range(i + 1, len(self.body)):
                    f = find_F(self.body[i], self.body[j])
                    self.body[i].apply_force(f)
                    self.body[j].apply_force((-f[0], -f[1]))
            # Сдвиг тел
            for i in self.body:
                i.move()
        # Обновление тел и треков
        for i in self.body:
            i.update()
            if self.relatively.get() != -1:
                i.update_track(relatively=self.body[self.relatively.get()])
            else:
                i.update_track()
        # Проверка обновлений векторов
        for vector in self.vectors:
            for key in vector.keys():
                if vector[key]:
                    vector[key].update()
        # Отрисовка и новая задача обновить экран
        self.update()
        self.after(0, self.update_sim)


if __name__ == "__main__":
    App().mainloop()
