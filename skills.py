class Skills:
    def __init__(self, skill_name, dxp_gained):
        self._skill_name = skill_name
        self._dxp_gained = dxp_gained
        
    @property
    def skill_name(self):
        return self._skill_name
    
    @property
    def dxp_gained(self):
        return self._dxp_gained
    
    @dxp_gained.setter
    def dxp_gained(self, dxp_gained):
        self._dxp_gained = dxp_gained