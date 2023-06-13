import os, sys
from random import choice
from kivy.resources import resource_add_path, resource_find

from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen

class Pop(Popup):
    def __init__(self, widgets, **kwargs):
        super(Pop, self).__init__(**kwargs)
        self.widgets = {}
        
        for id, widget in widgets:
            self.register_widget(id, widget)

    def register_widget(self, id, widget):
        self.widgets[id] = widget
        self.content.add_widget(widget)

class Welcome(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(Welcome, self).__init__(**kwargs)
        self.widgets = {}

        self.add_widget(Label(text='Welcome',
                              font_size='18',
                              pos_hint={'center_x': 0.5, 'top': 1.25}))

        self.register_widget('spinner', Spinner(text='Select Mode',
                             values=('Multiplayer', 'Singleplayer'),
                             size_hint=(0.2, 0.1),
                             pos_hint={'center_x': 0.30, 'top': 0.66}))
        self.widgets['spinner'].bind(text=self.update_mode)

        self.register_widget('player_1', TextInput(hint_text='Player 1 Name',
                             multiline=False,
                             size_hint=(0.2, 0.1),
                             pos_hint={'center_x': 0.7, 'top': 0.66}))
        self.widgets['player_1'].bind(text=self.update_name)

        self.register_widget('player_2', TextInput(hint_text='Player 2 Name',
                             multiline=False,
                             size_hint=(0.2, 0.1),
                             pos_hint={'center_x': 0.7, 'top': 0.46}))
        self.widgets['player_2'].bind(text=self.update_name)

        self.register_widget('play', Button(text='Play',
                              on_release=self.update_screen,
                              size_hint=(0.2, 0.1),
                              pos_hint={'center_x': 0.5, 'top': 0.2}))

        self.warning = Popup(title='Warning',
                             content=Label(),
                             size_hint=(0.33, 0.33))

    def register_widget(self, id, widget):
        self.add_widget(widget)
        self.widgets[id] = widget

    def update_mode(self, instance, value):
        if value == 'Singleplayer':
            self.widgets['player_2'].readonly = True
            self.widgets['player_2'].background_active = self.widgets['player_2'].background_normal
            self.widgets['player_2'].text = 'Computer'
            self.widgets['player_2'].cursor_color = [0, 0, 0, 0]

        elif value == 'Multiplayer':
            self.widgets['player_2'].readonly = False
            self.widgets['player_2'].background_active = self.widgets['player_1'].background_active
            self.widgets['player_2'].text = ''
            self.widgets['player_2'].cursor_color = [1, 0, 0, 1]

    def update_name(self, instance, value):
        if self.widgets['player_1'] == instance:
            game.widgets['turn'].text = f'Turn: {value}'
            game.widgets['player_1_name'].text = value

        elif self.widgets['player_2'] == instance:
            game.widgets['player_2_name'].text = value

    def update_screen(self, instance):
        if self.widgets['spinner'].text == 'Select Mode':
            self.warning.content.text = 'Please select a mode'
            self.warning.open()

        elif not self.widgets['player_1'].text:
            self.warning.content.text = 'Please enter a name for player 1'
            self.warning.open()

        elif not self.widgets['player_2'].text:
            self.warning.content.text = 'Please enter a name for player 2\nOr select singleplayer mode'
            self.warning.open()
        
        elif self.widgets['player_2'].text == self.widgets['player_1'].text:
            self.warning.content.text = 'Please select different names for each player'
            self.warning.open()

        elif self.widgets['spinner'].text == 'Multiplayer' and self.widgets['player_2'].text == 'Computer':
            self.warning.content.text = 'That is not a valid name for Player 2'
            self.warning.open()

        else:
            sm.current = 'game'
            game.board.tiles[(1, 1)].validate()
            game.board.tiles[(1, 1)].highlight()

class Game(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.widgets = {}

        self.board = Board(rows=8, cols=8,
                     size_hint=(Window.size[1]/Window.size[0]*0.8, 0.8),
                     pos_hint={'center_x': 0.43, 'center_y': 0.5})
        self.add_widget(self.board)

        self.register_widget('player_1_name', Label(pos_hint={'center_x': 0.43, 'center_y': 0.05}))
        self.register_widget('player_2_name', Label(pos_hint={'center_x': 0.43, 'center_y': 0.95}))

        self.register_widget('red_capture_count', Button(text='0',
                             pos_hint={'center_x': 0.65, 'center_y': 0.57},
                             size_hint=(Window.size[1]/Window.size[0]*0.1, 0.1),
                             background_normal='assets/red_piece_no_background.png',
                             background_down='assets/red_piece_no_background.png',
                             color=(0, 0, 0, 1)))

        self.register_widget('white_capture_count', Button(text='0',
                             pos_hint={'center_x': 0.65, 'center_y': 0.42},
                             size_hint=(Window.size[1]/Window.size[0]*0.1, 0.1),
                             background_normal='assets/white_piece_no_background.png',
                             background_down='assets/white_piece_no_background.png',
                             color=(0, 0, 0, 1)))

        self.register_widget('turn', Label(text=f'Turn: {welcome.widgets["player_1"].text}',
                             pos_hint={'center_x': 0.65, 'center_y': 0.25}))

        self.won = Pop([('label', Label(text='CONGRATULATIONS YOU WON',
                                        pos_hint={'center_x': 0.5, 'center_y': 0.85})),
                        ('quit', Button(text='Quit to Desktop',
                                        on_release=self.terminate,
                                        size_hint=(0.33, 0.33),
                                        pos_hint={'right': .66, 'top': 0.33}))],
                       title='CONGRATULATIONS',
                       content=FloatLayout(),
                       size_hint=(0.33, 0.33),
                       auto_dismiss=False)

        self.recap_pop = Pop([('label', Label(text='WOULD YOU LIKE TO CAPTURE ANOTHER PIECE?',
                                        pos_hint={'center_x': 0.5, 'center_y': 0.85})),
                        ('yes', Button(text='Yes',
                                         on_release=self.board.tiles[(1, 1)].recap,
                                         size_hint=(0.33, 0.33),
                                         pos_hint={'right': 0.33, 'top': 0.33})),
                        ('no', Button(text='No',
                                        on_release=self.board.tiles[(1, 1)].no_recap,
                                        size_hint=(0.33, 0.33),
                                        pos_hint={'right': 1, 'top': 0.33}))],
                       title='NICE MOVE',
                       content=FloatLayout(),
                       size_hint=(0.33, 0.33),
                       auto_dismiss=False)

    def register_widget(self, id, widget):
        self.add_widget(widget)
        self.widgets[id] = widget

    def update_turn(self):
        if self.board.red_turn:
            self.widgets['turn'].text = f'Turn: {welcome.widgets["player_1"].text}'

        elif not game.board.red_turn:
            self.widgets['turn'].text = f'Turn: {welcome.widgets["player_2"].text}'

    def update_count(self, team_captured):
        if team_captured == 'red':
            self.widgets['red_capture_count'].text = str(int(self.widgets['red_capture_count'].text) + 1)

        elif team_captured == 'white':
            self.widgets['white_capture_count'].text = str(int(self.widgets['white_capture_count'].text) + 1)

    def reset_board(self, instance):
        pass

    def update_screen(self, instance):
        pass

    def terminate(self, instance):
        App.get_running_app().stop()

class Board(GridLayout):
    red_turn = True

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.tiles = {}
        self.add_tiles()

    def add_tiles(self):
        for i in range(self.rows, 0, -1):
            for j in range(1, self.cols+1):
                if (i + j)%2 == 0:
                    if i <= 3:
                        occupied = True
                        team = 'red'
                        background = 'assets/red_piece.png'
                        background_d = 'assets/red_piece_down.png'

                    elif i >= 6:
                        occupied = True
                        team = 'white'
                        background = 'assets/white_piece.png'
                        background_d = 'assets/white_piece_down.png'

                    else:
                        occupied = False
                        team = None
                        background = 'assets/black.png'
                        background_d = 'assets/black.png'

                else:
                    occupied = False
                    team = None
                    background = 'assets/white.png'
                    background_d = 'assets/white.png'

                tile = Checker((i, j),
                               occupied,
                               team,
                               background_normal=background,
                               background_down=background_d)

                self.tiles[(i, j)] = tile
                self.add_widget(tile)

    def clear_board(self, c_tile):
        for tile in self.tiles.values():
            if tile.background_normal == 'assets/ghost_piece.png':
                tile.background_normal = 'assets/black.png'
                tile.background_down = 'assets/black.png'

            # if the current tile is not occuppied I want to clear all tiles that are highlighted
            if not c_tile.team and 'high' in tile.background_normal:
                if tile.team == 'red':
                    if tile.king:
                        tile.background_normal = 'assets/red_king.png'
                        tile.background_down = 'assets/red_king_down.png'

                    elif not tile.king:
                        tile.background_normal = 'assets/red_piece.png'
                        tile.background_down = 'assets/red_piece_down.png'

                elif tile.team == 'white':
                    if tile.king:
                        tile.background_normal = 'assets/white_king.png'
                        tile.background_down = 'assets/white_king_down.png'

                    elif not tile.king:
                        tile.background_normal = 'assets/white_piece.png'
                        tile.background_down = 'assets/white_piece_down.png'

class Checker(Button):
    last_press = None
    moving_tiles = []
    capturing_tiles = []

    # 0:2 for red pieces
    # 2:4 for black pieces
    # 0:4 for kings
    to_check = [(1, -1), (1, 1), (-1, -1), (-1, 1)]

    def __init__(self, position, occupied, team, **kwargs):
        super(Checker, self).__init__(**kwargs)
        self.position = position
        self.on_release = self.action
        self.occupied = occupied
        self.king = False
        self.can_move = []
        self.can_capture = []
        self.to_check = []
        self.team = team

    def update_moves(self, tile):
        # checking over the given coord differences of the tiles that should be checked
        for dif_x, dif_y in tile.to_check:
            # can cause KeyError
            try:
                # checking tiles directly to the left or right if are available to move to
                if not game.board.tiles[tile.position[0] + dif_x, tile.position[1] + dif_y].occupied:
                    tile.can_move.append((tile.position[0] + dif_x, tile.position[1] + dif_y))

                # if the tile directly to the left or right is ocuppied, check if the one to the left or right after it
                # if it isnot ocuppied, that means this tile can capture
                elif not game.board.tiles[tile.position[0] + dif_x*2, tile.position[1] + dif_y*2].occupied:
                    # if the tile directly to the left or to the right is not the same team
                    if game.board.tiles[tile.position[0] + dif_x, tile.position[1] + dif_y].team != tile.team:
                        tile.can_capture.append((tile.position[0] + dif_x*2, tile.position[1] + dif_y*2))

            except:
                pass

    def highlight(self):
        highlighted = False
        # if there are checkers that can capture
        for tile in Checker.capturing_tiles:
            # if a checker is highlighted skip to next iteration
            # and set highlighted to True
            if tile.team == 'red' and game.board.red_turn:
                if tile.king:
                    tile.background_normal = 'assets/red_king_high.png'
                    tile.background_down = 'assets/red_king_high_down.png'

                elif not tile.king:          
                    tile.background_normal = 'assets/red_piece_high.png'
                    tile.background_down = 'assets/red_piece_high_down.png'

                highlighted = True
                continue

            elif tile.team == 'white' and not game.board.red_turn and welcome.widgets['player_2'].text != 'Computer':
                if tile.king:
                    tile.background_normal = 'assets/white_king_high.png'
                    tile.background_down = 'assets/white_king_high_down.png'

                elif not tile.king:          
                    tile.background_normal = 'assets/white_piece_high.png'
                    tile.background_down = 'assets/white_piece_high_down.png'

                highlighted = True
                continue

        # if anything was highlighted above, do not highlight moving tiles
        if highlighted:
            return

        for tile in Checker.moving_tiles:
            if tile.team == 'red' and game.board.red_turn:
                if tile.king:
                    tile.background_normal = 'assets/red_king_high.png'
                    tile.background_down = 'assets/red_king_high_down.png'

                elif not tile.king:          
                    tile.background_normal = 'assets/red_piece_high.png'
                    tile.background_down = 'assets/red_piece_high_down.png'

            elif tile.team == 'white' and not game.board.red_turn and welcome.widgets['player_2'].text != 'Computer':
                if tile.king:
                    tile.background_normal = 'assets/white_king_high.png'
                    tile.background_down = 'assets/white_king_high_down.png'

                elif not tile.king:          
                    tile.background_normal = 'assets/white_piece_high.png'
                    tile.background_down = 'assets/white_piece_high_down.png'

    # loops over every tile and checks which pieces it can move to and capture
    def validate(self):
        red_lost = True
        white_lost = True
        # clearing the list of tiles that can move
        Checker.moving_tiles.clear()
        Checker.capturing_tiles.clear()
        # determining where the tile can move and capture
        for tile in game.board.tiles.values():
            tile.can_move.clear()
            tile.can_capture.clear()
            if tile.occupied:
                # checking if tile can be king and if it is not a king
                if tile.team == 'red' and tile.position[0] == 8 and not tile.king:
                    tile.king = True
                    tile.background_normal = 'assets/red_king.png'
                    tile.background_down = 'assets/red_king_down.png'

                elif tile.team == 'white' and tile.position[0] == 1 and not tile.king:
                    tile.king = True
                    tile.background_normal = 'assets/white_king.png'
                    tile.background_down = 'assets/white_king_down.png'

                if tile.king:
                    if tile.team == 'red':
                        red_lost = False

                    elif tile.team == 'white':
                        white_lost = False

                    tile.to_check = [(1, -1), (1, 1), (-1, -1), (-1, 1)]
                    tile.update_moves(tile)

                elif not tile.king:
                    if tile.team == 'red':
                        red_lost = False
                        tile.to_check = [(1, -1), (1, 1)]
                        tile.update_moves(tile)

                    elif tile.team == 'white':
                        white_lost = False
                        tile.to_check = [(-1, -1), (-1, 1)]
                        tile.update_moves(tile)

            if tile.can_move:
                Checker.moving_tiles.append(tile)

            if tile.can_capture:
                Checker.capturing_tiles.append(tile)

        if not Checker.moving_tiles + Checker.capturing_tiles:
            if int(game.widgets['red_capture_count'].text) > int(game.widgets['white_capture_count'].text):
                red_lost = True

            elif int(game.widgets['red_capture_count'].text) < int(game.widgets['white_capture_count'].text):
                white_lost = True

            else:
                game.won.widgets['label'].text = f"THE GAME ENDED IN A TIE!"
                game.won.open()

        else:
            if red_lost:
                if welcome.widgets['player_2'].text == 'Computer':
                    game.won.widgets['label'].text = f"ARE YOU SERIOUS!? YOU LOST TO A MACHINE THAT RANDOMLY PICKS MOVES"
                    
                else:
                    game.won.widgets['label'].text = f"CONGRATULATIONS, YOU WON {welcome.widgets['player_2'].text}!"
                game.won.open()

            elif white_lost:
                game.won.widgets['label'].text = f"CONGRATULATIONS, YOU WON {welcome.widgets['player_1'].text}!"
                game.won.open()


    def move(self, origin):
        # check if this was a capture move
        if origin.can_capture:
            # captured piece
            captured = game.board.tiles[((self.position[0]+origin.position[0])//2,
                                         (self.position[1]+origin.position[1])//2)]

            game.update_count(captured.team)
            captured.background_normal = 'assets/black.png'
            captured.background_down = 'assets/black.png'
            captured.team = None
            captured.occupied = False
            captured.king = False
            capped = True

        elif not origin.can_capture:
            capped = False

        # setting up the destination
        if origin.team == 'red':
            if origin.king:
                self.king = True
                self.background_normal = 'assets/red_king.png'
                self.background_down = 'assets/red_king_down.png'

            elif not origin.king:
                self.background_normal = 'assets/red_piece.png'
                self.background_down = 'assets/red_piece_down.png'
            
            self.team = 'red'

        elif origin.team == 'white':
            if origin.king:
                self.king = True
                self.background_normal = 'assets/white_king.png'
                self.background_down = 'assets/white_king_down.png'

            elif not origin.king:
                self.background_normal = 'assets/white_piece.png'
                self.background_down = 'assets/white_piece_down.png'

            self.team = 'white'

        self.occupied = True


        # setting up origin
        origin.background_normal = 'assets/black.png'
        origin.background_down = 'assets/black.png'
        origin.occupied = False
        origin.team = None
        origin.king = False
        origin.to_check.clear()

        game.board.red_turn = False if game.board.red_turn else True
        game.update_turn()

        return capped

    # validates pieces
    # highlights possible moves
    # moves the piece
    def action(self):
        if self.occupied:
            game.board.clear_board(self)
            made_ghost = False
            # highlights possible moves
            if 'red' in self.background_normal and 'high' in self.background_normal and game.board.red_turn:
                if Checker.capturing_tiles:
                    for piece in self.can_capture:
                        made_ghost = True
                        game.board.tiles[piece].background_normal = 'assets/ghost_piece.png'
                        game.board.tiles[piece].background_down = 'assets/ghost_piece.png'

                if not made_ghost:
                    if Checker.moving_tiles:
                        for piece in self.can_move:
                            game.board.tiles[piece].background_normal = 'assets/ghost_piece.png'
                            game.board.tiles[piece].background_down = 'assets/ghost_piece.png'

            elif 'white' in self.background_normal and 'high' in self.background_normal and not game.board.red_turn:
                if Checker.capturing_tiles:
                    for piece in self.can_capture:
                        made_ghost = True
                        game.board.tiles[piece].background_normal = 'assets/ghost_piece.png'
                        game.board.tiles[piece].background_down = 'assets/ghost_piece.png'

                if not made_ghost:
                    if Checker.moving_tiles:
                        for piece in self.can_move:
                            game.board.tiles[piece].background_normal = 'assets/ghost_piece.png'
                            game.board.tiles[piece].background_down = 'assets/ghost_piece.png' 

            Checker.last_press = self

        # moves the piece
        elif self.background_normal == 'assets/ghost_piece.png':
            game.board.clear_board(self)
            capped = self.move(Checker.last_press)
            self.validate()

            if capped:
                can_recap = False
                if self in Checker.capturing_tiles:
                    can_recap = True
                    game.board.red_turn = False if game.board.red_turn else True
                    game.recap_pop.open()

                if not can_recap:
                    self.highlight()

            elif not capped:
                self.highlight()

        if welcome.widgets['player_2'].text == 'Computer' and not game.board.red_turn:
            comp_capture = []
            comp_move = []
            if Checker.capturing_tiles:
                for tile in Checker.capturing_tiles:
                    if tile.team == 'white':
                        comp_capture.append(tile)

            if not comp_capture:
                if Checker.moving_tiles:
                    for tile in Checker.moving_tiles:
                        if tile.team == 'white':
                            comp_move.append(tile)

            if comp_capture:
                game.board.clear_board(self)
                chosen = choice(comp_capture)
                destination = game.board.tiles[choice(chosen.can_capture)]
                capped = destination.move(chosen)
                self.validate()
                if capped:
                    can_recap = False
                    if destination in Checker.capturing_tiles:
                        can_recap = True
                        game.board.red_turn = False if game.board.red_turn else True
                        self.recap(None)
                        destination.action()

                    if not can_recap:
                        self.highlight()
                
                elif not capped:
                    self.highlight()

            elif comp_move:
                game.board.clear_board(self)
                chosen = choice(comp_move)
                game.board.tiles[choice(chosen.can_move)].move(chosen)
                self.validate()
                self.highlight()

    def recap(self, instance):
        game.recap_pop.dismiss()
        self.highlight()

    def no_recap(self, instance):
        game.board.red_turn = False if game.board.red_turn else True
        game.recap_pop.dismiss()
        self.highlight()

        if welcome.widgets['player_2'].text == 'Computer':
            game.board.tiles[(1, 1)].action()

# Creating app
sm = ScreenManager()

# Creating screens
welcome = Welcome(name='welcome')
game = Game(name='game')

# adding the screen to the app
sm.add_widget(welcome)
sm.add_widget(game)

class CheckersApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    CheckersApp().run()

# create a tile clear function
# check over the whole code for repeated code
# add a way for the user to undo a move
# add a history page so that user can view all played games and results