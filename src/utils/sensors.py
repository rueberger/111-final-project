from dac import set_voltage
from adc import read_rms
from time import sleep, time

class Sensors(object):

    def __init__(self):
        """
        might want to put a dialog for calibrating here
        """
        # bugs for first timestep but whatever
        self.last_pos = 0
        self.last_time = 0
        self.calibrate_top()
        self.calibrate_bottom()

    def calibrate_top(self):
        # need to rewrite
        print "Calibrating top speed. Stand back"
        set_voltage(3.3)
        measured = read_rms(itrs=100)
        print "Calibration finished"
        self.top_cal = measured

    def calibrate_bottom(self):
        print "Calibrating min speed. Stand back."
        set_voltage(0)
        measured = read_rms()
        print "Calibration finished"
        self.bot_cal = measured

    def measure_pos(self):
        """
        unitless conversion
        return value between 0 and 1
        """
        # may want to do an average
        pos = (read_rms() - self.bot_cal) / self.top_cal
        return pos, time()

    def measure(self):
        """
        returns curr_pos, velocity, delta t
        """
        curr_pos, curr_time = self.measure_pos()
        d_t = curr_time - self.last_time
        velocity = (curr_pos - self.last_pos) / (curr_time - self.last_time)
        self.last_pos = curr_pos
        self.last_time = curr_time
        return curr_pos, velocity, d_t, curr_time
