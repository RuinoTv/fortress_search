import tkinter as tk
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class StrongholdFinder:
    def __init__(self, master):
        self.master = master
        self.stage = 1
        self.coords1 = None

        master.title("пойск координат портала с двумя глазами око")

        self.label = tk.Label(master, text="Введите первые координаты")
        self.label.pack()

        self.entry_x = self._make_entry("X")
        self.entry_z = self._make_entry("Z")
        self.entry_yaw = self._make_entry("Head Pos")

        self.button = tk.Button(master, text="Подтвердить", command=self.confirm)
        self.button.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

        # график
        self.fig = plt.Figure(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack()

    def _make_entry(self, label_text):
        tk.Label(self.master, text=label_text).pack()
        entry = tk.Entry(self.master)
        entry.pack()
        return entry

    def _get_values(self):
        try:
            return float(self.entry_x.get()), float(self.entry_z.get()), float(self.entry_yaw.get())
        except ValueError:
            self.result_label.config(text="Ошибка: введите числа!")
            return None

    def confirm(self):
        values = self._get_values()
        if not values:
            return

        if self.stage == 1:
            self.coords1 = values
            self._clear_entries()
            self.label.config(text="Введите вторые координаты")
            self.button.config(text="Рассчитать")
            self.stage = 2
        else:
            coords2 = values
            self._calculate_and_plot(self.coords1, coords2)

            #сбрасывает код

            self._clear_entries()
            self.label.config(text="Введите первые координаты")
            self.button.config(text="Подтвердить")
            self.stage = 1
            self.coords1 = None

    def _clear_entries(self):
        self.entry_x.delete(0, tk.END)
        self.entry_z.delete(0, tk.END)
        self.entry_yaw.delete(0, tk.END)

    def _calculate_and_plot(self, coords1, coords2):
        x1, z1, yaw1 = coords1
        x2, z2, yaw2 = coords2

        # перевод углов в радианы
        yaw1_rad, yaw2_rad = math.radians(yaw1), math.radians(yaw2)

        dx1, dz1 = -math.sin(yaw1_rad), math.cos(yaw1_rad)
        dx2, dz2 = -math.sin(yaw2_rad), math.cos(yaw2_rad)

        # точка пересечения
        t = ((x2 - x1) * dz2 - (z2 - z1) * dx2) / (dx1 * dz2 - dz1 * dx2)
        X, Z = x1 + t * dx1, z1 + t * dz1

        self.result_label.config(text=f"Крепость примерно тут:\nX = {round(X)}\nZ = {round(Z)}")

        # рисует график
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.set_title("Поиск крепости")
        ax.set_xlabel("X")
        ax.set_ylabel("N")

        ax.plot([x1, x2], [z1, z2], 'ro', label="Игроки")

        self._draw_direction(ax, x1, z1, X, Z, "Око 1")
        self._draw_direction(ax, x2, z2, X, Z, "Око 2")

        ax.plot(X, Z, 'go', label="Крепость")
        ax.legend()
        self.canvas.draw()

    def _draw_direction(self, ax, x, z, X, Z, label):
        extend = 50
        vec_x, vec_z = X - x, Z - z
        length = math.hypot(vec_x, vec_z)
        factor = (length + extend) / length
        end_x, end_z = x + vec_x * factor, z + vec_z * factor
        ax.plot([x, end_x], [z, end_z], 'b-', label=label)


if __name__ == "__main__":
    root = tk.Tk()
    app = StrongholdFinder(root)
    root.mainloop()