import kivy
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import RenderContext
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.factory import Factory
# from kivy.storage.jsonstore import JsonStore
from flatstore import FlatStore
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.base import EventLoop
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.uix.textinput import TextInput

class RangeInput(TextInput):
    min_value = NumericProperty(0)
    max_value = NumericProperty(100)

    def insert_text(self, substring, from_undo=False):
        s = self.text+str(substring)
        try:
            if self.min_value <= int(s) <= self.max_value:
                pass
        except:
            s = self.text
        return super().insert_text(s, from_undo=from_undo)

class ShaderView(FloatLayout):
    fs = StringProperty()
    disabled_value = NumericProperty(0)
    time = 0
    dtime = 1 / 60.
    mouse_pos = [0,0]

    def __init__(self,**kwargs):
        self.canvas = RenderContext()
        super(ShaderView,self).__init__(**kwargs)
        Clock.schedule_interval(self.update_shader,self.dtime)

    def update_shader(self, *args):
        if self.disabled_value == 0:
            s = self.canvas
            s['time'] = self.time
            s['resolution'] = list(map(float, self.size))
            s['mouse'] = list(map(float, self.mouse_pos))
            s['projection_mat'] = Window.render_context['projection_mat']
            s.ask_update()
            self.time = self.time + self.dtime

    def on_fs(self, instance, value):
        shader = self.canvas.shader
        old_value = shader.fs
        try:
            shader.fs = value
        except:
            raise
        if not shader.success:
            shader.fs = old_value
        else:
            print('Compiled!')

    def reset_time(self):
        self.time = 0

def on_touch_move(touch):
    mouse_pos = touch.pos

class FekgaShaderEditorApp(App):
    store = FlatStore('fs_shader.json')
    fs = StringProperty()

    def on_start(self):
        if self.store.exists('shader'):
            self.fs = self.store.get('shader')['fragment']

    def on_stop(self):
        self.store.put('shader',fragment=self.fs)

    def show_cursor_info(self, cursor_row, cursor_col):
        self.ids.lineLabel.text = "line " + str(cursor_row+1)
        self.ids.colLabel.text = " column " + str(cursor_col+1)
        # print("line number: " + str(line_n_s))
        # print("touch: " + str(touch))

    def build(self):
        self.ids = self.root.ids
        self.root.on_touch_move = on_touch_move

    def toggle_fullscreen(self, toggle_value):
        self.root_window.borderless = toggle_value
        self.root_window.resizable = toggle_value
        self.root_window.fullscreen = [False,'auto'][toggle_value]

if __name__ == '__main__':
    FekgaShaderEditorApp(title='FekgaShaderEditor').run()
