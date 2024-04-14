from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
import os.path
import json
import sys


class MyWidget(BoxLayout):
    if not os.path.exists('formatos.json'):
        with open('formatos.json', 'w', encoding='UTF-8') as f:
            f.write("""[{
  "Titulo": "Formato Clásico",
  "Data": {
    "Duración de Película": 120,
    "Etapas": {
        "Incidente inicial": 3,
        "Pregunta activa": 10,
        "Pinza 3": 15,
        "Plotpoint 1": 30,
        "Pinza 1": 45,
        "Punto medio": 60,
        "Pinza 2": 75,
        "Plotpoint 2": 90,
        "Climax": "105, 110",
        "Final": 115,
        "Créditos": 120
    }
  }
}]""")

    try:
        with open('formatos.json', encoding='UTF-8') as f:
            atributos = json.loads(f.read())
        formato = atributos[0]['Titulo']
    except:
        print('\n\nARCHIVO formatos.json INEXISTENTE O CON PROBLEMA DE FORMATO\n')
        sys.exit()

    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.box = BoxLayout()
        self.box.size_hint_y = 0.1
        values = []
        for atributo in self.atributos:
            values.append(atributo['Titulo'])
        self.spinner = Spinner(text=self.formato, values=values)
        self.box.add_widget(self.spinner)
        self.spinner.bind(text=self.on_formato_cambiado)
        self.txt_min = TextInput(text='120', halign='center', multiline=False)
        self.txt_min.bind(text=self.on_press, focus=self.focus)
        self.box.add_widget(self.txt_min)
        self.add_widget(self.box)
        self.form = BoxLayout()
        self.add_widget(self.form)
        self.calcular()
        self.focus(self.txt_min)

    def focus(self, instance, focus=False):
        if not focus:
            self.txt_min.focus = True

    def validar(self, valor):
        if self.txt_min.text != '':
            try:
                t = int(valor)/1
            except:
                self.txt_min.text = '1'
            return True
        else:
            return False

    def on_press(self, instance, valor):
        if self.validar(valor):
            self.calcular()
        else:
            self.form.clear_widgets()

    def calcular(self, instance=None):
        if not self.validar(self.txt_min.text):
            return -1

        self.form.clear_widgets()

        etapas = self.calcular_lista_actualizada(int(self.txt_min.text))

        box = BoxLayout(orientation='vertical')
        for nombre, valor in etapas.items():
            box2 = BoxLayout()
            box2.add_widget(Label(text=nombre))
            box2.add_widget(Label(text=valor))
            box.add_widget(box2)
        self.form.add_widget(box)

    def on_formato_cambiado(self, formato=formato, *args):
        if args:
            formato = args[0]
        self.formato = formato
        self.calcular()

    def calcular_lista_actualizada(self, duracion_pelicula) -> dict:
        indice = -1
        for i in range(len(self.atributos)):
            if self.formato == self.atributos[i]['Titulo']:
                indice = i
                break
        actualizado = {}
        for nombre, duracion_relativa in self.atributos[indice]['Data']["Etapas"].items():
            if isinstance(duracion_relativa, (int, float)):
                actualizado[nombre] = str(round((duracion_pelicula * duracion_relativa /
                                                 self.atributos[indice]['Data']['Duración de Película']), 1))
            else:
                duracion_relativa = list(str(duracion_relativa).split(sep=','))
                for z in range(len(duracion_relativa)):
                    duracion_relativa[z] = int(duracion_relativa[z].strip())
                actualizado[nombre] = str(round((duracion_pelicula * duracion_relativa[0] /
                                                 self.atributos[indice]['Data']['Duración de Película']), 1)) + ' / ' + str(
                    round((duracion_pelicula * duracion_relativa[1] /
                           self.atributos[indice]['Data']['Duración de Película']), 1))
        return actualizado


class Pelis(App):
    def build(self):
        self.title = 'Pelis Calculator'
        return MyWidget()


if __name__ == '__main__':
    Pelis().run()
