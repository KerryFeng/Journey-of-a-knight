#!/usr/bin/env python
# coding: utf-8

# In[8]:


from tkinter import *
from tkinter.messagebox import showinfo

class Game:
    # This class defines global parameters
    def __init__(self, master):
        # Pack header
        self.header = Frame(master, width = 700, height = 75, bg = '#adf8ff', highlightthickness = 0)
        self.header.pack_propagate(0)
        self.header.pack()
        # Items in the header
        self.title_label = Label(self.header, text = 'Journey of a knight', font = ('Comic Sans MS',18), bg = '#adf8ff', fg = '#BF3EFF')
        self.level_number = StringVar()
        self.level_label = Label(self.header, textvariable = self.level_number, font = ('Tempus Sans ITC',12), bg = '#adf8ff', fg = '#2C2CFC')
        self.back_label = Label(self.header, text = 'Back', font = ('Ink Free',15), bg = '#adf8ff', fg = '#BF3EFF')
        self.undo_label = Label(self.header, text = 'Undo', font = ('Ink Free',15), bg = '#adf8ff', fg = '#BF3EFF')
        self.restart_label = Label(self.header, text = 'Restart', font = ('Ink Free',15), bg = '#adf8ff', fg = '#BF3EFF')
        self.last_level_label = Label(self.header, text = 'Last level', font = ('Ink Free',15), bg = '#adf8ff', fg = '#BF3EFF')
        self.next_level_label = Label(self.header, text = 'Next level', font = ('Ink Free',15), bg = '#adf8ff', fg = '#BF3EFF')
        # Canvas parameters
        self.width = 700
        self.height = 575
        self.offset = 5
        # Pack canvas
        self.board = Canvas(master, width = self.width, height = self.height, bg = '#CCCCCC', highlightthickness = 0)
        self.board.pack()
        # Create Level & knight
        self.level = Level(self)
        self.knight = Knight(self)
        
    def enter(self): # Enter start interface or a new level
        if self.level.level_id == 0:
            self.board.bind("<ButtonRelease-1>", Start_Interface(self).start_event)
            Start_Interface(self).draw_start_interface()
        else:
            self.level.grid_pending.clear()
            self.knight.record.clear()
            # Draw level
            self.level.get_design()
            self.level.draw_level()
            # Draw knight
            self.knight.get_design()
            self.knight.draw_knight(self.knight.row, self.knight.column)

    def level_event(self, event): # Event of levels
        if event.y > self.level.upper_offset and event.x > self.level.left_offset and event.y < self.level.upper_offset + self.level.grid_size * self.level.n_row and event.x < self.level.left_offset + self.level.grid_size * self.level.n_column:
            new_row = int((event.y - self.level.upper_offset) / self.level.grid_size) + 1
            new_column = int((event.x - self.level.left_offset) / self.level.grid_size) + 1
            self.knight.move(new_row, new_column)
    
    def back_event(self, event):
        for item in self.board.find_all():
            self.board.delete(item)
        self.level.level_id = 0
        self.level_label.pack_forget()
        self.back_label.pack_forget()
        self.undo_label.pack_forget()
        self.restart_label.pack_forget()
        self.next_level_label.pack_forget()
        self.last_level_label.pack_forget()
        self.enter()
        
    def undo_event(self, event):
        if len(self.knight.record) > 1:
            Grid(self).draw_grid(1, self.knight.row, self.knight.column)
            self.level.level_map[self.knight.row-1][self.knight.column-1] = 1
            self.level.grid_pending.add((self.knight.row, self.knight.column))
            self.knight.record.pop()
            [self.knight.row, self.knight.column] = self.knight.record[-1]
            self.knight.draw_knight(self.knight.row, self.knight.column)
            
    def restart_event(self, event):
        self.level.grid_pending.clear()
        self.knight.record.clear()
        # Draw level
        self.level.get_design()
        self.level.draw_level()
        # Draw knight
        self.knight.get_design()
        self.knight.draw_knight(self.knight.row, self.knight.column)
        
    def last_level_event(self, event):
        if self.level.level_id > 1:
            self.level.level_id -= 1
            self.level_number.set('Level ' + str(self.level.level_id))
            for item in self.board.find_all():
                self.board.delete(item)
            self.enter()
        
    def next_level_event(self, event):
        if self.level.level_id < self.level.level_numbers:
            for item in self.board.find_all():
                self.board.delete(item)
            self.level.level_id += 1
            self.level_number.set('Level ' + str(self.level.level_id))
            self.enter()
        else:
            message = showinfo("Level %d" % self.level.level_id, 'This is the last level!')
                  
    def is_win(self):
        if not self.level.grid_pending:
            message = showinfo("Level %d" % self.level.level_id, 'You win!')
            for item in self.board.find_all():
                self.board.delete(item)
            if self.level.level_id < self.level.level_numbers:
                self.level.level_id += 1
                self.level_number.set('Level ' + str(self.level.level_id))
            else:
                self.level.level_id = 0
                self.level_label.pack_forget()
                self.back_label.pack_forget()
                self.undo_label.pack_forget()
                self.restart_label.pack_forget()
                self.next_level_label.pack_forget()
                self.last_level_label.pack_forget()
            self.enter()
                
