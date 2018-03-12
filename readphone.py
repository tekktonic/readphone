import pandas as p
import numpy as n
import matplotlib.pyplot as plot
import math

ACCEL_X_INDEX = 0
ACCEL_Y_INDEX = 1
ACCEL_Z_INDEX = 2

LAT_X_INDEX = 6
LAT_Y_INDEX = 7
LAT_Z_INDEX = 8

LUX_INDEX = 12

ORIENTATION_X_INDEX = 16
ORIENTATION_Y_INDEX = 17
ORIENTATION_Z_INDEX = 18

PROXIMITY_INDEX = 19
DECIBEL_INDEX = 20
TIME_INDEX = 29

def column(arr, col):
    ret = []
    for i in range(0, len(arr)):
        ret.append(arr[i][col])
    return ret

data = p.read_csv("data.csv")


num = data.values

light = column(num, 12)
time = column(num, TIME_INDEX)
time = [time / 1000.0 for time in time]

# According to Microsoft user guides, dim indoor lighting is about 200 lux.
low_light_frames = [frame for frame in num if frame[LUX_INDEX] < 200]

# If the light is low and there's something right next to us, we're probably either on the phone or it's in the pocket.
# My phone's proximity meter is binary: it's either 5 cm or 0 cm.
pocket = [frame for frame in low_light_frames if frame[PROXIMITY_INDEX] < 5]

# 60 decibels is the volume of a normal conversation.
noisy = [frame for frame in pocket if frame[DECIBEL_INDEX] > 60]
print("There are " + str(len(num)) + " frames of data in total.")
print("There are " + str(len(low_light_frames)) + " sensor frames with low light")

print("Of those, it was probably in my pocket " + str(len(pocket)) + " frames");
print("The average light level overall was " + str(sum(column(num, LUX_INDEX))/len(num)) + ". I'm in a dark part of the office.")

total_time = (num[-1][TIME_INDEX] - num[0][TIME_INDEX]) / 1000.0


active_time = [frame for frame in num if ((abs(frame[LAT_X_INDEX]) + abs(frame[LAT_Y_INDEX]) + abs(frame[LAT_Z_INDEX])) > 1)]

print("Of those times when it was probably in my pocket, we probably were able to pick up on conversation for " + str(len(noisy)) + " of them.")

print("The total amount of time spent recording was " + str(total_time) + " S")

# Each frame is .5 seconds.
active_time = (500 * len(active_time)) / 1000.0

print("The active time was " + str(active_time) + ".")

print("Which means I had an active percentage of " + str((active_time / total_time) * 100) + ".")


plot.plot(time, column(num, LUX_INDEX))
plot.title("Lux (light level) vs time.")
plot.show()

plot.plot(time, column(num,DECIBEL_INDEX))
plot.title("Decibels (sound level) vs time.")
plot.show()

movement_sums = []
for frame in num:
    movement_sums.append((abs(frame[LAT_X_INDEX]) + abs(frame[LAT_Y_INDEX]) + abs(frame[LAT_Z_INDEX])))
    
plot.plot(time, movement_sums)
plot.title("Total movement vs time.")
plot.show()

active = []

for frame in num:
    if ((abs(frame[LAT_X_INDEX]) + abs(frame[LAT_Y_INDEX]) + abs(frame[LAT_Z_INDEX])) > 1):
        active.append(1)
    else:
        active.append(0)
    
plot.bar(time, active)
plot.title("Blocks of active time.")
plot.show()

