# MicroPython

from machine import Pin, time_pulse_us, ADC
import time

# Pin definitions for LEDs
white_led = Pin(2, Pin.OUT)
green_led_1 = Pin(3, Pin.OUT)
green_led_2 = Pin(4, Pin.OUT)
yellow_led_1 = Pin(5, Pin.OUT)
yellow_led_2 = Pin(9, Pin.OUT)
red_led_1 = Pin(7, Pin.OUT)
red_led_2 = Pin(11, Pin.OUT)

# Pin definition for Buzzer
buzzer = Pin(28, Pin.OUT)

# Pin definitions for Ultrasonic sensor
trig = Pin(15, Pin.OUT)
echo = Pin(16, Pin.IN)

# Pin definition for Sound Sensor
sound_sensor = ADC(Pin(26))

# Function to measure distance
def measure_distance():
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(10)
    trig.low()
    
    duration = time_pulse_us(echo, 1)
    
    # Calculate the distance in cm
    distance = (duration / 2) / 29.1
    return distance

# Function to control buzzer sound
def buzzer_alert(distance):
    if distance < 4:
        # Too close
        buzzer.on()
    elif distance < 10:
        # Close distance, continuous sound
        buzzer.on()
        time.sleep(0.1)
        buzzer.off()
    elif distance < 20:
        # Medium distance, fast beeps
        buzzer.on()
        time.sleep(0.1)
        buzzer.off()
        time.sleep(0.1)
    elif distance < 30:
        # Far distance, slow beeps
        buzzer.on()
        time.sleep(0.2)
        buzzer.off()
        time.sleep(0.3)
    else:
        buzzer.off()

def check_buzzer_status():
    # Read analog value from the sound sensor
    sound_level = sound_sensor.read_u16()
    threshold = 1000  
    if sound_level > threshold:
        return True # Main buzzer operating normal
    else:
        return False

# Check if the distance sensor is operating
def check_distance_sensor(distance):
    if distance < 0:
        return False # Distance sensor not working
    else:
        return True

# Distance sensor error case
def sensor_error_alert():
    red_led_1.toggle()
    red_led_2.toggle()
    buzzer.on()
    time.sleep(0.05)
    buzzer.off()
    time.sleep(0.05)

# Main loop
while True:
    distance = measure_distance()
    
    if check_distance_sensor(distance):
        print("Distance: ", distance, "cm")
    else:
        print("Distance: ", distance, "cm")
        print("Distance sensor error!")
        sensor_error_alert()
    
    # White LED always on
    white_led.value(1)
    
    # Control LEDs based on distance
    if distance < 4:
        red_led_1.value(1)
        red_led_2.value(1)
        yellow_led_1.value(1)
        yellow_led_2.value(1)
        green_led_1.value(1)
        green_led_2.value(1)
    elif distance < 10:
        red_led_1.value(1)
        red_led_2.value(0)
        yellow_led_1.value(1)
        yellow_led_2.value(1)
        green_led_1.value(1)
        green_led_2.value(1)
    elif distance < 15:
        red_led_1.value(0)
        red_led_2.value(0)
        yellow_led_1.value(1)
        yellow_led_2.value(1)
        green_led_1.value(1)
        green_led_2.value(1)
    elif distance < 20:
        red_led_1.value(0)
        red_led_2.value(0)
        yellow_led_1.value(1)
        yellow_led_2.value(0)
        green_led_1.value(1)
        green_led_2.value(1)
    elif distance < 25:
        red_led_1.value(0)
        red_led_2.value(0)
        yellow_led_1.value(0)
        yellow_led_2.value(0)
        green_led_1.value(1)
        green_led_2.value(1)
    elif distance < 30:
        red_led_1.value(0)
        red_led_2.value(0)
        yellow_led_1.value(0)
        yellow_led_2.value(0)
        green_led_1.value(1)
        green_led_2.value(0)
    else:
        red_led_1.value(0)
        red_led_2.value(0)
        yellow_led_1.value(0)
        yellow_led_2.value(0)
        green_led_1.value(0)
        green_led_2.value(0)

    
    if distance < 30:
        # Check if the main buzzer is working
        noneedbackup = check_buzzer_status()
        if noneedbackup:
            buzzer_alert(distance)
        else:
            buzzer = Pin(27, Pin.OUT)
            print("MAIN BUZZER ERROR")
            buzzer_alert(distance)
    
    # Small delay to prevent excessive polling
    time.sleep(0.1)