class Design:
    def level_design(self, level_id):
        if level_id == 1:
            return [[0,0,0,1,0,0,0],
                    [0,2,0,0,0,1,0],
                    [0,0,1,1,1,0,0],
                    [1,0,1,0,1,0,1],
                    [0,0,1,1,1,0,0],
                    [0,1,0,0,0,1,0],
                    [0,0,0,1,0,0,0]]
        elif level_id == 2:
            return [[0,0,1],
                    [2,1,1],
                    [1,1,1],
                    [1,1,1],
                    [1,1,1],
                    [1,0,1],
                    [1,1,1]]
        elif level_id == 3:
            return [[0,0,1,0,0],
                    [0,1,1,1,0],
                    [1,1,2,1,1],
                    [1,1,1,1,1],
                    [0,1,1,1,0],
                    [0,0,1,0,0],
                    [0,0,1,0,0]]
        elif level_id == 4:
             return [[1,1,1,0,0,0,0],
                    [1,0,1,0,1,1,1],
                    [1,1,1,0,1,0,2],
                    [0,0,1,1,1,1,1],
                    [1,2,1,0,0,0,0]]
        elif level_id == 5:
            return [[0,0,1,1,0,0],
                    [0,1,1,1,1,0],
                    [1,1,1,1,1,1],
                    [2,1,1,1,1,1],
                    [0,0,1,1,0,0],
                    [0,0,1,1,0,0]]
        elif level_id == 6:
            return [[0,2,1,0],
                    [1,1,1,1],
                    [1,1,1,1],
                    [0,1,1,0]]
        elif level_id == 7:
            return [[2,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1],
                    [0,0,0,0,1,1,1],
                    [0,0,0,0,1,1,1],
                    [0,0,0,0,1,1,1],
                    [0,0,0,0,1,1,1],
                    [0,0,0,0,1,1,1]]
        elif level_id == 8:
            return [[1,0,0,1,0,0,0],
                    [0,0,1,0,0,1,0],
                    [0,1,0,0,1,0,0],
                    [2,0,0,1,0,0,1],
                    [0,0,1,0,0,1,0],
                    [0,1,0,0,1,0,0],
                    [0,0,0,1,0,0,1]]
        else:
            return [[2,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1]]
        
    def color_design(self, level_id):
        if level_id == 0:
            c0 = '#ECFCDC'
            c1 = 'green'
            return [[c0,c0,c0,c0,c0,c0,c0,c0,c1,c1],
                    [c0,c0,c0,c0,c0,c0,c0,c0,c1,c1],
                    [c0,c0,c0,c0,c0,c0,c0,c0,c1,c1],
                    [c0,c0,c0,c0,c0,c0,c0,c0,c1,c1],
                    [c0,c0,c0,c0,c1,c1,c1,c1,c1,c1],
                    [c0,c0,c0,c0,c1,c1,c1,c1,c1,c1],
                    [c0,c0,c0,c0,c1,c1,c0,c0,c0,c0],
                    [c0,c0,c0,c0,c1,c1,c0,c0,c0,c0],
                    [c1,c1,c1,c1,c1,c1,c0,c0,c0,c0],
                    [c1,c1,c1,c1,c1,c1,c0,c0,c0,c0]]
        elif level_id == 1:
            c0 = '#CCCCCC'
            c1 = 'orange'
            c2 = '#F24B09'
            return [[c0,c0,c0,c1,c0,c0,c0],
                    [c0,c1,c0,c0,c0,c1,c0],
                    [c0,c0,c2,c2,c2,c0,c0],
                    [c1,c0,c2,c0,c2,c0,c1],
                    [c0,c0,c2,c2,c2,c0,c0],
                    [c0,c1,c0,c0,c0,c1,c0],
                    [c0,c0,c0,c1,c0,c0,c0]]
        elif level_id == 2:
            c0 = '#CCCCCC'
            c1 = '#A1BBAE'
            c2 = '#656F88'
            return [[c0,c0,c2],
                    [c1,c1,c1],
                    [c1,c1,c1],
                    [c1,c1,c1],
                    [c2,c2,c2],
                    [c2,c0,c2],
                    [c2,c2,c2]]
        elif level_id == 3:
            c0 = '#CCCCCC'
            c1 = '#F22C2C'
            return [[c0,c0,c1,c0,c0],
                    [c0,c1,c1,c1,c0],
                    [c1,c1,c1,c1,c1],
                    [c1,c1,c1,c1,c1],
                    [c0,c1,c1,c1,c0],
                    [c0,c0,c1,c0,c0],
                    [c0,c0,c1,c0,c0]]
        elif level_id == 4:
            c0 = '#CCCCCC'
            c1 = '#9B30E7'
            c2 = '#D880FF'
            c3 = '#833CE2'
            return [[c1,c1,c1,c0,c0,c0,c0],
                    [c1,c0,c1,c0,c3,c3,c3],
                    [c1,c1,c1,c0,c3,c0,c3],
                    [c0,c0,c1,c2,c3,c3,c3],
                    [c1,c1,c1,c0,c0,c0,c0]]
        elif level_id == 5:
            c0 = '#CCCCCC'
            c1 = '#719510'
            c2 = '#755026'
            return [[c0,c0,c1,c1,c0,c0],
                    [c0,c1,c1,c1,c1,c0],
                    [c1,c1,c1,c1,c1,c1],
                    [c1,c1,c1,c1,c1,c1],
                    [c0,c0,c2,c2,c0,c0],
                    [c0,c0,c2,c2,c0,c0]]
        elif level_id == 6:
            c0 = '#CCCCCC'
            c1 = '#66AAFF'
            c2 = '#FFFF66'
            return [[c0,c1,c1,c0],
                    [c1,c2,c2,c1],
                    [c1,c2,c2,c1],
                    [c0,c1,c1,c0]]
        elif level_id == 7:
            c0 = '#CCCCCC'
            c1 = '#F5D3B9'
            return [[c1,c1,c1,c1,c1,c1,c1],
                    [c1,c1,c1,c1,c1,c1,c1],
                    [c1,c1,c1,c1,c1,c1,c1],
                    [c0,c0,c0,c0,c1,c1,c1],
                    [c0,c0,c0,c0,c1,c1,c1],
                    [c0,c0,c0,c0,c1,c1,c1],
                    [c0,c0,c0,c0,c1,c1,c1],
                    [c0,c0,c0,c0,c1,c1,c1]]
        elif level_id == 8:
            c0 = '#CCCCCC'
            c1 = '#EF0708'
            c2 = '#FCEC3C'
            c3 = '#36b30e'
            c4 = '#0C8DD6'
            c5 = '#993bf5'
            return [[c1,c0,c0,c2,c0,c0,c0],
                    [c0,c0,c2,c0,c0,c3,c0],
                    [c0,c2,c0,c0,c3,c0,c0],
                    [c2,c0,c0,c3,c0,c0,c4],
                    [c0,c0,c3,c0,c0,c4,c0],
                    [c0,c3,c0,c0,c4,c0,c0],
                    [c0,c0,c0,c4,c0,c0,c5]]
        else:
            c0 = '#A75615'
            c1 = '#EBD5B0'
            return [[c1,c0,c1,c0,c1,c0,c1,c0],
                    [c0,c1,c0,c1,c0,c1,c0,c1],
                    [c1,c0,c1,c0,c1,c0,c1,c0],
                    [c0,c1,c0,c1,c0,c1,c0,c1],
                    [c1,c0,c1,c0,c1,c0,c1,c0],
                    [c0,c1,c0,c1,c0,c1,c0,c1],
                    [c1,c0,c1,c0,c1,c0,c1,c0],
                    [c0,c1,c0,c1,c0,c1,c0,c1]]

    def knight_design(self, level_id):
        if level_id == 1:
            return [2,2]
        elif level_id == 2:
            return [2,1]
        elif level_id == 3:
            return [3,3]
        elif level_id == 4:
            return [5,2]
        elif level_id == 5:
            return [4,1]
        elif level_id == 6:
            return [1,2]
        elif level_id == 7:
            return [1,1]
        elif level_id == 8:
            return [4,1]
        else:
            return [1,1]

