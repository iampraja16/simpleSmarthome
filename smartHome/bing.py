from pyfirmata import Arduino, util
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import pyqtSlot, QUrl, QObject
import sys

board = Arduino('COM3')

it = util.Iterator(board)
it.start()

LDR_PIN = 0
LM35_PIN = 2
MOTOR_PIN = 3
SERVO_PIN = 5
ECHO_PIN = 9
TRIG_PIN = 10
LED1_PIN = 11
LED2_PIN = 12
LED3_PIN = 13
LED4_PIN = 8
LED5_PIN = 7

ldr = board.get_pin(f'a:{LDR_PIN}:i')
lm35 = board.get_pin(f'd:{LM35_PIN}:i')
motor = board.get_pin(f'd:{MOTOR_PIN}:p')
servo = board.get_pin(f'd:{SERVO_PIN}:s')
echo = board.get_pin(f'd:{ECHO_PIN}:i')
trig = board.get_pin(f'd:{TRIG_PIN}:o')
led1 = board.get_pin(f'd:{LED1_PIN}:o')
led2 = board.get_pin(f'd:{LED2_PIN}:o')
led3 = board.get_pin(f'd:{LED3_PIN}:o')
led4 = board.get_pin(f'd:{LED4_PIN}:o')
led5 = board.get_pin(f'd:{LED5_PIN}:o')

#GATAU ANJING KENAPA INI HARUS DI SET, PADAHAL GUA PENGENNYA SET POINT DIATUR KEK BAPAK
LM35_SET_POINT = 20
LDR_SET_POINT = 500

ldr.enable_reporting()
lm35.enable_reporting()


def read_ultra(trig_pin, echo_pin):
    trig_pin.write(1)
    board.pass_time(0.00001)
    trig_pin.write(0)

    duration = echo_pin.read()

    distance = duration * 340 / 2 * 100
    return distance

def control_light(led3, ldr_value, LDR_SET_POINT):
    print(f"LDR Value {ldr_value: }")
    print(f"LDR_SET_POINT: {LDR_SET_POINT}")
    if ldr_value > LDR_SET_POINT:
        led3.write(1)
    else:
        led3.write(0)

def control_motor(motor, lm35_value, LM35_SET_POINT):
    if lm35_value > LM35_SET_POINT:
        motor.write(0)
    else:
        motor.write(1)

def control_servo(servo, ultra_value):
    if ultra_value < 10:
        servo.write(0)
    else:
        servo.write(90)

class Communicator(QObject):
    ldr = 0
    lm35 = 0
    ultra = 0

    @pyqtSlot(int)
    def receive_ldr_set_point(self, value):
        global LDR_SET_POINT
        LDR_SET_POINT = value

    @pyqtSlot(int)
    def receive_LM35_set_point(self, value):
        global LM35_SET_POINT
        LM35_SET_POINT = value

    @pyqtSlot(bool)
    def receive_led1_status(self, value):
        led1.write(value)

    @pyqtSlot(bool)
    def receive_led2_status(self, value):
        led2.write(value)
        
    @pyqtSlot(bool)
    def receive_led4_status(self, value):
        led4.write(value)
        
    @pyqtSlot(bool)
    def receive_led5_status(self, value):
        led5.write(value)

    @pyqtSlot(int)
    def receive_servo_angle(self, value):
        servo.write(value)
        
    @pyqtSlot(str)
    def receive_servo_command(self, command):
        print(f"Received servo command: {command}")
        if command == "clockwise":
            print("Moving servo clockwise")
            servo.write(180)
        elif command == "counterclockwise":
            print("Moving servo counterclockwise")
            servo.write(0)
            

app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
communicator = Communicator()
engine.rootContext().setContextProperty("communicator", communicator)
engine.load(QUrl("bing.qml"))
root = engine.rootObjects()

while True:
    ldr_value = ldr.read()
    lm35_value = read_lm35(lm35)
    ultra_value = read_ultra(trig, echo)

    control_light(led3, ldr_value, LDR_SET_POINT)
    control_motor(motor, lm35_value, LM35_SET_POINT)
    control_servo(servo, ultra_value)

    communicator.ldr = ldr_value
    communicator.lm35 = lm35_value
    communicator.ultra = ultra_value

    app.exec_()

