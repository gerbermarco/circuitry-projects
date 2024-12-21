import time
import random
from threading import Thread
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw
import adafruit_ssd1306
from gpiozero import LED

print("Initializing I2C and OLED")
# Initialize I2C and OLED
i2c = busio.I2C(SCL, SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)  # Ensure the correct width and height

# Create blank image for drawing
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

print("Setting up LEDs")
led_pins = [17, 27, 5, 6]
leds = [LED(pin) for pin in led_pins]

def blink_led(led):
    while True:
        led.on()
        time.sleep(random.uniform(0.1, 0.5))
        led.off()
        time.sleep(random.uniform(0.1, 0.5))

# Start a thread for each LED to blink independently
for led in leds:
    thread = Thread(target=blink_led, args=(led,))
    thread.daemon = True
    thread.start()

def draw_tree():
    # Draw Christmas tree
    draw.polygon([(66, 5), (50, 15), (82, 15)], fill=1)  # Top
    draw.polygon([(66, 12), (45, 22), (87, 22)], fill=1)  # Middle
    draw.polygon([(66, 19), (40, 29), (92, 29)], fill=1)  # Bottom
    draw.rectangle((62, 29, 70, 32), fill=1)  # Trunk

# Create snow particles
snow = [(random.randint(0, 127), random.randint(0, 31)) for _ in range(15)]

print("Merry Christmas!")

try:
    while True:
        # Clear display
        draw.rectangle((0, 0, 127, 31), outline=0, fill=0)

        # Draw tree
        draw_tree()

        # Update and draw snow
        for i in range(len(snow)):
            x, y = snow[i]
            draw.point((x, y), fill=1)
            # Move snow down and sideways slightly
            y = (y + 1) % 32
            x = (x + random.randint(-1, 1)) % 128
            snow[i] = (x, y)

        # Display image
        oled.image(image)
        oled.show()
        time.sleep(0.1)

except KeyboardInterrupt:
    # Clear display on exit
    oled.fill(0)
    oled.show()