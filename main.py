#載入模組
import pygame
import time

#初始化pygame模組
pygame.init()

#設定視窗物件
wn = pygame.display.set_mode((800, 600))

#全域變數
running = True #操縱遊戲迴圈是否繼續
mouse = "" #記錄滑鼠目前是否被按下
loop_start_time = 0 #迴圈開始時間
start_time = 0 #遊戲開始時間
time_pass = 0  #遊戲經過多久
started = 0 #操縱遊戲是否已開始
drop_before_arrive = 0.8 #音符到達判定線前多少秒要出現
pixel_per_second = 565 / drop_before_arrive #音符每秒要跑幾單位距離
showing_array = []
pointer = 0
result_combo = 0
result_score = 0
result_perfect = 0
result_good = 0
result_miss = 0

#載入圖片
note = pygame.image.load("images\\note.png").convert_alpha()
note2 = pygame.image.load("images\\note2.png").convert_alpha()
start_menu = pygame.image.load("images\start_window.png").convert_alpha()
start_button = pygame.image.load("images\start_button.png").convert_alpha()
result_bg = pygame.image.load("images\\result_window.png").convert_alpha()
cover = pygame.image.load("images\\idol.jpg").convert_alpha()
j_perfect = pygame.image.load("images\\perfect.png").convert_alpha()
j_good = pygame.image.load("images\\good.png").convert_alpha()
j_miss = pygame.image.load("images\\miss.png").convert_alpha()

#調整圖片
note = pygame.transform.scale(note, (80, 20))
note2 = pygame.transform.scale(note2, (80, 40))
Notes = (note, note2)
start_menu = pygame.transform.scale(start_menu, (800, 600))
start_button = pygame.transform.scale(start_button, (400, 200))
result_bg = pygame.transform.scale(result_bg, (800, 600))
cover = pygame.transform.scale(cover, (275, 275))
j_perfect = pygame.transform.scale(j_perfect, (120, 40))
j_good = pygame.transform.scale(j_good, (120, 40))
j_miss = pygame.transform.scale(j_miss, (120, 40))
juty = (j_miss, j_perfect, j_good)

#載入音樂
music_location = "images\\idol.mp3"
track = pygame.mixer.music.load(music_location)

#字型設定
font = pygame.font.Font("freesansbold.ttf", 32)

#圖形定義
bg_back = pygame.Rect(0, 0, 800, 600)
border_left_line = pygame.Rect(150, 0, 10, 600)
border_right_line = pygame.Rect(640, 0, 10, 600)
display_p10 = pygame.Rect(160, 500, 80, 30)
display_p11 = pygame.Rect(160, 490, 80, 10)
display_p20 = pygame.Rect(240, 500, 80, 30)
display_p21 = pygame.Rect(240, 490, 80, 10)
display_p30 = pygame.Rect(320, 500, 80, 30)
display_p31 = pygame.Rect(320, 490, 80, 10)
display_p40 = pygame.Rect(400, 500, 80, 30)
display_p41 = pygame.Rect(400, 490, 80, 10)
display_p50 = pygame.Rect(480, 500, 80, 30)
display_p51 = pygame.Rect(480, 490, 80, 10)
display_p60 = pygame.Rect(560, 500, 80, 30)
display_p61 = pygame.Rect(560, 490, 80, 10)

#讀取檔案
times_arrive = []
times_drop = []
notes = []
note_types = []

with open(f"notes_and_time\\times.txt", "r") as time_f:
    for i in time_f:
        i = int(i)
        i /= 1000
        i = round(i, 4)
        times_arrive.append(i)

with open(f"notes_and_time\\notes.txt", "r") as note_f:
    for i in note_f:
        i = int(i)
        notes.append(i)

with open(f"notes_and_time\\types.txt", "r") as types_f:
    for i in types_f:
        i = int(i)
        note_types.append(i)

for i in times_arrive:
    i -= drop_before_arrive
    i = round(i, 4)
    times_drop.append(i)

#音符
class Note():
    def __init__(self, drop_time, arrive_time, xcor, ycor, block, noty, order):
        self.drop_time = drop_time
        self.arrive_time = arrive_time
        self.xcor = xcor
        self.ycor = ycor
        self.block = block
        self.noty = noty
        self.order = order
        self.hit = 0
        self.show = True

    def ycor_update(self, time_pass):
        p = time_pass - self.drop_time
        self.ycor += pixel_per_second * p - (self.ycor + 60)

    def check(self, time_pass):
        block_check = keys[self.block]
        time_check = abs(self.arrive_time - time_pass) <= 0.2
        if block_check and time_check:
            if abs(self.arrive_time - time_pass) <= 0.1:
                return 1
            elif abs(self.arrive_time - time_pass) <= 0.2:
                return 2
            else:
                return 0
        return 0

