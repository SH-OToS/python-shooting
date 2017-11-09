# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
from random import randint
import os

def main():
    (w,h) = (400,400)   # 画面サイズ
    pygame.init()       # pygame初期化
    pygame.font.init()  # テキストを出すやつ
    myfont = pygame.font.SysFont('Comic Sans MS', 30) # set font
    screen = pygame.display.set_mode((w, h), 0)  # 画面設定
    fps = 0
    BULLED_MAX_LENGTH = 10
    ENEMY_MAX_LENGTH = 10
    score = 0
    enemys = []
    bulleds = []
    effect = []
    first = True
    stop = False

    # player
    (p_w,p_h) = (20,50)
    print(os.path.abspath("."))
    tmp = pygame.image.load(os.path.join(os.path.abspath("."), "home.png")).convert_alpha()
    tmp = pygame.transform.scale(tmp, (p_w,p_h))
    rect_player = tmp.get_rect()
    rect_player.center = (w/2, h/2)
    player = {"img":tmp, "rect": rect_player, "width": p_w, "height": p_h, "HP":0, "speed": 3}

    # background
    background_img = pygame.image.load(os.path.join(os.path.abspath("."),"background.jpg"))
    background_img = pygame.transform.scale(background_img, (w, h))

    # bullet
    (b_w,b_h) = (10,10)
    bullet_img = pygame.image.load(os.path.join(os.path.abspath("."),"./bullet.png")).convert_alpha()
    bullet_img = pygame.transform.scale(bullet_img, (b_w, b_h))

    # enemy
    (e_w,e_h) = (50,50)
    enemy_img = pygame.image.load(os.path.join(os.path.abspath("."),"./bullet.png")).convert_alpha()
    enemy_img = pygame.transform.scale(enemy_img, (e_w, e_h))
    enemy_pattern = []

    # Hit effect
    (h_w, h_h) = (50, 50)
    hit_img = pygame.image.load(os.path.join(os.path.abspath("."),"./explosion.png")).convert_alpha()
    hit_img = pygame.transform.scale(hit_img, (h_w, h_h))

        
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
                if event.key == 115 and player["HP"] < 1:
                    enemys = []
                    bulleds = []
                    effect = []
                    player["rect"].x = w / 2 - player["width"] / 2
                    player["rect"].y = h / 2 - player["height"] / 2
                    score = 0
                    player["HP"] = 3
                if event.key == 112:
                    stop = not stop
                    if(stop):
                        player["speed"] = 0
                    else:
                        player["speed"] = 3

        if(player["HP"] < 1):
            if(first == False):
                Text1 = myfont.render("GameOver         Score: " + str(score), False, (255, 255, 255))
                screen.blit(Text1,(0, 30))
            Text2 = myfont.render("start: S", False, (255, 255, 255))
            Text3 = myfont.render("finish: esc", False, (255, 255, 255))
            screen.blit(Text2,(0, 100))
            screen.blit(Text3,(0, 150))
            continue

        first = False
        pressed_key = pygame.key.get_pressed()
        rect = player["rect"]
        if pressed_key[K_LEFT] and rect.x > 0:
            rect.move_ip(-(player["speed"]), 0)
        if pressed_key[K_RIGHT] and rect.x < (w - player["width"]):
            rect.move_ip((player["speed"]), 0)
        if pressed_key[K_UP] and rect.y > 0:
            rect.move_ip(0, -(player["speed"]))
        if pressed_key[K_DOWN] and rect.y < (h - player["height"]):
            rect.move_ip(0, (player["speed"]))
        
        # 時間ごとにscoreをプラス
        if(fps % 6 == 0 and not stop):
            score += 1
        
        # 背景の描画
        screen.blit(background_img, (0,0))
        
        # 爆発の描画
        for i in range(len(effect)):
            if(stop):
                effect[i][1] += 1
            size = fps - effect[i][1] + 50
            screen.blit(pygame.transform.scale(hit_img, (size, size)), effect[i][0])
        
        # プレイヤー画像の描画
        screen.blit(player["img"], player["rect"])

        # 球の描画
        for i in range(len(bulleds)):
            screen.blit(bullet_img, bulleds[i])
        
        # enemyの描画
        for i in range(len(enemys)):
            screen.blit(enemy_img, enemys[i])
        
        # テキストの描画
        scoreText = myfont.render('score: ' + str(score), False, (255, 255, 255)) # スコア "HP: " + str(player["HP"]
        HPBar = ""
        for i in range(player["HP"]):
            HPBar += "O"
        HPText = myfont.render("HP: " + HPBar, False, (255, 255, 255))
        screen.blit(scoreText,(0, 0))
        screen.blit(HPText, (0, 30))

        if(stop == True):
            continue
        
        # enemy の sporn
        while(len(enemy_pattern) < ENEMY_MAX_LENGTH):
            enemy_pattern.append([randint(-3,3), randint(2, 5)])
        ENEMY_MAX_LENGTH = score / 20 + 5
        if(fps % 10 == 0 and len(enemys) < ENEMY_MAX_LENGTH):
            sporn_x = randint(0, (h - 50))
            sporn_y = 5
            enemys.append(enemy_img.get_rect())
            enemys[len(enemys) - 1].center = (sporn_x, sporn_y)

        #爆発の移動、削除
        for i in range(len(effect)):
            size = fps - effect[i][1] + 50
            if(size > 100):
                effect[i][0].move_ip(1, 1)
            if(effect[i][0].x > w + 10):
                effect.pop(i)
                break

        # 弾の移動、削除
        for i in range(len(bulleds)):
            bulleds[i].move_ip(0, -4)
            if(bulleds[i].y < 1):
                bulleds.pop(i)
                break
        
        #enemyの移動、削除
        for i in range(len(enemys)):
            enemys[i].move_ip(enemy_pattern[i][0],enemy_pattern[i][1])
            if(enemys[i].y > h):
                enemys.pop(i)
                break

        # 当たり判定
        flag = 0
        for i in range(len(enemys)):
            if(enemys[i].y + e_h >= player["rect"].y and enemys[i].y <= player["rect"].y + player["height"]):
              if(enemys[i].x + e_w >= player["rect"].x and enemys[i].x <= player["rect"].x + player["width"]):
                player["HP"] -= 1
                effect.append([hit_img.get_rect(), fps])
                effect[-1][0].center = (enemys[i].x + e_w / 2, player["rect"].y + e_h / 2)
                enemys.pop(i)
                break
        for l in range(len(bulleds)):
            if(enemys[i].y + e_h >= bulleds[l].y and enemys[i].y <= bulleds[l].y + b_h):
                if(enemys[i].x + e_w >= bulleds[l].x and enemys[i].x <= bulleds[l].x + b_w):
                    effect.append([hit_img.get_rect(), fps])
                    effect[-1][0].center = (bulleds[l].x, bulleds[l].y)
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
