import ev3dev.ev3 as ev3
import time
import queue
# x axis length
N = 10
# y axis length
M = 10

strt_x = 0
strt_y = 4

dst_x = 2
dst_y = 1

dir = [[1,0], [0,1], [-1,0], [0,-1]]

def weight(arr):
    #arr = [[1,1,0,1,1],[1,1,1,1,1],[0,1,0,1,1]]
    q = queue.Queue()
    check = [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]]
    check[strt_x][strt_y] = 1
    q.put((strt_x, strt_y))
    while (q.qsize() != 0):
        x = q.queue[0][0]
        y = q.queue[0][1]
        q.get()
        for i in range(4):
            xx = x + dir[i][0]
            yy = y + dir[i][1]
            if(xx < 0 or xx >= N or yy < 0 or yy >= M):
                continue
            if(arr[xx][yy] == 0 or check[xx][yy] != -1):
                continue

            check[xx][yy] = check[x][y] + 1

            q.put((xx,yy))
    return check

def MakeOrder(check):
    stack = []
    order = []
    check[strt_x][strt_y] = 1
    stack.append((strt_x, strt_y))

    do_nothing = False
    while(len(stack) != 0):
        x = stack[-1][0]
        y = stack[-1][1]
        p = stack.pop()
        if(do_nothing):
            boundary_answer = check[p[0]][p[1]]
            boundary = order.pop()
            while(check[boundary[0]][boundary[1]] > boundary_answer):
                boundary = order.pop()
        order.append(p)

        do_nothing = True
        for i in range(4):
            xx = x + dir[i][0]
            yy = y + dir[i][1]
            if(xx < 0 or xx >= N or yy < 0 or yy >= M):
                continue
            if(check[xx][yy] == -1):
                continue
            if(check[xx][yy] == check[x][y] + 1):
                if(check[xx][yy] == check[dst_x][dst_y] and xx != dst_x and yy != dst_y ):
                    continue
                if((xx,yy) == (dst_x, dst_y)):
                    order.append((xx,yy))
                    return order
                stack.append((xx,yy))
                do_nothing = False
    return order

def decision_color(row):
    idx = 0
    count = 0
    counts_arr = []
    for c in row:
        if(len(counts_arr) > 0):
            if(counts_arr[-1][1] == c):
                counts_arr[-1][2] += 1
            else :
                counts_arr.append([idx,c,0])
                idx +=1
        else:
            counts_arr.append([idx,c,0])
            idx += 1
    counts_arr[0][2] -= 10
    #counts_arr[-1][2] += 5
    #if( len(counts_arr) > 10):
    #    sort_arr = sort_arr[:10]
    #sort_arr = sorted(counts_arr, key = lambda x : x[2], reverse = True)
    #sort_arr = sort_arr[:10]
    #top_n = sorted(sort_arr, key = lambda x : x[0] )
    extract_color = []
    diff_small_value = []
    diff_big_value = []
    corrected_idx = []
    print(counts_arr)
    for i in range(2):
        #extract_color = []
        #diff_small_value = []
        if( i == 1):
            if(len(extract_color) == 10):
                break
            elif(len(extract_color) < 10):
                counts_arr[ corrected_idx [ diff_small_value.index(min(diff_small_value))] ][2] += (min(diff_small_value) + 2)
                print(diff_small_value)
            else:
                counts_arr[ corrected_idx [ diff_big_value.index(min(diff_big_value)) ]][2] -= (min(diff_big_value) +2)
                print(diff_big_value)
            print("fix .. original : ", extract_color)
            print(counts_arr)
            extract_color = []
            diff_small_value = []
            diff_big_value = []
            corrected_idx = []
        for c in range(len(counts_arr)) :
            num = 0
            dif = 0
            clr = -1
            if(counts_arr[c][1] == 1):
                clr = 0
                dif = -5
            elif(counts_arr[c][1] == 6):
                clr = 1
                dif = 5
            elif(counts_arr[c][1] == 3 or counts_arr[c][1] == 5):
                clr = counts_arr[c][1]
            else:
                continue
            if( counts_arr[c][2] > 530):
                num = 10
                diff_small_value.append(100)
                diff_big_value.append(counts_arr[c][2] - 530)
            elif(counts_arr[c][2] > 460):
                num = 9
                diff_small_value.append(530 - counts_arr[c][2])
                diff_big_value.append(counts_arr[c][2] - 460)
            elif( counts_arr[c][2] > 390):
                num = 8
                diff_small_value.append(460 - counts_arr[c][2])
                diff_big_value.append(counts_arr[c][2] - 390)
            elif( counts_arr[c][2] > 340):
                num = 7
                diff_small_value.append(390 - counts_arr[c][2])
                diff_big_value.append(counts_arr[c][2] - 340)
            elif( counts_arr[c][2] > 280):
                num = 6
                diff_small_value.append(340 - counts_arr[c][2])
                diff_big_value.append(counts_arr[c][2] - 280)
            elif( counts_arr[c][2] > 220):
                num = 5
                diff_small_value.append(280 - counts_arr[c][2])
                diff_big_value.append(counts_arr[c][2] - 220)
            elif( counts_arr[c][2] > 180 + dif):
                num = 4
                diff_small_value.append(220 - counts_arr[c][2])
                diff_big_value.append(counts_arr[c][2] + dif - 180)
            elif( counts_arr[c][2] > 120 + dif):
                num = 3
                diff_small_value.append(180 + dif - counts_arr[c][2])
                diff_big_value.append(counts_arr[c][2] - dif - 120 )
            elif( counts_arr[c][2] > 70 + dif):
                num = 2
                diff_small_value.append(120 +dif - counts_arr[c][2])
                diff_big_value.append(counts_arr[c][2] - dif - 70)
            elif( counts_arr[c][2] > 15):
                num = 1
                diff_small_value.append(70 + dif - counts_arr[c][2])
                diff_big_value.append(counts_arr[c][2] - 15)
            else:
                continue
            corrected_idx.append(c)
            for i in range(num):
                extract_color.append(clr)
    #print(counts_arr)
    #if(len(extract_color) < 10):
    #   print("some thing wrong : ",counts_arr)
    return extract_color


