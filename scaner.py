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
    counts_arr[0][2] += 5
    counts_arr[-1][2] += 10
    #if( len(counts_arr) > 10):
    #    sort_arr = sort_arr[:10]
    #sort_arr = sorted(counts_arr, key = lambda x : x[2], reverse = True)
    #sort_arr = sort_arr[:10]
    #top_n = sorted(sort_arr, key = lambda x : x[0] )
    extract_color = []
    for c in counts_arr :
        num = 0
        dif = 0
        clr = c[1]
        if(c[1] == 1):
            clr = 0
        elif(c[1] == 6):
            clr = 1
            dif = 10
        if( c[2] > 415):
            num = 8
        elif( c[2] > 355):
            num = 7
        elif( c[2] > 295):
            num = 6
        elif( c[2] > 240):
            num = 5
        elif( c[2] > 190 + dif):
            num = 4
        elif( c[2] > 135 + dif / 2):
            num = 3
        elif( c[2] > 75):
            num = 2
        elif( c[2] > 20):
            num = 1
        for i in range(num):
            extract_color.append(clr)
    #print(extract_color)
    #if(len(extract_color) != 10):
    #print("some thing wrong : ",counts_arr)
    return extract_color


ev3.Sound.beep()

rightmotor = ev3.LargeMotor('outA')
leftmotor = ev3.LargeMotor('outD')
colormotor = ev3.MediumMotor('outB')

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
                    rightmotor.run_to_rel_pos(position_sp = 62, speed_sp = sp)
                    leftmotor.run_to_rel_pos(position_sp = 62, speed_sp = sp)
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
                colormotor.run_to_rel_pos(position_sp = color_sp, speed_sp = 50)
        else:
            if(right_touch_ss.is_pressed == 1):
                color_sp = 45
                colormotor.stop()
                if(not Start):
                    rightmotor.run_to_rel_pos(position_sp = 62, speed_sp = sp)
                    leftmotor.run_to_rel_pos(position_sp = 62, speed_sp = sp)
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
                colormotor.run_to_rel_pos(position_sp = color_sp, speed_sp = 50)
        row_colors.append(cs.color)
        #rightmotor.run_to_rel_pos(position_sp = 1080, speed_sp = sp)
        #leftmotor.run_to_rel_pos(position_sp = 1080, speed_sp = sp)
    except :
        rightmotor.stop()
        leftmotor.stop()
        colormotor.stop()
        break
ev3.Sound.beep()




#for i in range(10):
for j in range(10):
    # i : x, j : y
    if(color_map[0][j] == 3 ) :
        strt_x = 0
        strt_y = j
        color_map[0][j] = 1
        break
for j in range(10):
    if(color_map[9][j] == 5):
        dst_x = 9
        dst_y = j
        color_map[9][j] = 1
        break

check = weight(color_map)
OrderList = MakeOrder(check)
print("minimum distance")
for i in range(N):
    for j in range(M):
        print('{0:^2d}'.format(check[i][j]), end = ",")
    print()

print("Order list")
print(OrderList)

time.sleep(5)
ev3.Sound.beep()

cur = (0,0)
for tmp in OrderList:
    term = 0
    if(cur[1] - tmp[1] != 0):
        if(cur[1] > tmp[1]):
            term = cur[1] - tmp[1] # left
            for i in range(term):
                colormotor.run_to_rel_pos(position_sp = 48 , speed_sp = 45 )
                time.sleep(3)
                colormotor.stop()
        else:
            term = tmp[1] - cur[1]
            for i in range(term):
                colormotor.run_to_rel_pos(position_sp = -48, speed_sp = 45 )
                time.sleep(3)
                colormotor.stop()
    else:
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