import time
import argparse
from datetime import datetime

#import RPi.GPIO as GPIO

from lib.configuration import Configuration
from lib.panel_position import PanelPosition
from lib.solar_position import SolarPosition
from lib.panel_controller import PanelController


class main:
    
    def __init__(self, args):
        
        config = Configuration(args.config_path)
        print(config)
    
        # Create object to track sun's position
        self._solar_position = SolarPosition(config.latitude,
                                             config.longitude,
                                             config.d_time_zone)

        # Initialize with sun's position as of right now
        day_of_year, now_min = self._get_time_now()
        
        self._solar_position.update_sun_position(day_of_year, now_min)
        self._solar_position.update_sunrise_sunset()

        # Create object to track panel's position 
        self._panel_position = PanelPosition(5,
                                             config.panel_init_angle)

        # Create object to control rotation of panels
        self._panel_controller = PanelController(config.cw_pin,
                                                 config.ccw_pin)
        
    def _get_time_now(self, old_day_of_year = None):
        
        today = datetime.now().timetuple()
        day_of_year = today.tm_yday
        hr_, min_, sec_ = today.tm_hour, today.tm_min, today.tm_sec
        now_min = hr_ * 60 + min_ + sec_ / 60
        
        day_changed = False
        if day_of_year is not None:
            if old_day_of_year != day_of_year:
                day_changed = True
            
        return day_of_year, now_min
        
    def run(self):
        
        print(f'Starting to run the program.')
        
        self.__running = True
        day_of_year, now_min = self._get_time_now()
        now_min_spoof = now_min
        day_changed = False
        
        while self.__running:
            # In some class, make a trigger event to update things

            try:
                time.sleep(1)
                #day_of_year, now_min, day_changed = self._get_time_now(day_of_year)

                self._solar_position.update_sun_position(day_of_year, now_min_spoof)
                if day_changed:
                    self._solar_position.update_sunrise_sunset()
                    day_changed = False

                _, _, _, hra = self._solar_position.position
                sunrise = self._solar_position.sunrise
                sunset = self._solar_position.sunset
                
                # If between sunrise and sunset, track sun
                if now_min_spoof >= sunrise and now_min_spoof <= sunset:
                    on_time, direction = self._panel_position.update_angle(hra)
                    angle = self._panel_position.angle
                else:
                    # Calculate HRA of sunrise and go to it
                    hra_sunrise = self._solar_position._calculate_hra(sunrise, day_of_year + 1)
                    on_time, direction = self._panel_position.update_angle(hra_sunrise)
                    angle = self._panel_position.angle
                    
                print(f'At time {now_min_spoof / 60}: \n'
                      f'The sun is at {hra} deg of HRA.\n'
                      f'The panels needs to be at {angle} degrees.\n'
                      f'The motors need to turn on for {on_time} seconds.')
                
                if on_time > 0:
                    self._panel_controller.rotate_panels(on_time, direction)

                # Spoof the time
                now_min_spoof += 60
                if now_min_spoof > 1440:
                    day_changed = True
                    now_min_spoof = 0.0
                
            except KeyboardInterrupt:
                self.terminate()
            
    def terminate(self):
        print('All done!')
        self.__running = False
        GPIO.cleanup()

if __name__=='__main__':
    
    parser = argparse.ArgumentParser(description='Arguments to pass to main functionality.')
    parser.add_argument('--config_path', default='./config.yaml',
                         help='Path to the config.yaml file.')
    args = parser.parse_args()

    main = main(args)
    main.run()
