__author__ = 'Rafał'

import PicoBorgRev
import time
import math

"""
Klasa obsługująca koła
"""


class Robot:
    def __init__(self):
        self.PBR = PicoBorgRev.PicoBorgRev()
        self.PBR.Init()
        self.is_good  = True
        if not self.PBR.foundChip:
            boards = PicoBorgRev.ScanForPicoBorgReverse()
            if len(boards) == 0:
                print('No PicoBorg Reverse found, check you are attached :)')
            else:
                print('No PicoBorg Reverse at address %02X, but we did find boards:' % (self.PBR.i2cAddress))
                for board in boards:
                    print('    %02X (%d)' % (board, board))
                print('If you need to change the I²C address change the setup line so it is correct, e.g.')
                print('PBR.i2cAddress = 0x%02X' % (boards[0]))
            self.is_good = False
            return

        self.PBR.SetCommsFailsafe(False)             # Disable the communications failsafe
        self.PBR.ResetEpo()

        self.timeForward1m = 5.7                     # Number of seconds needed to move about 1 meter
        self.timeSpin360   = 4.8                     # Number of seconds needed to make a full left / right spin
        self.testMode = False                        # True to run the motion tests, False to run the normal sequence

        self.voltageIn = 12.0                        # Total battery voltage to the PicoBorg Reverse
        self.voltageOut = 6.0                        # Maximum motor voltage

        if self.voltageOut > self.voltageIn:
           self.maxPower = 1.0
        else:
            self.maxPower = self.voltageOut / float(self.voltageIn)

    # Function to perform a general movement
    def move(self, driveLeft, driveRight):
        # Set the motors running
        self.PBR.SetMotor1(driveRight * self.maxPower)
        self.PBR.SetMotor2(-driveLeft * self.maxPower)

    def stop(self):
        # Turn the motors off
        self.PBR.MotorsOff()

    def spin(self, angle):
        if angle < 0.0:
            # Left turn
            driveLeft  = -1.0
            driveRight = +1.0
            angle *= -1
        else:
            # Right turn
            driveLeft  = +1.0
            driveRight = -1.0
        # Perform the motion
        self.move(driveLeft, driveRight)

if __name__ == "__main__":
    r = Robot()
    r.move(1, 1)
    time.sleep(3)
    r.stop()
