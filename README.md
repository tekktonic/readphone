# Introduction
Read phone data from an AndroSensor CSV file.

Make use of the light sensor, microphone, proximity sensor, and accelerometers to draw conclusions about the user's activity during a session captured by AndroSensor.

# Inferred Metrics
1. The user's time in low light environments (in frames.)
2. The user's average light level (lux.)
3. The time when the phone was in the user's pocket (in frames.)
4. The user's pocket time when the microphone detected noise loud enough to be conversation.
5. The user's active time, when they were likely to be moving around.
6. The user's active percentage, what amount of the recording time they were active for.

Additionally, it plots three factors used in detecting these: total movement, light level, and sound level.
