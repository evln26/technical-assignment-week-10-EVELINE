import RPi.GPIO as GPIO
import time
from ubidots import ApiClient
import random

# Ubidots API Token
API_TOKEN = "BBFF-oqbWpMBA5aTdSZMZnlmSG9MahP38bo"

# Ubidots Variable IDs
distance_variable_id = "64db2598358957000c29f93b"
random_variable_id = "64db259f358957000c29f93c"

# GPIO setup
GPIO.setmode(GPIO.BCM)
TRIG = 2
ECHO = 3
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Ubidots setup
api = ApiClient(token=API_TOKEN)
distance_variable = api.get_variable(distance_variable_id)
random_variable = api.get_variable(random_variable_id)

def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    start_time = time.time()
    stop_time = time.time()
    
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
    
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()
    
    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2  # Sound speed in cm/s
    
    return distance

try:
    while True:
        distance = get_distance()
        random_value = random.randint(1, 100)

        print("Distance: {:.2f} cm".format(distance))
        print("Random Value:", random_value)

        # Send data to Ubidots
        distance_variable.save_value({"value": distance})
        random_variable.save_value({"value": random_value})

        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
