
import ev3dev.ev3 as ev3
import time
#ev3.Sound.beep()

row_motor = ev3.LargeMotor('outA')
col_motor = ev3.LargeMotor('outD')
r_sp = 45
p_sp = 1080
# positive : right, negative : left
color_sensor = ev3.ColorSensor()
row_count = 0
right_max = 289
left_max = 292
row_max = 0
col_max = 122
col_count = 0
diff_row = [-1,0,0,0,0,0,0,0,0,0]
diff_col = [0,0,0,0,0,0,0,0,0,0]
start = True
try:
    for row in range(10):
        if(not start):
            while(col_count < col_max):
                col_motor.run_to_rel_pos(position_sp = -1080, speed_sp = 100)
                col_count +=1
            col_count = 0
            col_motor.stop()
        else:
            start = False
        try_counts = 0
        frequency = [0,0,0,0,0,0,0,0,0,0]
        tries = []
        while (True):
            tries = []
            for t in range(2):
                try_row = []
                for col in range(10):
                    cs = color_sensor.color
                    # check frequency
                    if(row == 0) :
                        if(cs == 1):
                            frequency[col] += 1
                        elif(cs == 3):
                            frequency[col] -= 1
                    elif(row == 9) :
                        if(cs == 1):
                            frequency[col] += 1
                        elif(cs == 5):
                            frequency[col] -= 1
                    else :
                        if(cs == 1): # check frequency when the row is not 0 , 9 row
                            frequency[col] += 1
                        elif(cs == 6):
                            frequency[col] -= 1
                    try_row.append(cs)
                    if(p_sp > 0):
                        if(col == 9):
                            p_sp = -1080
                            break
                        row_max = right_max + diff_col[col]
                    else:
                        if(col == 9):
                            p_sp = 1080
                            break
                        row_max = left_max + diff_col[col]
                    while(row_count < row_max ):
                        row_motor.run_to_rel_pos(position_sp = p_sp , speed_sp = r_sp)
                        row_count += 1
                    row_count = 0
                row_motor.stop()
                tries.append(try_row)
            tries[1].reverse()
            if(tries[0] == tries[1]):
                print(tries[0])
                break
            elif(try_counts > 1):
                key = -1
                if( row == 0):
                    key = 3
                elif( row == 9):
                    key = 5
                else :
                    key = 6
                for t in range(10):
                    if (frequency[t] > 0 ):
                        frequency[t] = 1
                    else :
                        frequency[t] = key
                print(frequency)
                break
            else :
                try_counts += 1
            #row_motor.stop()
            #time.sleep(0.5)
            # print(col)
except :
    row_motor.stop()
    col_motor.stop()
col_motor.stop()
row_motor.stop()
# ev3.Sound.beep()