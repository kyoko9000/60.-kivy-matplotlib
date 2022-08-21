# **************kivyMD GUI ********************************
from kivy import Config
from kivy.clock import Clock
from kivy.core.text import Label
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.progressbar import ProgressBar
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
plt.plot([1, 23, 2, 4])
plt.ylabel('some numbers')

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')
Config.write()


class MainWindow(MDScreen):
    def __init__(self):
        super(MainWindow, self).__init__()
        box_1 = BoxLayout()
        box_1.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        box = BoxLayout(
            orientation='vertical'
        )
        toolbar = MDTopAppBar(
            title="Menu",
        )
        # toolbar.md_bg_color = [1, 0.2, 0.2, 1]
        toolbar.left_action_items = [["menu", lambda x: print('menu')]]
        toolbar.right_action_items = [["logout", lambda x: print('exit')]]

        bottom = MDBottomNavigation()
        # bottom.md_bg_color = [0.4, 0.4, 0.4, 1]
        # bottom.panel_color = [0.2, 0.2, 0.2, 1]
        with bottom.canvas:
            Color(33 / 255, 150 / 255, 243 / 255, 0.3)
            bottom.rect = Rectangle(
                pos=bottom.pos,
                size=bottom.size,
            )
        bottom.bind(pos=lambda obj, pos: setattr(bottom.rect, "pos", pos))
        bottom.bind(size=lambda obj, size: setattr(bottom.rect, "size", (bottom.width, 56.0)))

        item_1 = MDBottomNavigationItem(
            name='screen 1',
            text='main',
            icon='home'
        )
        self.box = BoxLayout(
            size_hint=(None, None),
            size=(300, 300),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        item_2 = MDBottomNavigationItem(
            name='screen 2',
            text='contacts',
            icon='contacts'
        )
        label_2 = MDLabel(
            text='sub screen 1',
            halign='center'
        )
        item_3 = MDBottomNavigationItem(
            name='screen 3',
            text='account',
            icon='account'
        )
        label_3 = MDLabel(
            text='sub screen 2',
            halign='center'
        )

        item_1.add_widget(box_1)
        item_2.add_widget(label_2)
        item_3.add_widget(label_3)
        bottom.add_widget(item_1)
        bottom.add_widget(item_2)
        bottom.add_widget(item_3)

        box.add_widget(toolbar)
        box.add_widget(bottom)
        self.add_widget(box)

        self.l = ProgressBar()
        self.l.size_hint = (None, None)
        self.l.height = 50
        self.l.width = 50
        self.l.max = 100

        self.change_value = 39.263
        # Animate the progress bar
        Clock.schedule_interval(self.animate, 0.1)

        # Set constant for the bar thickness_1
        self.thickness_1 = 40

        # Create a direct text representation
        self.label_1 = Label(text="0%", font_size=self.thickness_1)

        # Initialise the texture_size_1 variable
        self.texture_size_1 = None

        # Refresh the text
        self.refresh_text()

    def animate(self, dt):
        # self.set_value(60.56)
        if self.l.value < self.change_value:
            self.set_value(self.l.value + 1)
        # else:
        #     self.set_value(0)

    def set_value(self, value):
        # Update the progress bar value
        self.l.value = value

        # Update textual value and refresh the texture
        self.label_1.text = str(round(self.l.value_normalized * 100, 2)) + "%"
        self.refresh_text()

        # Draw all the elements
        self.draw()

    def refresh_text(self):
        # Render the label_1
        self.label_1.refresh()

        # Set the texture size each refresh
        self.texture_size_1 = list(self.label_1.texture.size)

    def draw(self):
        with self.box.canvas:
            # Empty canvas instructions
            self.box.canvas.clear()

            # Draw no-progress circle
            Color(0.26, 0.26, 0.26)
            Ellipse(pos=self.box.pos, size=self.box.size)

            # Draw progress circle, small hack if there is no progress (angle_end = 0 results in full progress)
            Color(1, 0, 0)
            Ellipse(pos=self.box.pos, size=self.box.size,
                    angle_end=(0.001 if self.l.value_normalized == 0 else self.l.value_normalized * 360))
            #
            # # Draw the inner circle (colour should be equal to the background)
            Color(0.2, 0.8, 0)
            Ellipse(pos=(self.box.pos[0] + self.thickness_1 / 2, self.box.pos[1] + self.thickness_1 / 2),
                    size=(self.box.size[0] - self.thickness_1, self.box.size[1] - self.thickness_1))

            # Center and draw the progress text
            Color(1, 1, 1, 1)
            # added pos[0]and pos[1] for centralizing label_1 text whenever pos_hint is set
            Rectangle(texture=self.label_1.texture, size=self.texture_size_1,
                      pos=(self.box.size[0] / 2 - self.texture_size_1[0] / 2 + self.box.pos[0],
                           self.box.size[1] / 2 - self.texture_size_1[1] / 2 + self.box.pos[1]))


class MyApp(MDApp):
    def __init__(self):
        super().__init__()

    def build(self):
        return MainWindow()


if __name__ == '__main__':
    MyApp().run()