ev3.Sound.beep()

rightmotor = ev3.LargeMotor('outA')
leftmotor = ev3.LargeMotor('outD')
#colormotor = ev3.MediumMotor('outB')
colormotor = ev3.LargeMotor('outB')
cs_sp = 40
sp = 50
flag = 300
visit_green = False
left_touch_ss = ev3.TouchSensor(ev3.INPUT_4)
right_touch_ss = ev3.TouchSensor(ev3.INPUT_1)
cs = ev3.ColorSensor()
color_sp = 70 # positive : left , negative : right
row_colors = []

color_map = []
Start = True

while(True):
    try:
        #print(left_touch_ss.is_pressed, right_touch_ss.is_pressed)
        if(len(color_map) == 10) :
            break
        if(color_sp >0):
            if(left_touch_ss.is_pressed == 1):
                color_sp = -45
                colormotor.stop()
                if(not Start):
                    rightmotor.run_to_rel_pos(position_sp = 63, speed_sp = sp)
                    leftmotor.run_to_rel_pos(position_sp = 63, speed_sp = sp)
                    r = decision_color(row_colors[:])
                    r.reverse()
                    print(r)
                    color_map.append(r)
                else:
                    Start = False
                row_colors = []
                time.sleep(3)
                rightmotor.stop()
                leftmotor.stop()
            else:
                colormotor.run_to_rel_pos(position_sp = color_sp, speed_sp = cs_sp)
        else:
            if(right_touch_ss.is_pressed == 1):
                color_sp = 45
                colormotor.stop()
                if(not Start):
                    rightmotor.run_to_rel_pos(position_sp = 63, speed_sp = sp)
                    leftmotor.run_to_rel_pos(position_sp = 63, speed_sp = sp)
                    r = decision_color(row_colors[:])
                    print(r)
                    color_map.append(r)
                else :
                    Start = False
                row_colors = []
                time.sleep(3)
                rightmotor.stop()
                leftmotor.stop()
            else:
                colormotor.run_to_rel_pos(position_sp = color_sp, speed_sp = cs_sp)
        row_colors.append(cs.color)
        #rightmotor.run_to_rel_pos(position_sp = 1080, speed_sp = sp)
        #leftmotor.run_to_rel_pos(position_sp = 1080, speed_sp = sp)
    except:
        #print(e)
        rightmotor.stop()
        leftmotor.stop()
        colormotor.stop()
        break
ev3.Sound.beep()


mv_sp = 45

#for i in range(10):
for i in range(M):
    for j in range(N):
        if(color_map[i][j] == 5):
            dst_x = i
            dst_y = j
            color_map[i][j] = 1
        elif(color_map[i][j] == 3):
            strt_x = i
            strt_y = j
            color_map[i][j] = 1

check = weight(color_map)
OrderList = MakeOrder(check)
print("minimum distance")
for i in range(N):
    for j in range(M):
        print('{0:^2d}'.format(check[i][j]), end = ",")
    print()

print("Order list")
print(OrderList)
leftmotor.run_to_rel_pos(position_sp = -640, speed_sp = sp)
rightmotor.run_to_rel_pos(position_sp = -640, speed_sp = sp)
time.sleep(18)
rightmotor.stop()
leftmotor.stop()
ev3.Sound.beep()

cur = (0,0)
for tmp in OrderList:
    term = 0
    print("current idx : ",cur)
    if(cur[1] - tmp[1] != 0):
        if(cur[1] > tmp[1]):
            term = cur[1] - tmp[1] # left
            for i in range(term):
                colormotor.run_to_rel_pos(position_sp = 56 , speed_sp = mv_sp )
                time.sleep(3)
                colormotor.stop()
        else:
            term = tmp[1] - cur[1]
            for i in range(term):
                colormotor.run_to_rel_pos(position_sp = -56, speed_sp = mv_sp )
                time.sleep(3)
                colormotor.stop()
    if(cur[0] - tmp[0] != 0):
        if(cur[0] > tmp[0]):
            term = cur[0] - tmp[0]
            for i in range(term):
                leftmotor.run_to_rel_pos(position_sp = -62, speed_sp = sp)
                rightmotor.run_to_rel_pos(position_sp = -62, speed_sp = sp)
                time.sleep(3)
                leftmotor.stop()
                rightmotor.stop()
        else:
            term = tmp[0] - cur[0]
            for i in range(term):
                leftmotor.run_to_rel_pos(position_sp = 62, speed_sp = sp)
                rightmotor.run_to_rel_pos(position_sp = 62, speed_sp = sp)
                time.sleep(3)
                leftmotor.stop()
                rightmotor.stop()
    cur = tmp