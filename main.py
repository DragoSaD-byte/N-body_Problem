import tkinter
from model import *




class App:
    def __init__(self):
        self.configurationWindow = tkinter.Tk()
        self.configurationWindow.config(height=300, width=730)
        self.mainmenu = tkinter.Menu(self.configurationWindow)
        self.configurationWindow.config(menu=self.mainmenu)
        self.mainmenu.add_command(label="Запуск симуляции", command=self.start_sim)
        self.mainmenu.add_command(label="Добавить тело", command=self.add_body)
        self.mainmenu.add_command(label="Убрать тело", command=self.pop_body)
        self.mainmenu.add_command(label="Сохранить настройки", command=self.load)
        self.mainmenu.add_command(label="Загрузить настройки", command=self.save)
        self.bot_frame = tkinter.LabelFrame(self.configurationWindow, text="тела:")
        self.bot_frame.place(x=10, y=0)
        self.outputs = []
        self.sims = set()

        self.add_body((250, 250, -0.0000022, 0, 3000, "white", "green"))
        self.add_body((253, 50, 0.00033, -0.000002, 10, "white", "green"))
        self.add_body((247, 50, 0.00033, 0.000002, 10, "white", "green"))

    def add_body(self, inputs=tuple([0, 0, 0, 0, 0, "white", "green"])):
        frame = tkinter.LabelFrame(self.bot_frame, text=f"Тело {len(self.outputs) + 1}")
        output = [frame]
        for i in inputs[:-2]:
            output.append(tkinter.Text(frame, width=7, height=1))
            output[-1].insert(1.0, i)
        output.append(tkinter.Button(frame, text="Тело", width=3, height=1, bg=inputs[5]))
        output.append(tkinter.Button(frame, text="Трек", width=3, height=1, bg=inputs[6]))

        tkinter.Label(frame, text="Coord").grid(row=0, column=0, columnspan=2)
        tkinter.Label(frame, text="X:").grid(row=1, column=0)
        tkinter.Label(frame, text="Y:").grid(row=2, column=0)
        output[1].grid(row=1, column=1)
        output[2].grid(row=2, column=1)

        tkinter.Label(frame, text="V").grid(row=0, column=3, columnspan=2)
        tkinter.Label(frame, text="X:").grid(row=1, column=3)
        tkinter.Label(frame, text="Y:").grid(row=2, column=3)
        output[3].grid(row=1, column=4)
        output[4].grid(row=2, column=4)

        tkinter.Label(frame, text="Mass").grid(row=0, column=5, columnspan=3)
        tkinter.Label(frame, text="M:").grid(row=1, column=5)
        output[5].grid(row=1, column=6, columnspan=2)

        output[6].grid(row=2, column=5, columnspan=2)
        output[7].grid(row=2, column=7)

        frame.grid(row=len(self.outputs) // 3, column=len(self.outputs) % 3)
        self.outputs.append(output)

    def load(self):
        for i in self.outputs:
            print(*(bool(j) for j in i))

    def save(self):
        pass

    def pop_body(self):
        if len(self.outputs) > 1:
            self.outputs[-1][0].destroy()
            self.outputs.pop(-1)

    def start_sim(self):
        sim(self.read_conf())

    def read_conf(self):
        ret = []
        for i in self.outputs:
            a = list(float(j.get('1.0', tkinter.END)) for j in i[1:-2])
            a.append(i[-2].cget('bg'))
            a.append(i[-1].cget('bg'))
            ret.append(tuple(a))
        return tuple(ret)

    def mainloop(self):
        self.configurationWindow.mainloop()

class sim(tkinter.Tk):
    def __init__(self, conf):
        super().__init__()
        self.canvas = tkinter.Canvas(self, height=500, width=500, background="black")
        self.body = tuple(MSolid(self.canvas, *i) for i in conf)
        self.canvas.pack()
        self.update_sim()

    def update_sim(self):
        for _ in range(10000):
            for i in range(len(self.body)):
                for j in range(i + 1, len(self.body)):
                    f = find_F(self.body[i], self.body[j])
                    self.body[i].apply_force(f)
                    self.body[j].apply_force((-f[0], -f[1]))
            for i in self.body:
                i.move()
        for i in self.body:
            i.update()
            i.update_track()
        self.update()
        self.after(0, self.update_sim)


App().mainloop()