class Start_Interface:
    def __init__(self, game):
        self.game = game
        self.level_mark = {(9,1): 1, (10,3): 2, (9,5): 3, (7,6): 4, (5,5): 5, (6,7): 6, (5,9): 7, (3,10): 8, (1,9): 9}
        
    def draw_start_interface(self):
        game.title_label.pack(side=LEFT, padx=20)
        game.board.create_rectangle(0, 0, game.width, game.height, outline = '#ECFCDC', fill = '#ECFCDC')
        game.level.grid_size = (game.height - game.offset * 2) / 10
        game.level.left_offset = (game.width - game.level.grid_size * 10) / 2
        game.level.upper_offset = game.offset
        game.level.map_color = Design().color_design(game.level.level_id)
        for i in range(10):
            for j in range(10):
                self.draw_start_grid(i+1, j+1)
        for key in self.level_mark.keys():
            self.draw_level_mark(self.level_mark[key], key[0], key[1])
    
    def draw_start_grid(self, row, column):
        game.board.create_rectangle(
            (column - 1) * game.level.grid_size + game.level.left_offset, (row - 1) * game.level.grid_size + game.level.upper_offset,
            column * game.level.grid_size + game.level.left_offset, row * game.level.grid_size + game.level.upper_offset,
            outline = game.level.map_color[row-1][column-1], fill = game.level.map_color[row-1][column-1]
        )
        
    def draw_level_mark(self, level_id, row, column):
        center = [(column - 0.5) * game.level.grid_size + game.level.left_offset,(row - 0.5) * game.level.grid_size + game.level.upper_offset]
        r = 24
        points=[
            center[0] - int(r * 0.951),center[1] - int(r * 0.309),
            center[0] + int(r * 0.951),center[1] - int(r * 0.309),
            center[0] - int(r * 0.588),center[1] + int(r * 0.809),
            center[0],center[1] - r,
            center[0] + int(r * 0.588),center[1] + int(r * 0.809),
        ]
        game.board.create_polygon(points, outline = 'yellow',fill = 'yellow')
        game.board.create_text((column - 0.5) * game.level.grid_size + game.level.left_offset,(row - 0.5) * game.level.grid_size + game.level.upper_offset,
                          text = str(level_id), font = ('Bradley Hand ITC', 12), fill = 'purple')
    
    def start_event(self, event): # Event of the start interface
        if event.y > game.level.upper_offset and event.x > game.level.left_offset and event.y < game.level.upper_offset + game.level.grid_size * 10 and event.x < game.level.left_offset + game.level.grid_size * 10:
            row = int((event.y - game.level.upper_offset) / game.level.grid_size) + 1
            column = int((event.x - game.level.left_offset) / game.level.grid_size) + 1
            level_id = self.level_mark.get((row,column), None)
            if level_id != None:
                game.level.level_id = level_id
                game.title_label.pack_forget()
                for item in game.board.find_all():
                    game.board.delete(item)
                game.board.bind("<ButtonRelease-1>", game.level_event)
                # Draw header: Level
                game.level_number.set('Level ' + str(game.level.level_id))
                game.level_label.pack(side=LEFT, padx=20)
                # Draw header: Back
                game.back_label.pack(side=RIGHT, padx=20)
                game.back_label.bind("<ButtonRelease-1>", game.back_event)
                # Draw header: Next level
                game.next_level_label.pack(side=RIGHT, padx=20)
                game.next_level_label.bind("<ButtonRelease-1>", game.next_level_event)
                # Draw header: Last level
                game.last_level_label.pack(side=RIGHT, padx=20)
                game.last_level_label.bind("<ButtonRelease-1>", game.last_level_event)
                # Draw header: Restart
                game.restart_label.pack(side=RIGHT, padx=20)
                game.restart_label.bind("<ButtonRelease-1>", game.restart_event)
                # Draw header: Undo
                game.undo_label.pack(side=RIGHT, padx=20)
                game.undo_label.bind("<ButtonRelease-1>", game.undo_event)
                game.enter()
        
