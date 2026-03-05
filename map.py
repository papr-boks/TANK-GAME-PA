from enum import IntEnum
from pathlib import Path
from tkinter import Canvas
from typing import Callable

import numpy as np

from utils import overlap
from assets import open_and_resize_photoimage, RESIZE_SCALE

TILE_SIZE = int(32 * RESIZE_SCALE)
ASSETS_PATH = Path("assets")


def create_map(map_str: str) -> "Map":
    """
    Read and parse a game map from a file.

    A map file is a text file where each non-blank character represents a tile in the map.

    A map file may contain the following characters:

    - "." represents an empty tile (Tile.EMPTY).
    - "#" represents a rock tile (Tile.ROCK).
    - "@" represents a bomb tile (Tile.BOMB).
    - "0" represents an empty tile and indicates the initial position of the tank for player 1.
    - "1" represents an empty tile and indicates the initial position of the tank for player 2.

    Each line in the file represents a row in the map and each non-blank character in the lines represents a tile.
    The number of non-space characters in the first line indicates the number of columns in the map.
    The number of lines in the file indicates the number of rows in the map.

    For example, the following is a valid map file:

    ```
    0 . .
    . # .
    . . 1
    ```

    The above map file represents a 3x3 map with the initial positions of tank 1 and tank 2, on the top-left and
    bottom-right corners, respectively. There is 1 rock tile in the center of the map with 8 empty tiles
    surrounding it.

    :param map_str: the file content as a string
    :return: the read and parsed game map
    """
    # a list of strings, each string is a line in the file
    lines = map_str.splitlines()

    # the number of lines in the file, i.e. the number of rows in the map
    rows = len(lines)

    # the number of non-space characters in the first line, i.e. the number of columns in the map
    cols = len(lines[0].split())

    # create a new Map object with the given number of columns and rows
    game_map = Map(cols, rows)

    # TODO: Task 1.1

    splitted_map_str = []
    for x in range(len(lines)):
        splitted_map_str.append(lines[x].split())
    
    for i in range(rows):
        for j in range(cols):
            char = splitted_map_str[i][j]
            if char == '#':
                game_map.map[i][j] = Tile.ROCK
            elif char == '.':
                game_map.map[i][j] = Tile.EMPTY
            elif char == '@':
                game_map.map[i][j] = Tile.BOMB
            elif char == '0':
                game_map.tank_position_map[0] = (j + 0.5, i + 0.5)
                game_map.map[i][j] = Tile.EMPTY
            elif char == '1':
                game_map.tank_position_map[1] = (j + 0.5, i + 0.5)
                game_map.map[i][j] = Tile.EMPTY


    '''splitted_map_str=[]
    for x in range(len(lines)):
        splitted_map_str.append([])
        splitted_map_str[x][:]=lines[x].split()
    for i in rows:
        for j in cols:
            if splitted_map_str[j][i] == '#':
                game_map[j][i]=Tile(1)
            elif splitted_map_str[j][i] == '.':
                game_map[j][i]=Tile(0)
            elif splitted_map_str[j][i] == '@':
                game_map[j][i]=Tile(2)
            elif splitted_map_str[j][i] == '1':
                game_map.tank_position_map['player1'] = [j+0.5,i+0.5]
                game_map[j+0.5][i+0.5] = 0
            elif splitted_map_str[j][i] == '2':
                game_map.tank_position_map['player2'] = [j+0.5,i+0.5]
                game_map[j+0.5][i+0.5] = 1    
                行列错误,for loop range错误,坦克的命名错误,类型错误
                '''
                # TODO: Task 1.1 END
    return game_map


class Tile(IntEnum):
    """
    An enumeration of integer values to represent tiles in the map.
    You should use Tile.EMPTY, Tile.ROCK and Tile.BOMB to represent the corresponding tiles instead of 0, 1 and 2.
    """
    EMPTY = 0
    ROCK = 1
    BOMB = 2


