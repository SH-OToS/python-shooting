# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
from random import randint

def main():
  (w,h) = (400,400)   # 画面サイズ
  pygame.init()       # pygame初期化
  pygame.font.init()  # テキストを出すやつ
  myfont = pygame.font.SysFont('Comic Sans MS', 30) # set font
  pygame.display.set_mode((w, h), 0)  # 画面設定
  screen = pygame.display.get_surface()
  fps = 0
  BULLED_MAX_LENGTH = 10
  ENEMY_MAX_LENGTH = 10
  score = 0
  enemys = []
  bulleds = []

  # player
  (p_w,p_h) = (20,50)
  tmp = pygame.image.load("./home.png").convert_alpha()
  tmp = pygame.transform.scale(tmp, (p_w,p_h))
  rect_player = tmp.get_rect()
  rect_player.center = (w/2, h/2)
  player = {"img":tmp, "rect": rect_player, "width": p_w, "height": p_h, "HP":3}

  # bullet
  (b_w,b_h) = (10,10)
  bullet_img = pygame.image.load("./bullet.png").convert_alpha()
  bullet_img = pygame.transform.scale(bullet_img, (b_w, b_h))

  # enemy
  (e_w,e_h) = (50,50)
  enemy_img = pygame.image.load("./enemy.png").convert_alpha()
  enemy_img = pygame.transform.scale(enemy_img, (e_w, e_h))
    
  while (1):
    pygame.display.update()             # 画面更新
    pygame.time.wait(30)                # 更新時間間隔
    screen.fill((0, 20, 0, 0))          # 画面の背景色
    fps += 1

    for event in pygame.event.get():
      if event.type == QUIT:          # 閉じるボタンが押されたとき
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN:       # キーを押したとき
        print(event.key)
        if event.key == K_ESCAPE:   # Escキーが押されたとき
          pygame.quit()
          sys.exit()
        if event.key == 32 and len(bulleds) < BULLED_MAX_LENGTH:
          bulleds.append(bullet_img.get_rect())
          bulleds[len(bulleds) - 1].center = (player["rect"].x + (player["width"] / 2), player["rect"].y + 10)

    if(player["HP"] < 1):
      Text = myfont.render("GameOver", False, (255, 255, 255))
      screen.blit(Text,(0, 0))
      continue

    pressed_key = pygame.key.get_pressed()
    rect = player["rect"]
    if pressed_key[K_LEFT] and rect.x > 0:
      rect.move_ip(-3, 0)
    if pressed_key[K_RIGHT] and rect.x < (w - player["width"]):
      rect.move_ip(3, 0)
    if pressed_key[K_UP] and rect.y > 0:
      rect.move_ip(0, -3)
    if pressed_key[K_DOWN] and rect.y < (h - player["height"]):
      rect.move_ip(0, 3)
    
    # 時間ごとにscoreをプラス
    if(fps % 6 == 0):
      score += 1
    
    # enemy の sporn
    if(fps % 10 == 0 and len(enemys) < 10):
      sporn_x = randint(0, (h - 50))
      sporn_y = 5
      enemys.append(enemy_img.get_rect())
      enemys[len(enemys) - 1].center = (sporn_x, sporn_y)
    
    # enemyの行動パターン
    enemy_pattern = [[0,4],[1,3],[-1,3],[-2,2],[1,3],[1,6],[-1,6],[1,1],[0,1],[0,5]]

    screen.blit(player["img"], player["rect"])    # プレイヤー画像の描画

    # 球の絵画
    for i in range(len(bulleds)):
      bulleds[i].move_ip(0, -4)
      screen.blit(bullet_img, bulleds[i])
    for i in range(len(bulleds)):
      if(bulleds[i].y < 1):
        bulleds.pop(i)
        break
    # enemyの絵画
    for i in range(len(enemys)):
      enemys[i].move_ip(enemy_pattern[i][0],enemy_pattern[i][1])
      screen.blit(enemy_img, enemys[i])
    for i in range(len(enemys)):
      if(enemys[i].y > h):
        enemys.pop(i)
        break

    # テキストの絵画
    scoreText = myfont.render('score: ' + str(score), False, (255, 255, 255)) # スコア "HP: " + str(player["HP"]
    HPBar = ""
    for i in range(player["HP"]):
      HPBar += "O"
    HPText = myfont.render("HP: " + HPBar, False, (255, 255, 255))
    screen.blit(scoreText,(0, 0))
    screen.blit(HPText, (0, 30))

    # 当たり判定
    flag = 0
    for i in range(len(enemys)):
      if(enemys[i].y + e_h >= player["rect"].y and enemys[i].y <= player["rect"].y + player["width"]):
          if(enemys[i].x + e_h >= player["rect"].x and enemys[i].x <= player["rect"].x + player["height"]):
            player["HP"] -= 1
            enemys.pop(i)
            break
      for l in range(len(bulleds)):
        if(enemys[i].y + e_h >= bulleds[l].y and enemys[i].y <= bulleds[l].y + b_h):
          if(enemys[i].x + e_h >= bulleds[l].x and enemys[i].x <= bulleds[l].x + b_w):
            enemys.pop(i)
            bulleds.pop(l)
            flag = 1
            score -= 10
            break
      if(flag == 1):
        flag == 0
        break
                
if __name__ == "__main__":
  main()