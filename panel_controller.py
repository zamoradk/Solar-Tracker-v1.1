import RPi.GPIO as GPIO
import time


class PanelController:
    
    def __init__(self, cw_pin, ccw_pin):
        
        self.name = 'PanelController'
        # Assign pins
        self._assign_pins([cw_pin, ccw_pin])

        self._pin_dirs = {'cw': cw_pin, 'ccw': ccw_pin}

    def rotate_panels(self, on_time, direction):
        
        delta = 0
        start = time.perf_counter()
        pin_num = self._pin_dirs[direction]
        print(pin_num)
        
        while delta < on_time:
            GPIO.output(pin_num, True)
            delta = time.perf_counter() - start
    
        print(f'Rotated panels for {delta} seconds.')

        GPIO.output(pin_num, False)
            
    def _assign_pins(self, pins):
        
        GPIO.setmode(GPIO.BCM)
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)