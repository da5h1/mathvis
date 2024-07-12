import pygame as pg
import numpy as np
import re 

class Vertex:
  def __init__(self, position: int, capacity: int, content: list):
    self.position = position
    self.capacity = capacity
    self.content = content

  def push(self):
    if self.content[0] == 0: #если стержень пуст, с него нельзя снять кольца
      print('you can not push from empty list')
      return
    if self.content[self.capacity-1] != 0: #если стержень полон, мы снимаем последнее кольцо
      output = self.content[self.capacity-1]
      self.content[self.capacity-1] = 0
      return output
    for i in range(self.capacity):
      if self.content[i] == 0:
        output = self.content[i-1]
        self.content[i-1] = 0
        return output

  def pop(self, size):
    if self.content[0] == 0: #если стержень пуст, мы добавляем одно кольцо
      self.content[0] = size
      return
    if self.content[self.capacity-1] != 0: #если стержень полон, мы не можем добавить больше колец
      print("vertex is full")
      return 
    for i in range(self.capacity):
      if self.content[i] == 0:
        if self.content[i-1] <= size:
          print("next piece should be smaller") 
          return "bring it back"
        else:
          self.content[i] = size
        return

class Game:
  def __init__(self):
    self.config = [Vertex(0, 8, [8,7,6,5,4,3,2,1]), Vertex(1, 8, [0,0,0,0,0,0,0,0]), Vertex(2, 8, [0,0,0,0,0,0,0,0])]

  def move(self, move):
    pattern = r'[1-3]{2}'
    if not re.fullmatch(pattern, move):
      return 
    # 3->2, 2->1, 1->0 
    s = ''
    s += str(int(move[0])-1)
    s += str(int(move[1])-1)
    move = s
    
    source = int(move[0])
    sink = int(move[1])
    size = self.config[source].push()
    if size == None:
      return 
    answer = self.config[sink].pop(size)
    if answer == "bring it back":
      self.config[source].pop(size)
    
  def get_config(self):
    return self.config
      
def draw_config(screen, config):
    pg.draw.polygon(screen, (255, 255, 255), [(200, 80), (131, 200), (269, 200)])
    for vertex_index, vertex in enumerate(config):
      rel_height = 12
      if vertex_index == 0:
        start_point = (165, 140)
        angle = 60
      if vertex_index == 1:
        start_point = (235, 140)
        angle = -60
      if vertex_index == 2:
        start_point = (200, 200)
        angle = 180
      for brick_index, brick_width in enumerate(vertex.content):
        if brick_width == 0:
          break
        image_orig = pg.Surface((brick_width * 16, 15))
        image_orig.set_colorkey((0, 0, 0))
        image_orig.fill((200 - brick_index*200/10, 200 - brick_index*200/10, 200 - brick_index*200/10))
        image = image_orig.copy()
        image.set_colorkey((0, 0, 0))
        rect = image.get_rect()
        new_image = pg.transform.rotate(image_orig, angle)
        rect = new_image.get_rect()
        rect.center = (start_point[0] - np.sin(angle*2*3.1415/360)*rel_height, start_point[1] - np.cos(angle*2*3.1415/360)*rel_height)
        screen.blit(new_image, rect)
        rel_height += 20
    
def main():
    g = Game()
    screen = pg.display.set_mode((400, 400))
    font = pg.font.Font(None, 32)
    clock = pg.time.Clock()
    input_box = pg.Rect(150, 10, 5, 30)
    color = pg.Color('dodgerblue2')
    RED = (255, 0, 0)

    text = ''
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    g.move(text)
                    text = ''
                elif event.key == pg.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        screen.fill((30, 30, 30))
        txt_surface = font.render(text, True, color)
        width = max(100, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pg.draw.rect(screen, color, input_box, 2)
        draw_config(screen, g.get_config())
        pg.display.flip()
        clock.tick(30)

pg.init()
main()
pg.quit()