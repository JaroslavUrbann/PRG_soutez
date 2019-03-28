from kivy.app import App
from kivy.core.image import Image as CoreImage
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from PIL import Image
from io import BytesIO
import numpy as np
import os


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class My2App(App):
    save_path = "/"
    load_path = "/"
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def build(self):
        # img = Image.new("RGB", (100, 100))
        img = np.zeros((100, 100, 3))
        img = Image.fromarray(img, mode="RGB")
        self.change_img(img.convert("RGB"))

    def change_img(self, img):
        img_io = BytesIO()
        img.save(img_io, format="jpeg")
        img_io.seek(0)
        self.root.ids.grayscale_img.texture = CoreImage(img_io, ext='jpg').texture

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()

        self.dismiss_popup()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)

        self.dismiss_popup()


if __name__ == '__main__':
    My2App().run()