#譜面
def showingArray_appending(time_pass):
    global showing_array
    global pointer
    global started
    cor_location = [160, 240, 320, 400, 480, 560]
    cor_key0 = {0: pygame.K_s, 1: pygame.K_d, 2: pygame.K_f, 3: pygame.K_j, 4: pygame.K_k, 5: pygame.K_l}
    cor_key1 = {0: pygame.K_w, 1: pygame.K_e, 2: pygame.K_r, 3: pygame.K_u, 4: pygame.K_i, 5: pygame.K_o}
    cor_key = (cor_key0, cor_key1)
    while pointer < len(times_drop) and abs(time_pass - times_drop[pointer]) <= 0.1:
        one_note = Note(times_drop[pointer], times_arrive[pointer], cor_location[notes[pointer]], -100, cor_key[note_types[pointer]][notes[pointer]], note_types[pointer], pointer)
        showing_array.append(one_note)
        pointer += 1

#顯示音符
def note_displaying(time_pass):
    global showing_array
    for one_note in showing_array:
        if one_note.show:
            one_note.ycor_update(time_pass)
            wn.blit(Notes[one_note.noty], (one_note.xcor, one_note.ycor))
        if one_note.ycor >= 600:
            one_note.show = False

#消去音符
def note_remove(time_pass):
    for one_note in showing_array:
        if  one_note.check(time_pass) != 0:
            one_note.hit = one_note.check(time_pass)
            one_note.show = False

#事件
def pygame_events():
    global running
    global mouse
    global started
    for event in pygame.event.get(): #取得目前事件
        if event.type == pygame.QUIT: #「按下退出鍵」事件發生
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN: #「按下滑鼠」事件發生
            mouse = 'down'
        if event.type != pygame.MOUSEBUTTONDOWN: #「按下滑鼠」事件未發生
            mouse = ''
    if started == 1:
        if not pygame.mixer.music.get_busy():
            started = 2

#顯示初始背景
def bg_display():
    global started
    global start_time
    if started  == 0:
        wn.blit(start_menu, (0, 0)) #顯示初始背景
        wn.blit(start_button, (200, 300)) #顯示開始按鈕
        if mouse == 'down':
            started = 1 #宣告遊戲開始
            start_time = time.time() #設定開始的時間
            pygame.mixer.music.play() #開始播放音樂
    elif started == 1:
        draw_bg() #繪製遊戲畫面
    else:
        wn.blit(result_bg, (0, 0)) #顯示結束背景
        draw_bg()

#繪製遊戲畫面
def draw_bg():
    global started
    global result_combo
    global result_score
    global result_perfect
    global result_good
    global result_miss
    if started == 1:
        pygame.draw.rect(wn, (0, 0, 0), bg_back)
        pygame.draw.rect(wn, (255, 255, 255), border_left_line)
        pygame.draw.rect(wn, (255, 255, 255), border_right_line)

        pygame.draw.line(wn, (255, 255, 255), (240, 0),(240, 600))
        pygame.draw.line(wn, (255, 255, 255), (320, 0),(320, 600))
        pygame.draw.line(wn, (255, 255, 255), (400, 0),(400, 600))
        pygame.draw.line(wn, (255, 255, 255), (480, 0),(480, 600))
        pygame.draw.line(wn, (255, 255, 255), (560, 0),(560, 600))

        pygame.draw.line(wn, (100, 100, 100), (160, 500),(640, 500))
        pygame.draw.line(wn, (100, 100, 100), (160, 530),(640, 530))

        wn.blit(font.render(f"S", True, (130, 130, 130)), (190, 540))
        wn.blit(font.render(f"D", True, (130, 130, 130)), (270, 540))
        wn.blit(font.render(f"F", True, (130, 130, 130)), (350, 540))
        wn.blit(font.render(f"J", True, (130, 130, 130)), (430, 540))
        wn.blit(font.render(f"K", True, (130, 130, 130)), (510, 540))
        wn.blit(font.render(f"L", True, (130, 130, 130)), (590, 540))
        wn.blit(font.render(f"W", True, (255, 100, 200)), (190, 460))
        wn.blit(font.render(f"E", True, (255, 100, 200)), (270, 460))
        wn.blit(font.render(f"R", True, (255, 100, 200)), (350, 460))
        wn.blit(font.render(f"U", True, (255, 100, 200)), (430, 460))
        wn.blit(font.render(f"I", True, (255, 100, 200)), (510, 460))
        wn.blit(font.render(f"O", True, (255, 100, 200)), (590, 460))
    elif started == 2:
        wn.blit(cover, (80, 50)) 
        wn.blit(font.render(f"{result_score}", True, (0, 0, 0)), (400, 80))
        wn.blit(font.render(f"{result_combo}", True, (0, 0, 0)), (400, 160))
        wn.blit(font.render(f"{result_perfect}", True, (0, 0, 0)), (400, 240))
        wn.blit(font.render(f"{result_good}", True, (0, 0, 0)), (520, 240))
        wn.blit(font.render(f"{result_miss}", True, (0, 0, 0)), (650, 240))

