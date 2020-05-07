import pyxel 
import os
import json
from random import randint
import math

class App():
    timer = 0
    def __init__(self):
        self.player = self.Player(72, 100)
        self.enemies = self.EnemyManagement()
        self.ret = self.Rectb()
        pyxel.init(144, 120, caption="Jam",fps=60)
        pyxel.load("assets/my_resource.pyxres")
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)
    
    class Rectb():
        def __init__(self):
            self.x = 0
            self.y = 0
        
        def update(self):
            if pyxel.btnr(pyxel.MOUSE_LEFT_BUTTON) or pyxel.btnr(pyxel.MOUSE_RIGHT_BUTTON):
                # マウスの位置を記録
                self.x = pyxel.mouse_x
                self.y = pyxel.mouse_y
        
        def draw(self):
            # 線の色が軌道を決める。
            if pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
                pyxel.line(pyxel.mouse_x, pyxel.mouse_y, self.x, self.y, col=9)
            if pyxel.btn(pyxel.MOUSE_RIGHT_BUTTON):
                pyxel.line(pyxel.mouse_x, pyxel.mouse_y, self.x, self.y, col=11)
    
    class Enemy():
        def __init__(self, x, y, speed):
            self.x = x
            self.y = y
            self.speed = speed
            self.monitor_in = True
        
        # シンプルに落ちるところから
        def update(self):
            self.y += self.speed
            for i in range(4):
                if pyxel.pget(self.x+4, self.y+i) == 9:
                    self.x -= 2
                    pyxel.play(0, 2)
                if pyxel.pget(self.x+4, self.y+i) == 11:
                    self.x += 2
                    pyxel.play(0, 2)

        def draw(self):
            pyxel.circ(self.x, self.y, 2, col=8)
    
    class Enemy_2(Enemy):
        def __init__(self, x, y, speed, rad):
            super().__init__(x, y, speed)
            self.monitor_in = True
            self.rad = math.radians(rad)
        
        def update(self):
            self.x += self.speed * math.cos(self.rad)
            self.y += self.speed * math.sin(-self.rad)
            for i in range(4):
                if pyxel.pget(self.x+2, self.y+i) == 9:
                    self.x -= 2
                    pyxel.play(0, 2)
                if pyxel.pget(self.x+2, self.y+i) == 11:
                    self.x += 2
                    pyxel.play(0, 2)

        def draw(self):
            pyxel.circ(self.x, self.y, 2, col=10)

    class Enemy_3(Enemy):
        def __init__(self, x, y, speed, target):
            super().__init__(x, y, speed)
            self.monitor_in = True
            self.tx = target.x
            self.ty = target.y
        
        def update(self):
            dx = self.tx - self.x
            dy = self.ty - self.y
            rad = math.atan2(-dy, dx)
            deg = math.degrees(rad)
            self.x += self.speed * math.cos(deg)
            self.y += self.speed * -math.sin(deg)

            for i in range(4):
                if pyxel.pget(self.x+2, self.y+i) == 9:
                    self.x -= 2
                    pyxel.play(0, 2)
                if pyxel.pget(self.x+2, self.y+i) == 11:
                    self.x += 2
                    pyxel.play(0, 2)

        def draw(self):
            pyxel.circ(self.x, self.y, 2, col=10)
    
    class EnemyManagement():
        def __init__(self):
            self.enemy_list = []
            self.item_list = []
            self.pattern_list = self.read_pattern()
            self.pattern_list_2 = self.read_pattern2()
            self.radian_pattern = [i for i in range(45, 135, 45)]
            self.fClose()
        
        # 予め作ったパターンを記録したjsonファイルを読み込む
        def read_pattern(self):
            dirname = os.path.dirname(__file__)
            path = os.path.join(dirname, "assets/data.json")
            self.in_file = open(path, "r", encoding='utf-8')
            self.json_obj = json.load(self.in_file)
            return self.json_obj["enemies"]

        def read_pattern2(self):
            return self.json_obj["enemies_2"]
        
        def fClose(self):
            self.in_file.close()
        
        def update(self, target):
            App.timer += 1
            for pattern in self.pattern_list:
                if int(pattern["timing"]) == App.timer:
                    enemy = App.Enemy(pattern["x"], pattern["y"], pattern["speed"])
                    self.enemy_list.append(enemy)

            for pattern in self.pattern_list_2:
                if int(pattern["timing"]) == App.timer:
                    enemy = App.Enemy_2(pattern["x"], pattern["y"], pattern["speed"], pattern["radian"])
                    self.enemy_list.append(enemy)
                    enemy = App.Enemy_3(pattern["x"], pattern["y"], pattern["speed"], target)
                    self.enemy_list.append(enemy)

            if randint(0, 99) < App.timer // 400:
                item = App.Item(randint(0, 144), 20)
                self.item_list.append(item)
            
            for i in self.enemy_list:
                i.update()

            for i in self.item_list:
                i.update()
            
            for j in self.enemy_list:
                if j.x <= 0 or j.x >= 144:
                    j.monitor_in = False
                if j.y >= 120:
                    j.monitor_in = False
            
            for j in self.item_list:
                if j.y >= 120:
                    j.monitor_in = False
            
            # クラスを消しても意味がなく、リストから削除しなければならないわけなので、
            for l,e in enumerate(self.enemy_list):
                if e.monitor_in == False:
                    self.enemy_list.pop(l)

            for l,e in enumerate(self.item_list):
                if e.monitor_in == False:
                    self.item_list.pop(l)

        def draw(self):
            for i in self.enemy_list:
                i.draw()

            for i in self.item_list:
                i.draw()

    class Item(Enemy):
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.monitor_in = True
        
        def update(self):
            self.y += 1
            for i in range(8):
                if pyxel.pget(self.x+i, self.y+i) == 9:
                    self.monitor_in = False
                    pyxel.play(0, 3)
                if pyxel.pget(self.x+i, self.y+i) == 11:
                    self.monitor_in = False
                    pyxel.play(0, 3)
            
            for i in range(8):
                if pyxel.pget(self.x + i, self.y + i) == 7:
                    self.monitor_in = False
        
        def draw(self):
            pyxel.blt(self.x, self.y, 0, 8, 8, 8, 8, colkey=0)

    class Player():
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.before_x = x
            self.before_y = y
            self.life = 8
            self.alive = True
            self.score = 0
        
        def update(self):
            if self.alive:
                if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
                    self.x -= 3
                    pyxel.play(0, 5)
                    if self.x <= 0:
                        self.x = 0

                if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
                    self.x += 3
                    pyxel.play(0, 5)
                    if self.x == 136:
                        self.x = 136
                
                if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.GAMEPAD_1_UP):
                    self.y -= 3
                    pyxel.play(0, 5)
                    if self.y <= 0:
                        self.y = 8 

                if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
                    self.y += 3
                    pyxel.play(0, 5)
                    if self.y >= 128:
                        self.y = 128
                
                for i in range(2):
                    for j in range(4):
                        if pyxel.pget(self.x + 2+i, self.y + j) == 8 or \
                            pyxel.pget(self.x + 2+i, self.y + j) == 10:
                            self.life -= 1
                            if self.life <= 0:
                                pyxel.play(0, 0)

                for j in range(8):
                    if pyxel.pget(self.x+j, self.y + j) == 14:
                        pyxel.play(0, 1)
                        self.score += 10
                
            if self.life <= 0:
                self.alive = False
                if pyxel.btn(pyxel.KEY_R):
                    App.timer = 0
                    self.alive = True
                    self.x = self.before_x
                    self.y = self.before_y
                    self.life = 8
                    self.score = 0
        
        def myxy(self):
            return (self.x, self.y)

        def draw(self):
            if self.alive:
                pyxel.blt(self.x, self.y, 0, 0, 0, 8, 8, colkey=0)
            for i in range(self.life):
                pyxel.rect(8 * i + 4, 2, 8, 8, col=12)

            if self.alive == False:
                pyxel.text(48, 16, "GAME OVER", col=7)
                pyxel.text(36, 60, "PRESS \"R\" TO RETRY", col=7)

            pyxel.text(48, 8, "SCORE:" + str(self.score), col=7)

    def update(self):
        self.player.update()
        self.enemies.update(self.player)
        self.ret.update()

    def draw(self):
        pyxel.cls(0)
        self.player.draw()
        self.enemies.draw()
        self.ret.draw()
        if App.timer >= 1800:
            pyxel.text(0, 16, str(App.timer // 60) + " OVER",col=7)

App()