class Map:
    """
    The Map class. Represents a map of the game.
    """
    def __init__(self, cols: int, rows: int):
        """
        Initializes the map.
        :param cols: the number of columns in the map
        :param rows: the number of rows in the map
        """
        self.cols = cols
        self.rows = rows
        self.width = cols * TILE_SIZE
        self.height = rows * TILE_SIZE

        self.prev_map = None
        self.map = np.full((rows, cols), Tile.EMPTY)
        self.canvas_floor_map = np.full((rows, cols), None)
        self.canvas_object_map = np.full((rows, cols), None)

        self.FLOOR_IMAGE = open_and_resize_photoimage(
            image_path=(ASSETS_PATH / "floor.png")
        )
        self.ROCK_IMAGE = open_and_resize_photoimage(
            image_path=(ASSETS_PATH / "rock.png")
        )
        self.BOMB_IMAGE = open_and_resize_photoimage(
            image_path=(ASSETS_PATH / "bomb.png")
        )

        self.tank_position_map = {}

    def map_diff(self):
        """
        Calculates the difference between the current map `self.map` and the previous map `self.prev_map`.

        If the previous map `self.prev_map` is None, it will be set to the current map `self.map` and the difference
        will be an array of True.

        After calculating the difference, the previous map `self.prev_map` will be updated to the current map
        `self.map`.

        YOU ARE NOT ALLOWED TO USE ANY LOOPS OR COMPREHENSION IN THIS TASK.

        :return: a boolean n-D array of the same shape as the map, where the element indicates whether the corresponding
        tile has changed.
        """
        # TODO: Task 1.2
        if self.prev_map is None:
            self.prev_map = self.map.copy()
            return np.ones_like(self.map, dtype=bool)
        else:
            diff = self.map != self.prev_map
            self.prev_map = self.map.copy()
            return diff
        
        
        
        if self.prev_map == None:
            self.prev_map = self.map
            bool_map = self.map == self.prev_map
        else:
            bool_map = self.map == self.prev_map
        return bool_map

        # TODO: Task 1.2 END

    def draw_on(self, canvas: Canvas):
        for y, x in np.argwhere(np.logical_not(self.canvas_floor_map)):
            self.canvas_floor_map[y][x] = canvas.create_image(
                x * TILE_SIZE, y * TILE_SIZE, image=self.FLOOR_IMAGE, anchor="nw"
            )

        diff = self.map_diff()

        for y, x in np.argwhere(diff):
            tile = self.map[y][x]
            canvas.delete(self.canvas_object_map[y][x])  # type: ignore
            if tile == Tile.ROCK:
                self.canvas_object_map[y][x] = canvas.create_image(
                    x * TILE_SIZE, y * TILE_SIZE, image=self.ROCK_IMAGE, anchor="nw"
                )
            if tile == Tile.BOMB:
                self.canvas_object_map[y][x] = canvas.create_image(
                    x * TILE_SIZE, y * TILE_SIZE, image=self.BOMB_IMAGE, anchor="nw"
                )

    def collides(
        self, x: float, y: float, width: float = 0, height: float = 0
    ) -> dict[tuple[int, int], Tile] | None:
        """
        Check if an object (not the 'object' in OOP >.<) whose hit-box centered at (x, y) with the size (width, height)
        collides with the map.

        An object collides with the map if:

        1. the object's hit-box, which means the rectangle it occupies in this assignment, overlaps with a non-empty tile, OR
        2. the object's hit-box, or partial hit-box is outside or overlaps with the map boundary.

        In the 1st case, the function returns a dictionary indicating the tile(s) that the object collides with; the
        key is the (x, y) coordinate of the top left corner of the tile(s), and the value is the type of the tile(s).
        Example: {(0, 0): Tile.BOMB}

        In the 2nd case, the function returns None. The 2nd case takes precedence over the 1st case.

        If neither of the two cases happens, the function returns an empty dictionary.

        Overlaps are inclusive, that is, if the hit-box of the object touches the map boundary or a tile,
        it is considered as overlapping.

        :param x: the x-coordinate of the center of the object's hit-box
        :param y: the y-coordinate of the center of the object's hit-box
        :param width: the width of the object's hit-box
        :param height: the height of the object's hit-box
        :return: a dictionary or None
        """
        # TODO: Task 2.1
        from utils import overlap
    
        # 定义物体的边界框
        obj_left = x - width/2
        obj_top = y - height/2
        obj_right = x + width/2
        obj_bottom = y + height/2
        obj_rect = (obj_left, obj_top, obj_right, obj_bottom)
        
        # 检查是否超出地图边界
        if (obj_left < 0 or obj_right > self.cols or 
            obj_top < 0 or obj_bottom > self.rows):
            return None
        
        collision_tiles = {}
        
        # 修正：计算物体可能覆盖的所有格子，包括边界情况
        start_col = int(max(0, obj_left))
        end_col = int(min(self.cols - 1, obj_right - 1e-5))  # 减去小量避免浮点误差
        start_row = int(max(0, obj_top))
        end_row = int(min(self.rows - 1, obj_bottom - 1e-5))
        
        # 检查所有可能碰撞的格子
        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                tile = self.map[row][col]
                if tile != Tile.EMPTY:
                    # 定义格子的边界框
                    tile_left = col
                    tile_top = row
                    tile_right = col + 1
                    tile_bottom = row + 1
                    tile_rect = (tile_left, tile_top, tile_right, tile_bottom)
                    
                    # 使用 overlap 函数检查重叠
                    if overlap(obj_rect, tile_rect):
                        collision_tiles[(col, row)] = tile
        
        return collision_tiles
        '''
        from utils import overlap
        obj_left = x - width/2
        obj_top = y - height/2
        obj_right = x + width/2
        obj_bottom = y + height/2
        obj_rect = (obj_left, obj_top, obj_right, obj_bottom)
        

        if (obj_left < 0 or obj_right > self.cols or 
            obj_top < 0 or obj_bottom > self.rows):
            return None
        
        collision_tiles = {}
        

        start_col = int(max(0, obj_left))
        end_col = int(min(self.cols - 1, obj_right - 0.001)) 
        start_row = int(max(0, obj_top))
        end_row = int(min(self.rows - 1, obj_bottom - 0.001))
        

        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                tile = self.map[row][col]
                if tile != Tile.EMPTY:
                    tile_left = col
                    tile_top = row
                    tile_right = col + 1
                    tile_bottom = row + 1
                    tile_rect = (tile_left, tile_top, tile_right, tile_bottom)
                    
                    if overlap(obj_rect, tile_rect):
                        collision_tiles[(col, row)] = tile
        
        return collision_tiles
        '''
        '''
        from utils import overlap
        ra = (x-width/2,y+height/2,x+width/2,y-height/2)
        rb = (int(x),int(y),int(x)+1,int(y)-1)
        overlap_dict = {}
        if x+width/2>self.cols or y+height/2 > self.rows or x-width/2<0 or y-height/2<0:
            return None
        elif overlap(ra,rb):
            overlap_dict[(int(x),int(y))] = self.map[int(x),int(y)]
            return overlap_dict
        else:
            return overlap_dict
        '''


        
        # TODO: Task 2.1 END

    def collides_with_tank(
        self, x: float, y: float, width: float = 0, height: float = 0
    ) -> int | None:
        """
        Check if an object whose hit-box centered at (x, y) with the size (width, height) collides with a tank.

        an object collides with the tank if its hit-box overlaps with the tank's hit-box.

        Overlaps are inclusive, that is, if the hit-box of the object touches the map boundary or a tile,
        it is considered as overlapping.

        The size of the tank's hit-box is 1x1.

        You may assume that the object will not collide with multiple tanks at the same time.

        :param x: the x-coordinate of the center of the object's hit-box
        :param y: the y-coordinate of the center of the object's hit-box
        :param width: the width of the object's hit-box
        :param height: the height of the object's hit-box
        :return: the tank id that the object collides with, or None if the object does not collide with any tank
        """
        # TODO: Task 2.2
        from utils import overlap
        
        # 定义物体的边界框
        obj_left = x - width/2
        obj_top = y - height/2
        obj_right = x + width/2
        obj_bottom = y + height/2
        obj_rect = (obj_left, obj_top, obj_right, obj_bottom)
        
        # 检查每个坦克
        for tank_id, (tank_x, tank_y) in self.tank_position_map.items():
            # 定义坦克的边界框（坦克大小为1x1）
            tank_left = tank_x - 0.5
            tank_top = tank_y - 0.5
            tank_right = tank_x + 0.5
            tank_bottom = tank_y + 0.5
            tank_rect = (tank_left, tank_top, tank_right, tank_bottom)
            
            # 使用 overlap 函数检查重叠
            if overlap(obj_rect, tank_rect):
                return tank_id
        
        return None
        return None
        from utils import overlap
        

        obj_left = x - width/2
        obj_top = y - height/2
        obj_right = x + width/2
        obj_bottom = y + height/2
        obj_rect = (obj_left, obj_top, obj_right, obj_bottom)

        for tank_id, (tank_x, tank_y) in self.tank_position_map.items():

            tank_left = tank_x - 0.5
            tank_top = tank_y - 0.5
            tank_right = tank_x + 0.5
            tank_bottom = tank_y + 0.5
            tank_rect = (tile_left, tile_top, tile_right, tile_bottom)
            

            if overlap(obj_rect, tank_rect):
                return tank_id
        
        return None

        from utils import overlap
  
        obj_left = x - width/2
        obj_top = y - height/2
        obj_right = x + width/2
        obj_bottom = y + height/2
        obj_rect = (obj_left, obj_top, obj_right, obj_bottom)
        

        for tank_id, (tank_x, tank_y) in self.tank_position_map.items():

            tank_left = tank_x - 0.5
            tank_top = tank_y - 0.5
            tank_right = tank_x + 0.5
            tank_bottom = tank_y + 0.5
            tank_rect = (tank_left, tank_top, tank_right, tank_bottom)
            

            if overlap(obj_rect, tank_rect):
                return tank_id

            from utils import overlap
            play1 = self.tank_position_map['player1']
            play2 = self.tank_position_map['player2']
            r1 = (paly1[0]-0.5,play1[1]-0.5,play1[0]+0.5,play1[1]+0.5)
            r2 = (paly2[0]-0.5,play2[1]-0.5,play2[0]+0.5,play2[1]+0.5)
            ra = (x-width/2,y-height/2,x+width/2,y+height/2)
            if overlap(r1,ra):
                return 0
            if overlap(r2,ra):
                return 1
            if not overlap(r1,ra) and overlap(r1,ra):
                return None

        # TODO: Task 2.2 END

    def nearest_position(
        self,
        x: float,
        y: float,
        new_x: float,
        new_y: float,
        width: float = 0,
        height: float = 0,
    ) -> tuple[float, float]:
        """
        Find the nearest position from (x, y) to (new_x, new_y) that does not collide with the map.
        """
        if self.collides(new_x, new_y, width, height) == {}:
            return new_x, new_y
        else:
            if new_x != x:
                new_x, _ = self.nearest_position(
                    x, y, new_x + np.sign(x - new_x) / 32, new_y, width, height
                )
            if new_y != y:
                _, new_y = self.nearest_position(
                    x, y, new_x, new_y + np.sign(y - new_y) / 32, width, height
                )
            return new_x, new_y

    def trigger_bomb(
        self, canvas: Canvas, col: int, row: int, explode: Callable[[int, int], None]
    ) -> None:
        """
        Trigger a bomb at the given position (col, row) and explode the surrounding tiles.

        The bomb will explode the surrounding tiles in a 3x3 square centered at the bomb, including the bomb itself.
        That is, all the tiles in the 3x3 square will be set to Tile.EMPTY.

        If another bomb is exploded by the current bomb, that is, if there are other bombs in the 3x3 square,
        the bomb will trigger these bombs, causing a chain reaction. You may call this function recursively to
        trigger the explosion of another bomb. Note that in calling this function recursively, you should pass the same
        `canvas` object and `explode` function.
        Do not use `canvas.after()` or some other similar functions to schedule the triggering.
        Otherwise, you may get trouble during grading.

        You can assume that there is indeed a bomb at the [row][column] position specified by the parameters.
        Moreover, you should NOT call `trigger_bomb()` on a position if there is not a bomb there.

        After modifying the map, for example, setting a tile to `Tile.EMPTY`, you should call
        `self.draw_on(canvas)` to update the canvas.

        :param canvas: the canvas to draw on
        :param col: the column of the bomb
        :param row: the row of the bomb
        :param explode: a function that triggers the explosion animation at the given position (col, row)
        """

        # Trigger the explosion animation at the bomb position.
        explode(col, row)

        # Example: the tile at (col, row) is a bomb, so set it to Tile.EMPTY.
        # Important: After modifying the map, call `self.draw_on(canvas)` to update the canvas.
        self.map[row][col] = Tile.EMPTY
        self.draw_on(canvas)

        # You may start to implement the remaining part of the function here.

        # TODO 3
        bombs_to_trigger = []
        
        # 遍历3x3区域（包括炸弹自身）
        for i in range(-1, 2):  # i = -1, 0, 1
            for j in range(-1, 2):  # j = -1, 0, 1
                # 计算周围格子的坐标
                new_col = col + i
                new_row = row + j
                
                # 检查坐标是否在地图范围内
                if 0 <= new_col < self.cols and 0 <= new_row < self.rows:
                    # 清除这个格子（无论是什么类型）
                    self.map[new_row][new_col] = Tile.EMPTY
                    
                    # 如果这个位置有炸弹，添加到待触发列表
                    if new_col != col or new_row != row:  # 避免重复触发当前炸弹
                        if self.map[new_row][new_col] == Tile.BOMB:
                            bombs_to_trigger.append((new_col, new_row))
        
        # 绘制更新后的地图
        self.draw_on(canvas)
        
        # 递归触发所有找到的炸弹
        for bomb_col, bomb_row in bombs_to_trigger:
            self.trigger_bomb(canvas, bomb_col, bomb_row, explode)
        '''for i in range(-1, 2):  
            for j in range(-1, 2):  
                new_col = col + i
                new_row = row + j
                

                if 0 <= new_col < self.cols and 0 <= new_row < self.rows:
                    if self.map[new_row][new_col] == Tile.BOMB:
                        self.trigger_bomb(canvas, new_col, new_row, explode)
        
'''
        # TODO 3 END
