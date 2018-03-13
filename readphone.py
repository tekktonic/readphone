"""Interpret AndroSensor data into various 'interesting'
categories and metrics, depending on your definition of interesting."""

# CSV import
import pandas as p

# The function-based interface for plotting lists.
import matplotlib.pyplot as plot



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
    for _, item in enumerate(arr):
        ret.append(item[col])
    return ret

def is_low_light(frame):
    """Microsoft's usability guidelines say that dim
    lighting starts at 200 lux."""
    return frame[LUX_INDEX] < 200

def is_close(frame):
    """My particular phone sensor is binary, either 5cm or 0cm.
    I can't vouch for others."""
    return frame[PROXIMITY_INDEX] < 5

def is_audible(frame):
    """60 decibels is roughly the noise level of conversation"""
    return frame[DECIBEL_INDEX] > 60

def is_active(frame):
    """Just an arbitrary threshhold for "Yeah, it looks like this person is moving"
    via the sensors"""
    return (abs(frame[LAT_X_INDEX]) + abs(frame[LAT_Y_INDEX]) + abs(frame[LAT_Z_INDEX])) > 1


# Read the CSV file containing all of our data
DATA = p.read_csv("data.csv")

# Extract the numpy array which is the actual data values without context.
NUM = DATA.values


# The time column is the X axis for practically every graph
TIME = column(NUM, TIME_INDEX)

# Time is recorded in milliseconds, convert to seconds.
TIME = [TIME / 1000.0 for TIME in TIME]

# Extract all of our sensor snapshots which are in low light.
LOW_LIGHT_FRAMES = [frame for frame in NUM if is_low_light(frame)]

# If the light is low and there's something right next to us,
#we're probably either on the phone or it's in the pocket.
POCKET = [frame for frame in LOW_LIGHT_FRAMES if is_close(frame)]


# Extract all frames which were above the conversation threshhold
NOISY = [frame for frame in POCKET if is_audible(frame)]


print("There are " + str(len(NUM)) + " frames of data in total, each frame is 0.5s")

print("There are " + str(len(LOW_LIGHT_FRAMES)) + " frames with low light")

print("Of those, it was probably in my pocket " + str(len(POCKET)) + " frames")

print("The average light level overall was "
      + str(sum(column(NUM, LUX_INDEX))/len(NUM)) + ". I'm in a dark part of the office.")

# Just get the total time from the first and last frames quickly.
TOTAL_TIME = (NUM[-1][TIME_INDEX] - NUM[0][TIME_INDEX]) / 1000.0

# Pull all frames during which we were active (above a linear acceleration threshhold.)
ACTIVE_TIME = [frame for frame in NUM if is_active(frame)]

print("Of those frames when it was probably in my pocket, we probably were able to pick "
      + "up on conversation for " + str(len(NOISY)) + " of them.")

print("The total amount of time spent recording was " + str(TOTAL_TIME) + " S")

# Each frame is 500 milliseconds.
ACTIVE_TIME = (500 * len(ACTIVE_TIME)) / 1000.0

print("The active time was " + str(ACTIVE_TIME) + ".")

print("Which means I had an active percentage of " + str((ACTIVE_TIME / TOTAL_TIME) * 100) + ".")

# Plot various relevant metrics.
plot.plot(TIME, column(NUM, LUX_INDEX))
plot.title("Lux (light level) vs time.")
plot.show()

plot.plot(TIME, column(NUM, DECIBEL_INDEX))
plot.title("Decibels (sound level) vs time.")
plot.show()

# Take every frame and sum the X, Y, and Z acceleration magnitudes in those frames.
MOVEMENT_SUMS = []
for sensor_frame in NUM:
    MOVEMENT_SUMS.append((abs(sensor_frame[LAT_X_INDEX]) + abs(sensor_frame[LAT_Y_INDEX])
                          + abs(sensor_frame[LAT_Z_INDEX])))

plot.plot(TIME, MOVEMENT_SUMS)
plot.title("Total movement vs time.")
plot.show()

# Just show a binary chart: either the user is active or the user is not,
# as determined by our threshhold that we decided on before.
ACTIVE = []
for sensor_frame in NUM:
    if (abs(sensor_frame[LAT_X_INDEX]) + abs(sensor_frame[LAT_Y_INDEX])
            + abs(sensor_frame[LAT_Z_INDEX])) > 1:
        ACTIVE.append(1)
    else:
        ACTIVE.append(0)

plot.bar(TIME, ACTIVE)
plot.title("Blocks of active time.")
plot.show()
