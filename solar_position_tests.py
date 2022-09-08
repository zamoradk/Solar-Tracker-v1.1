import sys
import os
sys.path.insert(0, os.getcwd())

import unittest

from lib.solar_position import SolarPosition

class SolarPositionTests(unittest.TestCase):
    
    def test_position(self):
        
        latitude = 32.7133421
        longitude = -97.3468719
        d_time_zone = -5
        
        solar_position = SolarPosition(latitude,
                                       longitude,
                                       d_time_zone)
        
        day_of_year = 0
        fake_time_now_min = 0
        
        hras = {}
        while fake_time_now_min < 1440:
            solar_position.update_sun_position(day_of_year, fake_time_now_min)
            _, _, _, hra = solar_position.position

            hras[fake_time_now_min] = hra
            
            fake_time_now_min += 60
    
        self.assertEqual(len(hras.keys()), 24)
        for key in hras:
            hra = hras[key]
            
            print(f'Time: {key//60}, hra: {hra}')
              
            if key // 60 < 12:
                self.assertTrue(hra < 0)
            else:
                self.assertTrue(hra > 0)
                
            
if __name__=='__main__':
    unittest.main()