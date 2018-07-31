import kivy
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
# from kivy.storage.jsonstore import JsonStore
from flatstore import FlatStore

fs_header = '''
#ifdef GL_ES
    precision highp float;
#endif
uniform vec2 resolution;
uniform float time;
'''

class ShaderEditor(BoxLayout):
    pass

class ShaderApp(App):
    store = FlatStore('fs_shader.json')
    shader_target = ObjectProperty()

    def __init__(self,*args,**kwargs):
        if 'shader_target' in kwargs:
            self.shader_target = kwargs['shader_target']
            del kwargs['shader_target']
        super(ShaderApp,self).__init__(*args,**kwargs)

    def on_start(self):
        if self.store.exists('shader'):
            self.root.fs = self.store.get('shader')['fragment']

    def on_stop(self):
        self.store.put('shader',fragment=self.root.fs)

    def build(self):
        self.root = ShaderEditor()
        self.root.fs = fs_header
