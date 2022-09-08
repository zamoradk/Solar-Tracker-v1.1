

class PanelPosition:
    
    def __init__(self, ang_velocity, init_angle):
                 
        self._angle = init_angle # degrees
        
        self._ang_velocity = ang_velocity # deg / s
    
        # On initialization, turn panels to a specific position?
    
    @property
    def angle(self):
        return self._angle
    
    def update_angle(self, desired_angle):
            
        # Make the panel go 10 degrees ahead of the sun
        final_angle = desired_angle + 10
        delta_angle = abs(final_angle - self._angle)
        
        if final_angle > self._angle:
            direction = 'cw'
        else:
            direction = 'ccw'

        on_time = delta_angle / self._ang_velocity
        
        self._angle = final_angle
        
        return on_time, direction