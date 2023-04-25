import tkinter as tk
from PIL import Image, ImageTk
import math
import filosofos as ph
import colorama


class MyViewer():
    def __init__(self):
        super(MyViewer, self).__init__()

        self.window = tk.Tk()
        self.window.title("Filósofos comensales")

        self.canvas: tk.Canvas = tk.Canvas(self.window, width=500, height=500)
        self.canvas.pack()

        self.images = self.load_images()
        self.draw_complete_scenario()

        play_button = tk.Button(text='Play simulation', command=self.myTask)
        play_button.pack(ipadx=5, ipady=5, expand=True)

        self.window.mainloop()

    def philosopher_status_changed(
            self, philosopher_num: int, new_status):
        print(colorama.Fore.YELLOW, philosopher_num, new_status)

        self.draw_philosopher(philosopher_num, self.images[new_status])

    def fork_status_changed(self, fork_num: int, new_status):
        print(colorama.Fore.LIGHTGREEN_EX, fork_num, new_status)

    def draw_complete_scenario(self):
        # Dibuja mesa
        self.canvas.create_oval(100, 100, 400, 400, width=5)

        for i in range(5):
            # draw_philosopher(i, images['thinking'])
            self.draw_philosopher(
                0, self.images[ph.PhilosopherStatus.THINKING])
            self.draw_fork(i, self.images['fork_'+str(i)])
            # draw_fork(0, images['fork_0'])

    def draw_fork(self, fork_num, image: ImageTk.PhotoImage, color=""):
        # Tenedor
        angle = fork_num * 2 * math.pi / 5 + math.pi/5
        x = 250 + 100 * math.cos(angle)
        y = 250 - 100 * math.sin(angle)

        self.canvas.create_image(x, y, image=image, anchor='center')

    def draw_table(self):
        self.canvas.create_oval(100, 100, 400, 400, width=5)

    def draw_philosopher(self, philosopher_num:int, image, color=""):
        angle = philosopher_num * 2 * math.pi / 5
        x = 250 + 175 * math.cos(angle)
        y = 250 - 175 * math.sin(angle)
        self.canvas.create_image(x, y, image=image, anchor='center')

    def load_image(self, filename, rotate_angle=0, widh=75, high=75):
        img = Image.open(filename)
        img = img.resize((widh, high), Image.ANTIALIAS)
        img = img.rotate(rotate_angle)

        return ImageTk.PhotoImage(img)

    def load_images(self) -> list:
        images = {
            ph.PhilosopherStatus.THINKING: self.load_image(
                "smile_thinking.png", 0, 100, 100),
            ph.PhilosopherStatus.RESTING: self.load_image(
                "smile_resting.png", 0, 75, 75),
            ph.PhilosopherStatus.EATING: self.load_image(
                "smile_eating.png", 0, 100, 100),
            'fork_0': self.load_image("fork.png", 0+175),
            'fork_1': self.load_image("fork.png", 360/5+175),
            'fork_2': self.load_image("fork.png", 360/5*2+175),
            'fork_3': self.load_image("fork.png", 360/5*3+175),
            'fork_4': self.load_image("fork.png", 360/5*4+175)
        }

        return images

    def myTask(self):
        sim = ph.Simulator(self.philosopher_status_changed,
                           self.fork_status_changed)
        sim.run()


def main():
    vw = MyViewer()


if __name__ == '__main__':
    main()

