from kivy.app import App

from kivy.core.clipboard import Clipboard
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

MORSE_CODE = {'A':'. _', 'Á':'. _ _ . _', 'Ä':'. _ . _',
            'B':'_ . . .',
            'C':'_ . _ .',
            'D':'_ . .',
            'E':'.', 'É':'. . _ . .',
            'F':'. . _ .',
            'G':'_ _ .',
            'H':'. . . .', 
            'I':'. .',
            'J':'. _ _ _',
            'K':'_ . _', 
            'L':'. _ . .',
            'M':'_ _',
            'N':'_ .', 'Ñ':'_ _ . _ _',
            'O':'_ _ _', 'Ö':'_ _ _ .',
            'P':'. _ _ .',
            'Q':'_ _ . _', 
            'R':'. _ .',
            'S':'. . .',
            'T':'_', 
            'U':'. . _', 'Ü':'. . _ _',
            'V':'. . . _',
            'W':'. _ _', 
            'X':'_ . . _',
            'Y':'_ . _ _',
            'Z':'_ _ . .', 
            '1':'. _ _ _ _',
            '2':'. . _ _ _',
            '3':'. . . _ _', 
            '4':'. . . . _',
            '5':'. . . . .',
            '6':'_ . . . .', 
            '7':'_ _ . . .',
            '8':'_ _ _ . .',
            '9':'_ _ _ _ .', 
            '0':'_ _ _ _ _',
            ',':'_ _ . . _ _', '.':'. _ . _ . _', '\'':'. _ _ _ _ .', '"':'. _ . . _ .',
            '?':'. . _ _ . .',
            '-':'_ . . . . _', '_':'. . _ _ . _',
            '(':'_ . _ _ .', ')':'_ . _ _ . _',
            ':':'_ _ _ . . .', ';':'_ . _ . _ .', 
            '=':'_ . . . _', '/':'_ . . _ .', '+': '. _ . _ .', '*':'_ . . _',
            '@':'. _ _ . _ .',
            '\n':'\n'
            }

def get_key(my_dict, val): 
    for key, value in my_dict.items(): 
         if val == value: 
             return key 

def get_child(children, id):
    for child in children:
        if child.id == id:
            return child

class EnglishMorse(GridLayout, Screen):

    def __init__(self, **kwargs):
        super(EnglishMorse, self).__init__(**kwargs)
        self.rows = 3
        self.padding = 15
        self.spacing = 15

        l1 = Label(text='Enter Text')
        t1 = TextInput()
        t1.bind(text=self.convert)


        l2 = Label(text='Output')
        t2 = TextInput(id='out',
                       readonly=True,
                       cursor_color=[0,0,0,0],
                       background_normal='atlas://data/images/defaulttheme/textinput_active')

        b1 = Button(text='Convert From Code')
        b1.bind(on_press=self.transfer)

        b2 = Button(text='Click to Copy')
        b2.bind(on_press=self.my_copy)

        for w in [l1, t1, l2, t2, b1, b2]:
            self.add_widget(w)

    def convert(self, instance, value):
        output = []
        for c in value:
            try:
                if c == ' ':
                    output.append('    ')

                else:
                    output.append(MORSE_CODE[c.upper()]+'   ')

            except Exception:
                output = f'Error: nonexistent character present: "{c}"   '
                break

        get_child(self.children, 'out').text = ''.join(output)[:-3]

    def my_copy(self, *args):
         for child in self.children:
            if child.id == 'out':
                Clipboard.copy(child.text)

    def transfer(self, *args):
        sm.current = 'MorseEnglish'
        sm.transition.direction = 'left'

class MorseEnglish(GridLayout, Screen):

    def __init__(self, **kwargs):
        super(MorseEnglish, self).__init__(**kwargs)
        self.rows = 3
        self.padding = 15
        self.spacing = 15


        l1 = Label(text='Enter Code')
        t1 = TextInput()
        t1.bind(text=self.convert)

        l2 = Label(text='Output')
        t2 = TextInput(id='out',
                       readonly=True,
                       cursor_color=[0,0,0,0],
                       background_normal='atlas://data/images/defaulttheme/textinput_active')

        b1 = Button(text='Convert From Text')
        b1.bind(on_press=self.transfer)

        b2 = Button(text='Click to Copy')
        b2.bind(on_press=self.my_copy)

        for w in [l1, t1, l2, t2, b1, b2]:
            self.add_widget(w)

    def convert(self, instance, value):
        output = []
        for w in value.split('       '):
            word = []
            for c in w.split('   '):
                if not c:
                    get_child(self.children, 'out').text = ''
                
                elif c in MORSE_CODE.values():
                    word.append(get_key(MORSE_CODE, c))

                else:
                    get_child(self.children, 'out').text = f'Error: nonexistent character present: "{c}"'
                    return

            output.append(''.join(word))

        get_child(self.children, 'out').text = ' '.join(output)

    def my_copy(self, *args):
         for child in self.children:
            if child.id == 'out':
                Clipboard.copy(child.text)

    def transfer(self, *args):
        sm.current = 'EnglishMorse'
        sm.transition.direction = 'right'

sm = ScreenManager()
sm.add_widget(EnglishMorse(name='EnglishMorse'))
sm.add_widget(MorseEnglish(name='MorseEnglish'))

class ConverterApp(App):
    def build(self):
        return sm

ConverterApp().run()