#繪製按鍵效果
def draw_press():
    if started == 1:
        if keys[pygame.K_s]:
            pygame.draw.rect(wn, (130, 130, 130), display_p10)
        if keys[pygame.K_d]:
            pygame.draw.rect(wn, (130, 130, 130), display_p20)
        if keys[pygame.K_f]:
            pygame.draw.rect(wn, (130, 130, 130), display_p30)
        if keys[pygame.K_j]:
            pygame.draw.rect(wn, (130, 130, 130), display_p40)
        if keys[pygame.K_k]:
            pygame.draw.rect(wn, (130, 130, 130), display_p50)
        if keys[pygame.K_l]:
            pygame.draw.rect(wn, (130, 130, 130), display_p60)
        if keys[pygame.K_w]:
            pygame.draw.rect(wn, (255, 100, 200), display_p11)
        if keys[pygame.K_e]:
            pygame.draw.rect(wn, (255, 100, 200), display_p21)
        if keys[pygame.K_r]:
            pygame.draw.rect(wn, (255, 100, 200), display_p31)
        if keys[pygame.K_u]:
            pygame.draw.rect(wn, (255, 100, 200), display_p41)
        if keys[pygame.K_i]:
            pygame.draw.rect(wn, (255, 100, 200), display_p51)
        if keys[pygame.K_o]:
            pygame.draw.rect(wn, (255, 100, 200), display_p61)

#初始時間設定
def pre_time_handle():
    global loop_start_time
    global start_time
    global time_pass
    loop_start_time = time.time() #定義迴圈開始時間
    if started != 1:
        start_time = loop_start_time
    time_pass = float(loop_start_time - start_time) #目前距離遊戲開始經歷多久
    time_pass = round(time_pass, 4) #四捨五入到小數點第四位

#過程時間設定
def post_time_handle(loop_start_time):
    now_end_time = time.time() #定義迴圈結束時間
    now_end_time = round(now_end_time, 4) #四捨五入到小數點第四位
    loop_time = now_end_time - loop_start_time #計算迴圈執行時間
    if loop_time < 0.001:
        time.sleep(0.001 - loop_time) #若迴圈執行時間少於0.001秒則等待

#判定
def judge():
    combo = 0
    score = 0
    perfect = 0
    good = 0
    miss = 0
    combo_max = 0
    combo_color = (238, 130, 238)
    note_died_count = 0
    global result_score
    global result_combo
    global result_perfect
    global result_good
    global result_miss
    judge_array = []
    for one_note in showing_array:
        if one_note.arrive_time < time_pass:
            note_died_count += 1
    for i in range(note_died_count):
        if showing_array[i].hit != 0:
            combo += 1
            if showing_array[i].hit == 1:
                judge_array.append(1)
                perfect += 1
                score += 3
            elif showing_array[i].hit == 2:
                judge_array.append(2)
                good += 1
                score += 1
            if combo > combo_max:
                combo_max = combo
        else:
            combo = 0
            judge_array.append(0)
            miss += 1
            combo_color = (255, 255, 255)
    # show combo and score
    if started == 1:
        combo_show1 = font.render(f"COMBO", True, combo_color)
        combo_show2 = font.render(f"{combo}", True, combo_color)
        wn.blit(combo_show1, (10, 280))
        wn.blit(combo_show2, (50, 320))
        score_show1 = font.render(f"SCORE", True, combo_color)
        score_show2 = font.render(f"{score}", True, combo_color)
        wn.blit(score_show1, (680, 280))
        wn.blit(score_show2, (720, 320))
        result_score = score
        result_combo = combo_max
        result_perfect = perfect
        result_good = good
        result_miss = miss
        if len(judge_array) != 0 and len(judge_array) == note_died_count:
            if showing_array[-1].arrive_time - time_pass  <= -0.001:
                wn.blit(juty[judge_array[-1]],(340, 400))

#主程式
while running:
    pre_time_handle()
    keys = pygame.key.get_pressed() #取得鍵盤上哪些按鍵被按下
    pygame_events()
    bg_display()
    draw_press()
    note_remove(time_pass)
    showingArray_appending(time_pass)
    note_displaying(time_pass)
    judge()
    pygame.display.update() #更新視窗
    post_time_handle(loop_start_time)