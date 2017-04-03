import RPi.GPIO as GPIO
import MFRC522
import signal
from Attendance import Attendance
from Register import Register
import time

class Read():
    
    CONTINUE_READING = None
    MIFAREReader = None
    MODE = None
    LED_RED = 7
    LED_GREEN = 37

    def __init__(self, mode):
        GPIO.setmode(GPIO.BOARD)
        self.__led(self.LED_RED, 1)
        self.__led(self.LED_GREEN, 1)
        time.sleep(1)
        self.__led(self.LED_GREEN, 0)

        self.CONTINUE_READING = True
        if mode:
            print 'Scan a card to mark attendance'
        else:
            print 'Scan a card to register'
        self.MODE = mode
        # Hook the SIGINT
        signal.signal(signal.SIGINT, self.__endRead)
        

    # Capture SIGINT for cleanup when the script is aborted
    def __endRead(self, signal,frame):
        self.__led(self.LED_RED, 0);
        self.__led(self.LED_GREEN, 0);
        print "Ctrl+C captured, ending read."
        self.CONTINUE_READING = False
        GPIO.cleanup()

    def __led(self, pin, state):
        GPIO.setup(pin, GPIO.OUT)
        if state:
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin,GPIO.LOW)
              

    def start(self):
        # Create an object of the class MFRC522
        MIFAREReader = MFRC522.MFRC522()

        # This loop keeps checking for chips. If one is near it will get the UID and authenticate
        while self.CONTINUE_READING:
            
            # Scan for cards    
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            
            # Get the UID of the card
            (status,uid) = MIFAREReader.MFRC522_Anticoll()

            # If we have the UID, continue
            if status == MIFAREReader.MI_OK:
                RFID = str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
                if self.MODE:
                    record = Attendance().markAttendance(RFID)
                else:
                    record = Register().new(RFID)

                if record:
                    self.__led(self.LED_GREEN, 1)
                    time.sleep(1)
                    self.__led(self.LED_GREEN, 0)

