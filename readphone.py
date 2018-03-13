"""Interpret AndroSensor data into various 'interesting' categories and metrics, depending on your definition of interesting."""

# CSV import things
import pandas as p

# The function-based interface for plotting lists.
import matplotlib.pyplot as plot

# Python standard math library.
import math

# These are the various offsets of interesting measurements in AndroSensor data.
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
    """Given a 2D array, extract all the elements in one column to its own list"""
    ret = []
    for i in range(0, len(arr)):
        ret.append(arr[i][col])
    return ret

def is_low_light(frame):
    """Microsoft's usability guidelines say that dim lighting starts at 200 lux."""
    return (frame[LUX_INDEX] < 200)

def is_close(frame):
    """My particular phone sensor is binary, either 5cm or 0cm. I can't vouch for others."""
    return frame[PROXIMITY_INDEX] < 5

def is_audible(frame):
    """60 decibels is roughly the noise level of conversation"""
    return frame[DECIBEL_INDEX] > 60

def is_active(frame):
    """Just an arbitrary threshhold for "Yeah, it looks like this person is moving" via the sensors"""
    return (abs(frame[LAT_X_INDEX]) + abs(frame[LAT_Y_INDEX]) + abs(frame[LAT_Z_INDEX])) > 1


# Read the CSV file containing all of our data
data = p.read_csv("data.csv")

# Extract the numpy array which is the actual data values without context.
num = data.values


# The time column is the X axis for practically every graph
time = column(num, TIME_INDEX)

# Time is recorded in milliseconds, convert to seconds.
time = [time / 1000.0 for time in time]

# Extract all of our sensor snapshots which are in low light.
low_light_frames = [frame for frame in num if is_low_light(frame)]

# If the light is low and there's something right next to us, we're probably either on the phone or it's in the pocket.
pocket = [frame for frame in low_light_frames if is_close(frame)]


# Extract all frames which were above the conversation threshhold
noisy = [frame for frame in pocket if is_audible(frame)]


print("There are " + str(len(num)) + " frames of data in total, each frame is 0.5s")

print("There are " + str(len(low_light_frames)) + " frames with low light")

print("Of those, it was probably in my pocket " + str(len(pocket)) + " frames");

print("The average light level overall was " + str(sum(column(num, LUX_INDEX))/len(num)) + ". I'm in a dark part of the office.")


# Just get the total time from the first and last frames quickly.
total_time = (num[-1][TIME_INDEX] - num[0][TIME_INDEX]) / 1000.0


# Pull all frames during which we were active (above a linear acceleration threshhold.)
active_time = [frame for frame in num if is_active(frame)]


print("Of those frames when it was probably in my pocket, we probably were able to pick up on conversation for " + str(len(noisy)) + " of them.")

print("The total amount of time spent recording was " + str(total_time) + " S")

# Each frame is 500 milliseconds.
active_time = (500 * len(active_time)) / 1000.0

print("The active time was " + str(active_time) + ".")

print("Which means I had an active percentage of " + str((active_time / total_time) * 100) + ".")


# Plot various relevant metrics.

plot.plot(time, column(num, LUX_INDEX))
plot.title("Lux (light level) vs time.")
plot.show()

plot.plot(time, column(num,DECIBEL_INDEX))
plot.title("Decibels (sound level) vs time.")
plot.show()

# Take every frame and sum the X, Y, and Z acceleration magnitudes in those frames.
movement_sums = []
for frame in num:
    movement_sums.append((abs(frame[LAT_X_INDEX]) + abs(frame[LAT_Y_INDEX]) + abs(frame[LAT_Z_INDEX])))
    
plot.plot(time, movement_sums)
plot.title("Total movement vs time.")
plot.show()

# Just show a binary chart: either the user is active or the user is not, as determined by our threshhold that we decided on before.
active = []
for frame in num:
    if ((abs(frame[LAT_X_INDEX]) + abs(frame[LAT_Y_INDEX]) + abs(frame[LAT_Z_INDEX])) > 1):
        active.append(1)
    else:
        active.append(0)
    
plot.bar(time, active)
plot.title("Blocks of active time.")
plot.show()