class Level:
    def __init__(self, game):
        self.game = game
        self.level_numbers = 9
        self.level_id = 0
        self.level_map = []
        self.grid_pending = set() # Record remain grids to be go through
        self.map_color = [] # Record color of each grid
        self.n_row = 1
        self.n_column = 1
        self.grid_size = 0
        self.upper_offset = 0 # The offset between the level map and upper margin of canvas
        self.left_offset = 0 # The offset between the level map and left margin of canvas
        
    def get_design(self):
        self.level_map = Design().level_design(self.level_id)
        self.map_color = Design().color_design(self.level_id)
        self.n_row = len(self.level_map)
        self.n_column = len(self.level_map[0])
        grid_size1 = (game.width - game.offset * 2) / self.n_column
        grid_size2 = (game.height - game.offset * 2) / self.n_row
        if grid_size1 < grid_size2:
            self.grid_size = grid_size1
            self.upper_offset = (game.height - self.grid_size * self.n_row) / 2
            self.left_offset = game.offset
        else:
            self.grid_size = grid_size2
            self.upper_offset = game.offset
            self.left_offset = (game.width - self.grid_size * self.n_column) / 2
        # Find all grids to be go through
        for i in range(self.n_row):
            for j in range(self.n_column):
                if self.level_map[i][j] == 1:
                    self.grid_pending.add((i+1, j+1))
            
    def draw_level(self):
        for i in range(self.n_row):
            for j in range(self.n_column):
                Grid(self.game).draw_grid(self.level_map[i][j], i+1, j+1)

class Grid:
    def __init__(self, game):
        self.game = game
        
    def draw_grid(self, draw_type, row, column):
        if draw_type == 0: #Grid of wall
            self.game.board.create_rectangle(
                (column - 1) * game.level.grid_size + game.level.left_offset, (row - 1) * game.level.grid_size + game.level.upper_offset,
                column * game.level.grid_size + game.level.left_offset, row * game.level.grid_size + game.level.upper_offset,
                outline = '#CCCCCC', fill = self.game.level.map_color[row-1][column-1]
            )
        elif draw_type == 1: # Empty gird
            self.game.board.create_rectangle(
                (column - 1) * game.level.grid_size + game.level.left_offset, (row - 1) * game.level.grid_size + game.level.upper_offset,
                column * game.level.grid_size + game.level.left_offset, row * game.level.grid_size + game.level.upper_offset,
                outline = '#CCCCCC', fill = 'white'
            )
        elif draw_type == 2: #Grid entered
            self.game.board.create_rectangle(
                (column - 1) * game.level.grid_size + game.level.left_offset, (row - 1) * game.level.grid_size + game.level.upper_offset,
                column * game.level.grid_size + game.level.left_offset, row * game.level.grid_size + game.level.upper_offset,
                outline = '#CCCCCC', fill = self.game.level.map_color[row-1][column-1]
            )

