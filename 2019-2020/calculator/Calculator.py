from kivy.app import App

# Builder allows me to code everything in one file
from kivy.lang import Builder

# The main layout that I will use for my code. I can use other layouts withing a layout.
from kivy.uix.gridlayout import GridLayout

# A custom label with a white background color
import LabelB

# Square root method
from math import sqrt

# Visual code, but there is some logic in this
Builder.load_string("""

<CButton@Button>:
    font_size: 32

<CalcGridLayout>:
    rows: 7
    padding: 10
    spacing: 10

    LabelB:
        id: entry
        bcolor: [1, 1, 1, 1]
        color: [0, 0, 0, 1]
        font_size: 32

    BoxLayout:
        spacing:10
        CButton:
            text: '%'
            on_release: root.new_calculation(entry, self.text)

        CButton:
            text: 'sqrt('
            on_release: root.new_calculation(entry, self.text)

        CButton:
            text: ')'
            on_release: root.new_calculation(entry, self.text)

        CButton:
            text: '^2'
            on_release: root.new_calculation(entry, self.text)

    BoxLayout:
        spacing: 10

        CButton:
            text: "x^y"
            on_release: root.new_calculation(entry, self.text)

        CButton:
            text: "10^x"
            on_release: root.new_calculation(entry, self.text)

        CButton:
            text: 'DEL'
            on_release: root.delete(entry)
        CButton:
            text: '+'
            on_release: root.new_calculation(entry, self.text)

    BoxLayout:
        spacing: 10
        CButton:
            text: '7'
            on_release: root.typing(entry, '7')

        CButton:
            text: '8'
            on_release: root.typing(entry, '8')

        CButton:
            text: '9'
            on_release: root.typing(entry, '9')

        CButton:
            text: '-'
            on_release: root.new_calculation(entry, self.text)

    BoxLayout:
        spacing: 10
        CButton:
            text: '4'
            on_release: root.typing(entry, '4')

        CButton:
            text: '5'
            on_release: root.typing(entry, '5')

        CButton:
            text: '6'
            on_release: root.typing(entry, '6')

        CButton:
            text: '*'
            on_release: root.new_calculation(entry, self.text)

    BoxLayout:
        spacing: 10
        CButton:
            text: '1'
            on_release: root.typing(entry, '1')

        CButton:
            text: '2'
            on_release: root.typing(entry, '2')

        CButton:
            text: '3'
            on_release: root.typing(entry, '3')

        CButton:
            text: '/'
            on_release: root.new_calculation(entry, self.text)

    BoxLayout:
        spacing: 10
        CButton:
            text: 'AC'
            on_release: entry.text = ''

        CButton:
            text: '0'
            on_release: root.typing(entry, '0')

        CButton:
            text: '.'
            on_release: entry.text += self.text

        CButton:
            text: '='
            on_release: root.calculate(entry)

""")

##########
#####
# typing()
# calculate()
# new_calculation()
# delete()
#####
#########
class CalcGridLayout(GridLayout):

    ######
    # Whenever you press a digit only
    # entry = TextInput()
    # text = CButton.text or the way that python understands a certain operation
    #####
    def typing(self, entry, text):
        # If you have made a calculation or an error, a new digit will clear the old calculation or error
        if '=' in entry.text or entry.text == 'Error':
            entry.text = text

        # If you have not made a calculation or error, add the digit to entry
        else:
            entry.text += text

    #####
    # Whenever you press the "=" button
    # entry = TextInput()
    #####
    def calculate(self, entry):
        # If you have typed any digit
        if entry.text:
            # If python converts your result to scientific notation, make so that it has 20 digits of precision
            try:
                if 'e' in str(eval(entry.text)):
                    entry.text += ' = ' + str('{:.20f}'.format(eval(entry.text)))

                # If your result is not in scientific notation, do not change the precision
                else:
                    entry.text += ' = ' + str((eval(entry.text)))

            # If there is an error in eval(), simply display error
            except Exception:
                entry.text = "Error"

    #####
    # Whenever a operation button is pressed
    # entry = TextInput()
    # operation = CButton.text
    #####
    def new_calculation(self, entry, operation):
        # If there is nothing in entry you cannot input a operation
        if entry.text and entry.text != 'Error':
            # If there is something in entry and it is not an error, get the last part of entry.text which is the result
            result = entry.text.split()[-1]

            # If you have not made a calculation, simply add the operation unless specified something else
            if '=' not in entry.text:
                # Operations that cannot simply add their actual text
                if operation == 'x^y':
                    entry.text += '**'

                elif operation == '^2':
                    entry.text += '**2'
                    self.calculate(entry)

                # Generic operations
                else:
                    entry.text += operation

            # If you have made a calculation and you press any operation, the result will be displayed with the operation
            else:
                # Custom outputs for operations that cannot simply add their actual text
                if operation == 'sqrt(':
                    # When pressing "sqrt(", you do not have to press the "=" button
                    entry.text = operation + result + ')'
                    # self is CalcGridLayout
                    self.calculate(entry)

                elif operation == 'x^y':
                    entry.text = result + '**'

                # When pressing "^2", you do not have to press the "=" button
                elif operation == '^2':
                    entry.text = result + '**2'
                    # self is CalcGridLayout
                    self.calculate(entry)

                # When pressing "10^x", you do not have to press the "=" button
                elif operation == '10^x':
                    entry.text = '10**' + result
                    # self is CalcGridLayout
                    self.calculate(entry)

                # Generic operations
                else:
                    entry.text = result + operation

        # Becuase the square root operation requires that the number must be inside paranthesis, you can use it even if there is nothing in entry
        else:
            if operation == 'sqrt(':
                entry.text += operation

    #####
    # Whenver you press the "DEL" button
    # entry = TextInput()
    #####
    def delete(self, entry):
        # If you press "DEL" while an error occured, "DEL" deletes everything
        if "Error" in entry.text:
            entry.text = ''

        # If an errro did not occur, "DEL" only deletes the last input
        elif entry.text:
            entry.text = entry.text[:-1]

class CalculatorApp(App):
    def build(self):
        return CalcGridLayout()

CalculatorApp().run()
