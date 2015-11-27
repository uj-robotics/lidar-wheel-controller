__author__ = 'Rafał'
"""
MAC: 80:1f:02:a2:f2:43
login: pi
haslo: UJlidar
"""

from PySide import QtCore
import sys
import communication
import robot
import signal


class RobotController:
    """
    Main class for robot controller
    """
    def __init__(self):
        # Time
        self.t = 0
        self.scan_time = 100  # ms

        # Robot
        self.robot = robot.Robot()

        # Communication
        self.communication = communication.Communication()
        self.communication.make_server()
        self.communication.new_data.connect(self.new_message)

        # run clock
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL('timeout()'), self.run)
        self.timer.start(self.scan_time)

    @QtCore.Slot(object)
    def run(self):
        pass

    @QtCore.Slot(object)
    def new_message(self, message):
        self.robot.move(message['left_motor']/255.0, message['right_motor']/255.0)

    def sigint_handler(self, *args):
        """
        Stop thread before end
        """
        self.communication.stop()
        QtCore.QCoreApplication.quit()

if __name__ == "__main__":
    app = QtCore.QCoreApplication(sys.argv)
    robotController = RobotController()
    signal.signal(signal.SIGINT, robotController.sigint_handler)  # allow ctrl+c
    app.exec_()
    robotController.communication.stop()
    sys.exit()