class Knight:
    def __init__(self, game):
        self.game = game
        self.row = 1
        self.column = 1
        self.record = [] # Record the path of the knight
        
    def get_design(self):
        [self.row, self.column] = Design().knight_design(self.game.level.level_id)
        self.record.append([self.row, self.column])
        
    def draw_knight(self, row, column):
        knight_points1 = ((0.49, 0.17), (0.49, 0.19), (0.51, 0.19), (0.51, 0.2), (0.53, 0.2), (0.52, 0.21), (0.54, 0.21), (0.52, 0.22), (0.54, 0.22), (0.49, 0.23), (0.51, 0.23), (0.55, 0.23), (0.44, 0.24), (0.48, 0.24), (0.5, 0.24), (0.54, 0.24), (0.56, 0.24), (0.44, 0.25), (0.46, 0.25), (0.5, 0.25), (0.52, 0.25), (0.56, 0.25), (0.58, 0.25), (0.43, 0.26), (0.45, 0.26), (0.49, 0.26), (0.51, 0.26), (0.55, 0.26), (0.57, 0.26), (0.4, 0.27), (0.42, 0.27), (0.46, 0.27), (0.48, 0.27), (0.52, 0.27), (0.54, 0.27), (0.58, 0.27), (0.6, 0.27), (0.41, 0.28), (0.43, 0.28), (0.47, 0.28), (0.49, 0.28), (0.53, 0.28), (0.55, 0.28), (0.59, 0.28), (0.61, 0.28), (0.41, 0.29), (0.43, 0.29), (0.47, 0.29), (0.49, 0.29), (0.53, 0.29), (0.55, 0.29), (0.59, 0.29), (0.61, 0.29), (0.4, 0.3), (0.42, 0.3), (0.46, 0.3), (0.48, 0.3), (0.52, 0.3), (0.54, 0.3), (0.58, 0.3), (0.6, 0.3), (0.38, 0.31), (0.4, 0.31), (0.44, 0.31), (0.46, 0.31), (0.5, 0.31), (0.52, 0.31), (0.56, 0.31), (0.58, 0.31), (0.62, 0.31), (0.36, 0.32), (0.4, 0.32), (0.42, 0.32), (0.46, 0.32), (0.48, 0.32), (0.52, 0.32), (0.54, 0.32), (0.58, 0.32), (0.6, 0.32), (0.34, 0.33), (0.36, 0.33), (0.4, 0.33), (0.42, 0.33), (0.46, 0.33), (0.48, 0.33), (0.52, 0.33), (0.54, 0.33), (0.58, 0.33), (0.6, 0.33), (0.64, 0.33), (0.33, 0.34), (0.37, 0.34), (0.39, 0.34), (0.43, 0.34), (0.45, 0.34), (0.49, 0.34), (0.51, 0.34), (0.55, 0.34), (0.57, 0.34), (0.61, 0.34), (0.63, 0.34), (0.32, 0.35), (0.34, 0.35), (0.38, 0.35), (0.4, 0.35), (0.44, 0.35), (0.46, 0.35), (0.5, 0.35), (0.52, 0.35), (0.56, 0.35), (0.58, 0.35), (0.62, 0.35), (0.64, 0.35), (0.33, 0.36), (0.35, 0.36), (0.39, 0.36), (0.41, 0.36), (0.45, 0.36), (0.47, 0.36), (0.51, 0.36), (0.53, 0.36), (0.57, 0.36), (0.59, 0.36), (0.63, 0.36), (0.65, 0.36), (0.33, 0.37), (0.35, 0.37), (0.39, 0.37), (0.41, 0.37), (0.45, 0.37), (0.47, 0.37), (0.52, 0.37), (0.54, 0.37), (0.58, 0.37), (0.6, 0.37), (0.64, 0.37), (0.3, 0.38), (0.34, 0.38), (0.36, 0.38), (0.4, 0.38), (0.42, 0.38), (0.46, 0.38), (0.5, 0.38), (0.54, 0.38), (0.56, 0.38), (0.6, 0.38), (0.62, 0.38), (0.3, 0.39), (0.32, 0.39), (0.36, 0.39), (0.49, 0.39), (0.53, 0.39), (0.55, 0.39), (0.59, 0.39), (0.61, 0.39), (0.65, 0.39), (0.32, 0.4), (0.5, 0.4), (0.52, 0.4), (0.56, 0.4), (0.58, 0.4), (0.62, 0.4), (0.64, 0.4), (0.49, 0.41), (0.51, 0.41), (0.55, 0.41), (0.57, 0.41), (0.61, 0.41), (0.63, 0.41), (0.48, 0.42), (0.5, 0.42), (0.54, 0.42), (0.56, 0.42), (0.6, 0.42), (0.62, 0.42), (0.66, 0.42), (0.48, 0.43), (0.52, 0.43), (0.54, 0.43), (0.58, 0.43), (0.6, 0.43), (0.64, 0.43), (0.66, 0.43), (0.5, 0.44), (0.52, 0.44), (0.56, 0.44), (0.58, 0.44), (0.62, 0.44), (0.64, 0.44), (0.47, 0.45), (0.49, 0.45), (0.53, 0.45), (0.55, 0.45), (0.59, 0.45), (0.61, 0.45), (0.65, 0.45), (0.45, 0.46), (0.49, 0.46), (0.51, 0.46), (0.55, 0.46), (0.57, 0.46), (0.61, 0.46), (0.63, 0.46), (0.45, 0.47), (0.47, 0.47), (0.51, 0.47), (0.53, 0.47), (0.57, 0.47), (0.59, 0.47), (0.63, 0.47), (0.65, 0.47), (0.46, 0.48), (0.48, 0.48), (0.52, 0.48), (0.54, 0.48), (0.58, 0.48), (0.6, 0.48), (0.64, 0.48), (0.66, 0.48), (0.47, 0.49), (0.49, 0.49), (0.53, 0.49), (0.55, 0.49), (0.59, 0.49), (0.61, 0.49), (0.65, 0.49), (0.43, 0.5), (0.47, 0.5), (0.49, 0.5), (0.53, 0.5), (0.55, 0.5), (0.59, 0.5), (0.61, 0.5), (0.65, 0.5), (0.43, 0.51), (0.47, 0.51), (0.49, 0.51), (0.53, 0.51), (0.55, 0.51), (0.59, 0.51), (0.61, 0.51), (0.65, 0.51), (0.42, 0.52), (0.46, 0.52), (0.48, 0.52), (0.52, 0.52), (0.54, 0.52), (0.58, 0.52), (0.6, 0.52), (0.64, 0.52), (0.66, 0.52), (0.45, 0.53), (0.47, 0.53), (0.51, 0.53), (0.53, 0.53), (0.57, 0.53), (0.59, 0.53), (0.63, 0.53), (0.65, 0.53), (0.43, 0.54), (0.45, 0.54), (0.49, 0.54), (0.51, 0.54), (0.55, 0.54), (0.57, 0.54), (0.61, 0.54), (0.63, 0.54), (0.41, 0.55), (0.43, 0.55), (0.47, 0.55), (0.49, 0.55), (0.53, 0.55), (0.55, 0.55), (0.59, 0.55), (0.61, 0.55), (0.65, 0.55), (0.41, 0.56), (0.45, 0.56), (0.47, 0.56), (0.51, 0.56), (0.53, 0.56), (0.57, 0.56), (0.59, 0.56), (0.63, 0.56), (0.65, 0.56), (0.43, 0.57), (0.45, 0.57), (0.49, 0.57), (0.51, 0.57), (0.55, 0.57), (0.57, 0.57), (0.61, 0.57), (0.63, 0.57), (0.41, 0.58), (0.43, 0.58), (0.47, 0.58), (0.49, 0.58), (0.53, 0.58), (0.55, 0.58), (0.59, 0.58), (0.61, 0.58), (0.65, 0.58), (0.41, 0.59), (0.45, 0.59), (0.47, 0.59), (0.51, 0.59), (0.53, 0.59), (0.57, 0.59), (0.59, 0.59), (0.63, 0.59), (0.65, 0.59), (0.42, 0.6), (0.44, 0.6), (0.48, 0.6), (0.5, 0.6), (0.54, 0.6), (0.56, 0.6), (0.6, 0.6), (0.62, 0.6), (0.4, 0.61), (0.42, 0.61), (0.46, 0.61), (0.48, 0.61), (0.52, 0.61), (0.54, 0.61), (0.58, 0.61), (0.6, 0.61), (0.64, 0.61), (0.41, 0.62), (0.45, 0.62), (0.47, 0.62), (0.51, 0.62), (0.53, 0.62), (0.57, 0.62), (0.59, 0.62), (0.63, 0.62), (0.39, 0.64), (0.43, 0.64), (0.45, 0.64), (0.49, 0.64), (0.51, 0.64), (0.55, 0.64), (0.57, 0.64), (0.61, 0.64), (0.63, 0.64), (0.4, 0.65), (0.42, 0.65), (0.46, 0.65), (0.48, 0.65), (0.52, 0.65), (0.54, 0.65), (0.58, 0.65), (0.6, 0.65), (0.64, 0.65), (0.38, 0.66), (0.42, 0.66), (0.44, 0.66), (0.48, 0.66), (0.5, 0.66), (0.54, 0.66), (0.56, 0.66), (0.6, 0.66), (0.62, 0.66), (0.38, 0.67), (0.4, 0.67), (0.44, 0.67), (0.46, 0.67), (0.5, 0.67), (0.52, 0.67), (0.56, 0.67), (0.58, 0.67), (0.62, 0.67), (0.64, 0.67), (0.38, 0.69), (0.4, 0.69), (0.44, 0.69), (0.46, 0.69), (0.5, 0.69), (0.52, 0.69), (0.56, 0.69), (0.58, 0.69), (0.62, 0.69), (0.64, 0.69), (0.35, 0.7), (0.37, 0.7), (0.41, 0.7), (0.43, 0.7), (0.47, 0.7), (0.49, 0.7), (0.53, 0.7), (0.55, 0.7), (0.59, 0.7), (0.61, 0.7), (0.65, 0.7), (0.67, 0.7), (0.37, 0.71), (0.39, 0.71), (0.43, 0.71), (0.45, 0.71), (0.49, 0.71), (0.51, 0.71), (0.55, 0.71), (0.57, 0.71), (0.61, 0.71), (0.63, 0.71), (0.67, 0.71), (0.35, 0.72), (0.39, 0.72), (0.41, 0.72), (0.45, 0.72), (0.47, 0.72), (0.51, 0.72), (0.53, 0.72), (0.57, 0.72), (0.59, 0.72), (0.63, 0.72), (0.65, 0.72), (0.35, 0.73), (0.37, 0.73), (0.41, 0.73), (0.43, 0.73), (0.47, 0.73), (0.49, 0.73), (0.53, 0.73), (0.55, 0.73), (0.59, 0.73), (0.61, 0.73), (0.65, 0.73), (0.67, 0.73), (0.37, 0.74), (0.39, 0.74), (0.43, 0.74), (0.45, 0.74), (0.49, 0.74), (0.51, 0.74), (0.55, 0.74), (0.57, 0.74), (0.61, 0.74), (0.63, 0.74), (0.67, 0.74), (0.35, 0.75), (0.39, 0.75), (0.41, 0.75), (0.45, 0.75), (0.47, 0.75), (0.51, 0.75), (0.53, 0.75), (0.57, 0.75), (0.59, 0.75), (0.63, 0.75), (0.65, 0.75), (0.35, 0.76), (0.37, 0.76), (0.41, 0.76), (0.43, 0.76), (0.47, 0.76), (0.49, 0.76), (0.53, 0.76), (0.55, 0.76), (0.59, 0.76), (0.61, 0.76), (0.65, 0.76), (0.67, 0.76), (0.37, 0.77), (0.39, 0.77), (0.43, 0.77), (0.45, 0.77), (0.49, 0.77), (0.51, 0.77), (0.55, 0.77), (0.57, 0.77), (0.61, 0.77), (0.63, 0.77), (0.67, 0.77), (0.35, 0.78), (0.39, 0.78), (0.41, 0.78), (0.45, 0.78), (0.47, 0.78), (0.51, 0.78), (0.53, 0.78), (0.57, 0.78), (0.59, 0.78), (0.63, 0.78), (0.65, 0.78))
        knight_points2 = ((0.48, 0.15), (0.47, 0.16), (0.49, 0.16), (0.51, 0.16), (0.48, 0.17), (0.51, 0.17), (0.47, 0.18), (0.52, 0.18), (0.54, 0.18), (0.48, 0.19), (0.54, 0.19), (0.47, 0.2), (0.55, 0.2), (0.46, 0.21), (0.48, 0.21), (0.56, 0.21), (0.44, 0.22), (0.46, 0.22), (0.48, 0.22), (0.57, 0.22), (0.42, 0.23), (0.44, 0.23), (0.46, 0.23), (0.58, 0.23), (0.39, 0.24), (0.41, 0.24), (0.43, 0.24), (0.59, 0.24), (0.38, 0.25), (0.4, 0.25), (0.59, 0.25), (0.61, 0.25), (0.38, 0.26), (0.6, 0.26), (0.62, 0.26), (0.37, 0.27), (0.61, 0.27), (0.63, 0.27), (0.37, 0.28), (0.63, 0.28), (0.37, 0.29), (0.64, 0.29), (0.36, 0.3), (0.63, 0.3), (0.33, 0.31), (0.35, 0.31), (0.64, 0.31), (0.32, 0.32), (0.34, 0.32), (0.64, 0.32), (0.3, 0.33), (0.32, 0.33), (0.65, 0.33), (0.28, 0.34), (0.3, 0.34), (0.65, 0.34), (0.27, 0.35), (0.29, 0.35), (0.66, 0.35), (0.29, 0.36), (0.67, 0.36), (0.29, 0.37), (0.66, 0.37), (0.28, 0.38), (0.47, 0.38), (0.66, 0.38), (0.28, 0.39), (0.38, 0.39), (0.4, 0.39), (0.42, 0.39), (0.44, 0.39), (0.46, 0.39), (0.48, 0.39), (0.67, 0.39), (0.3, 0.4), (0.36, 0.4), (0.38, 0.4), (0.4, 0.4), (0.42, 0.4), (0.44, 0.4), (0.46, 0.4), (0.48, 0.4), (0.29, 0.41), (0.31, 0.41), (0.33, 0.41), (0.35, 0.41), (0.37, 0.41), (0.47, 0.41), (0.67, 0.41), (0.31, 0.42), (0.33, 0.42), (0.45, 0.42), (0.47, 0.42), (0.68, 0.42), (0.31, 0.43), (0.46, 0.43), (0.68, 0.43), (0.45, 0.44), (0.67, 0.44), (0.44, 0.45), (0.67, 0.45), (0.43, 0.46), (0.67, 0.46), (0.42, 0.47), (0.44, 0.47), (0.68, 0.47), (0.43, 0.48), (0.68, 0.48), (0.42, 0.49), (0.67, 0.49), (0.41, 0.5), (0.67, 0.5), (0.4, 0.51), (0.42, 0.51), (0.68, 0.51), (0.41, 0.52), (0.68, 0.52), (0.4, 0.53), (0.67, 0.53), (0.39, 0.54), (0.67, 0.54), (0.38, 0.55), (0.4, 0.55), (0.67, 0.55), (0.39, 0.56), (0.67, 0.56), (0.39, 0.57), (0.67, 0.57), (0.39, 0.58), (0.67, 0.58), (0.39, 0.59), (0.67, 0.59), (0.38, 0.6), (0.66, 0.6), (0.38, 0.61), (0.66, 0.61), (0.39, 0.62), (0.66, 0.62), (0.38, 0.63), (0.4, 0.63), (0.42, 0.63), (0.44, 0.63), (0.46, 0.63), (0.48, 0.63), (0.5, 0.63), (0.52, 0.63), (0.54, 0.63), (0.56, 0.63), (0.58, 0.63), (0.6, 0.63), (0.62, 0.63), (0.64, 0.63), (0.66, 0.63), (0.37, 0.64), (0.65, 0.64), (0.67, 0.64), (0.37, 0.65), (0.67, 0.65), (0.37, 0.66), (0.67, 0.66), (0.36, 0.67), (0.66, 0.67), (0.68, 0.67), (0.34, 0.68), (0.36, 0.68), (0.38, 0.68), (0.4, 0.68), (0.42, 0.68), (0.44, 0.68), (0.46, 0.68), (0.48, 0.68), (0.5, 0.68), (0.52, 0.68), (0.54, 0.68), (0.56, 0.68), (0.58, 0.68), (0.6, 0.68), (0.62, 0.68), (0.64, 0.68), (0.66, 0.68), (0.68, 0.68), (0.33, 0.69), (0.35, 0.69), (0.69, 0.69), (0.33, 0.7), (0.69, 0.7), (0.33, 0.71), (0.69, 0.71), (0.33, 0.72), (0.69, 0.72), (0.33, 0.73), (0.69, 0.73), (0.33, 0.74), (0.69, 0.74), (0.33, 0.75), (0.69, 0.75), (0.33, 0.76), (0.69, 0.76), (0.33, 0.77), (0.69, 0.77), (0.33, 0.78), (0.69, 0.78), (0.33, 0.79), (0.35, 0.79), (0.37, 0.79), (0.39, 0.79), (0.41, 0.79), (0.43, 0.79), (0.45, 0.79), (0.47, 0.79), (0.49, 0.79), (0.51, 0.79), (0.53, 0.79), (0.55, 0.79), (0.57, 0.79), (0.59, 0.79), (0.61, 0.79), (0.63, 0.79), (0.65, 0.79), (0.67, 0.79), (0.69, 0.79), (0.33, 0.8), (0.35, 0.8), (0.37, 0.8), (0.39, 0.8), (0.41, 0.8), (0.43, 0.8), (0.45, 0.8), (0.47, 0.8), (0.49, 0.8), (0.51, 0.8), (0.53, 0.8), (0.55, 0.8), (0.57, 0.8), (0.59, 0.8), (0.61, 0.8), (0.63, 0.8), (0.65, 0.8), (0.67, 0.8), (0.69, 0.8))
        thickness = 1.25
        if game.level.n_row < 5 and game.level.n_column < 5:
            thickness *= 2
        for point in knight_points1: # Fill
            self.draw_point((column - 1 + point[0]) * game.level.grid_size + game.level.left_offset,
                            (row - 1 + point[1]) * game.level.grid_size + game.level.upper_offset, 1.16 * thickness, 'yellow')
        for point in knight_points2: # Outline
            self.draw_point((column - 1 + point[0]) * game.level.grid_size + game.level.left_offset, (row - 1 + point[1]) * game.level.grid_size + game.level.upper_offset, thickness, 'black')
   
    def draw_point(self, x, y, r, color):
        self.game.board.create_rectangle(x-r, y-r, x+r, y+r, outline = color, fill = color)
    
    def move(self, new_row, new_column):
        row_df = new_row - self.row
        column_df = new_column - self.column
        if (row_df in [-1,1] and column_df in [-2,2]) or (row_df in [-2,2] and column_df in [-1,1]):
            if game.level.level_map[new_row-1][new_column-1] == 1:
                # Draw the old position
                Grid(self.game).draw_grid(game.level.level_map[self.row-1][self.column-1], self.row, self.column)
                # Update position information
                self.row = new_row
                self.column = new_column
                self.record.append([self.row, self.column])
                game.level.level_map[self.row-1][self.column-1] = 2
                game.level.grid_pending.discard((self.row, self.column))
                # Draw the new position
                Grid(self.game).draw_grid(2, self.row, self.column)
                self.draw_knight(self.row, self.column)
                # Determine if the knight goes through all grids
                game.is_win()         
    
if __name__ == '__main__':
    root = Tk()
    # Window parameters
    root.title('Journey of a knight')
    root.geometry('700x650+100+40')
    root.resizable(0,0)
    
    game = Game(root) 
    game.enter()
    
    root.mainloop()

