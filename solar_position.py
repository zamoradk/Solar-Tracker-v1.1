import math


class SolarPosition:

    def __init__(self, lat, long, d_time_zone):
        
        self._azimuth = None
        self._declination = None
        self._elevation = None
        self._hra = None
        
        self._lat = lat
        self._long = long
        self._d_time_zone = d_time_zone

        self._sunrise = None
        self._sunset = None

    @property
    def position(self) -> tuple:
        """Retrieves the position of the sun

        Returns:
            Tuple containing the declination, elevation, and azimuth of the
            sun

        """
        return (self._declination, self._elevation, self._azimuth, self._hra)

    @property
    def sunrise(self) -> float:
        return self._sunrise
    
    @property
    def sunset(self) -> float:
        return self._sunset

    def update_sun_position(self, day_of_year: int, now_min: float):
        """Calculates the declination, elevation, and azimuth angles of the sun.

        Args:
            day_of_year: Numerical value of the day of the year
            now_min: The time of day it currently is in minutes
            lat: Latitude of the position
        
        """
        
        hra = self._calculate_hra(now_min, day_of_year)
        self._hra = hra
        self._calculate_declination(day_of_year)
        self._calculate_elevation(hra)
        self._calculate_azimuth(hra)

    def update_sunrise_sunset(self):
        """Calculates the time of sunrise and sunset in minutes
        using the latitude and declination angle.
        
        """
        
        lat_rad = math.radians(self._lat)
        dec_rad = math.radians(self._declination)
        
        arg_rad = -math.tan(lat_rad) * math.tan(dec_rad)
        ans_rad = math.acos(arg_rad)
        
        ans_deg = math.degrees(ans_rad)
        
        self._sunrise = (12 - ans_deg / 15 - self._tc / 60) * 60
        self._sunset = (12 + ans_deg / 15 - self._tc / 60) * 60

        print(f'Sunrise is at: {self._sunrise}, Sunset is at: {self._sunset}')
        
    def _calculate_hra(self, now_min, day_of_year):
        
        self._tc, self.eot_min = self._calculate_tc(self._d_time_zone, day_of_year)
        lst = (now_min/60) + self._tc / 60
        hra = 15*(lst - 12)
        
        return hra
    
    def _calculate_declination(self, day_of_year: int):
        """Method to calculate the declination angle of the
        sun. Uses equation:
            d = -23.45 * cos((360/365) * (day + 10))

        Args:
            day_of_year: Numerical value of the day of the year
        
        """
        arg_in_rads = math.radians((360/365) * (day_of_year + 10))

        self._declination = math.degrees(-math.radians(23.45) * math.cos(arg_in_rads))

    def _calculate_elevation(self, hra: float):
        """Method to calculate the elevation angle of the
        sun. Uses equation:

            alpha = asin(sin(d)sin(lat) + cos(d)cos(lat)cos(HRA))

        Args:
            hra: Hour angle that converts local time to the angle
                of degrees the sun has moved across the sky.
        
        """
        # Convert declination, latitude, and HRA to radians
        d_rad = math.radians(self._declination)
        hra_rad = math.radians(hra)
        lat_rad = math.radians(self._lat)

        # Calculate the arguments to go inside the inverse sine
        arg1 = math.sin(d_rad) * math.sin(lat_rad)
        arg2 = math.cos(d_rad) * math.cos(lat_rad) * math.cos(hra_rad)

        # Calculate the elevation in radians
        alpha = math.asin(arg1 + arg2)

        # Convert to degrees
        self._elevation = math.degrees(alpha)

    def _calculate_azimuth(self, hra: float):
        """Method to calculate the azimuth angle of the sun.
        Uses equation:
            azimuth = acos((sin(d)cos(lat) - cos(d)sin(lat)cos(hra))/cos(alpha))
        
        Args:
            hra: Hour angle that converts local time to the angle
                of degrees the sun has moved across the sky
            lat: Latitude of the location in degrees

        """

        # Convert from degrees to radians
        d_rad = math.radians(self._declination)
        alpha_rad = math.radians(self._elevation)
        hra_rad = math.radians(hra)
        lat_rad = math.radians(self._lat)

        arg1 = math.sin(d_rad) * math.cos(lat_rad)
        arg2 = math.cos(d_rad) * math.sin(lat_rad) * math.cos(hra_rad)
        arg3 = math.cos(alpha_rad)

        azimuth = math.acos((arg1 - arg2) / arg3)

        if hra > 0:
            self._azimuth = 360 - math.degrees(azimuth)
        else:
            self._azimuth = math.degrees(azimuth)

    def _calculate_tc(self, d_time_zone, day_of_year):
        
        lstm = 15 * d_time_zone # Hours?
        
        B = (360/365)*(day_of_year - 81) # Degrees
        B_rad = math.radians(B) # Radians
        
        EoT_min = 9.87*math.sin(2*B_rad) - 7.53*math.cos(B_rad)-1.5*math.sin(B_rad)
        
        tc = 4 * (self._long - lstm) + EoT_min        
        
        return tc, EoT_min
