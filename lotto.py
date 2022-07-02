# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 20:18:29 2022
the program simulates the lotto drawing. The assumptions are:
- the draw takes place three times a week
- the cost of the draw is PLN 3
- the user plays until he wins
- the user specifies the period in which he intends to play

the program returns the result of playing the lottery
@author: krykl
"""
from random import sample, uniform
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown

Builder.load_file('kivy.kv')
Window.size = (600, 600)

class FirstScreen(BoxLayout):
    """class"""

    avalable_numbers = ['{:02d}'.format(x) for x in range(1, 50)]
    user_numbers = set()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.age = 0
        self.age_end = 0
        self.amount_draw = 0
        self.result_3 = 0
        self.result_4 = 0
        self.result_5 = 0
        self.won_3 = 0
        self.won_4 = 0
        self.won_5 = 0
        self.won_6 = 1000000 * uniform(2.0, 24.0)
        self.result_6 = 1
        self.draw = set()
        self.age = 18
        self.age_end = 1
        self.user_numbers = set()
        self.szufladka = ''


        def show_selected_value(_, text):
            """
            This function add avalable and remove unavalable
            elements for list self.avalable_numbers and update
            the self.user_numbers

            Parameters
            ----------
            spinner : object.
            text : str.

            Returns
            -------
            Updates self.avalable_numbers for user.

            """

            self.avalable_numbers.remove(text)
            self.avalable_numbers.append(self.szufladka)

            self.user_numbers.add(text)
            self.user_numbers.remove(self.szufladka)


        def add_remove_number(spinner):
            """
            This function refresh self.spiner.values avalable
            dor user to choose. Return actual text spinner.

            Parameters
            ----------
            spinner : object.

            Returns
            -------
            Updates self.spiner.values for user, and return
            self.szufladka = actual text spinner

            """

            self.avalable_numbers.sort()
            spinner.values = self.avalable_numbers
            self.szufladka = (str(spinner.text))

        numb = sample(self.avalable_numbers, k=6)

        for i in numb:
            self.avalable_numbers.remove(i)
            self.user_numbers.add(i)

        for index in numb:

            spinner = SpinnerWidget(text=index, values=self.avalable_numbers,
                size_hint=(None, None), font_size = 25,
                color = (0,0,0,1), bold = True,
                background_normal = './ball.png',
                background_down = './ball.png',
                pos_hint={'center_x': .5, 'center_y': .5})
            spinner.bind(text=show_selected_value, on_press=add_remove_number)
            self.ids.user_numbers.add_widget(spinner)


    def age_set(self):
        """pass"""


    def age_end_set(self):
        """pass"""


    def check_your_result(self):
        """
        checks how many and what kind of winnings
        the user has obtained. It passes the result
        to a popup window

        Returns
        -------
        Popup.

        """

        self.age = 0
        self.age_end = 0
        self.amount_draw = 0
        self.result_3 = 0
        self.result_4 = 0
        self.result_5 = 0
        self.won_3 = 0
        self.won_4 = 0
        self.won_5 = 0
        self.won_6 = 1000000 * uniform(2.0, 24.0)
        self.result_6 = 1
        self.draw = set(sample(range(1,50), k=6))
        self.age = self.ids.slider_age.value
        self.age_end = self.ids.slider_duration.value
        self.user_numbers = {int(x) for x in self.user_numbers}

        while self.user_numbers != self.draw:
            self.amount_draw += 1
            result = self.user_numbers & self.draw
            if len(result) == 3:
                self.result_3 += 1
                self.won_3 += 24
            elif len(result) == 4:
                self.result_4 += 1
                self.won_4 += 10 * uniform(5.0, 30.0)
            elif len(result) == 5:
                self.result_5 += 1
                self.won_5 += 1000 * uniform(1.5, 11.0)
            self.draw = set(sample(range(1,50), k=6))
            if self.amount_draw/3//52 + self.age >= self.age + self.age_end:
                self.draw = self.user_numbers
                self.won_6 = 0
                self.result_6 = 0



        if self.result_6 == 1:

            pops = MyPopup()
            pops.tekst_uwaga((f'''
You win after {self.amount_draw} draws!
Your age is: {self.age + self.amount_draw/3//52} Years!
You was played over {self.amount_draw/3//52} Years and {self.amount_draw/3%52} Weeks!
You was played {self.amount_draw} Times!

You won:
    - {self.result_6} times six:      {self.won_6:.2f} PLN
    - {self.result_5} times five:     {self.won_5:.2f} PLN
    - {self.result_4} times four:     {self.won_4:.2f} PLN
    - {self.result_3} times tree:     {self.won_3:.2f} PLN

    TOTAL:     {(self.won_6+self.won_5+self.won_4+self.won_3):.2f} PLN

You paid for this: {(self.amount_draw*3):.2f} PLN
You are won/lost: {(self.won_6+self.won_5+self.won_4+self.won_3 - self.amount_draw*3):.2f} PLN'''))
            pops.open()
            self.user_numbers = {str('{:02d}'.format(x)) for x in self.user_numbers}

        else:

            pops = MyPopup()
            pops.tekst_uwaga((f'''
You don't have won!
Your age is: {self.age + self.amount_draw/3//52} Years!
You was played over {self.amount_draw/3//52} Years and {self.amount_draw/3%52} Weeks!
You was played {self.amount_draw} Times!

You won:
    - {self.result_6} times six:      {self.won_6:.2f} PLN
    - {self.result_5} times five:     {self.won_5:.2f} PLN
    - {self.result_4} times four:     {self.won_4:.2f} PLN
    - {self.result_3} times tree:     {self.won_3:.2f} PLN

    TOTAL:     {(self.won_6+self.won_5+self.won_4+self.won_3):.2f} PLN

You paid for this: {(self.amount_draw*3):.2f} PLN
You are won/lost: {(self.won_6+self.won_5+self.won_4+self.won_3 - self.amount_draw*3):.2f} PLN
         '''))
            pops.open()
            self.user_numbers = {str('{:02d}'.format(x)) for x in self.user_numbers}


class SpinnerOptions(SpinnerOption):
    """class"""


class SpinnerDropdown(DropDown):
    """clas"""


class SpinnerWidget(Spinner):
    """class"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dropdown_cls = SpinnerDropdown
        self.option_cls = SpinnerOptions


class MyPopup(Popup):
    """class"""

    def tekst_uwaga(self, tekst):
        """
        pass text to the popup window.

        Parameters
        ----------
        tekst : string.

        Returns
        -------
        Change text in popup.

        """
        self.ids.uwaga.text = tekst


class Start(App):
    """Start App"""

    def build(self):
        """
        Build the App

        Returns
        -------
        FirstScreen : BoxLayout.

        """
        return FirstScreen()

if __name__ == '__main__':
    Start().run()
