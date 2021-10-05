class Player:
    def __init__(self, player_id, prop):
        self.player_id = player_id
        self.player_id_str = str(player_id)
        
        self.connect = prop['connect'] #{'connect': False, 'img': None, 'name': None, 'level': 1, 'points': 0, 'inventory': {}, 'location': '', 'sys_event': False}
        self.name = prop['name']
        self.img = prop['img']
        self.level = prop['level']
        self.points = prop['points']
        self.inventory = prop['inventory']
        self.location = prop['location']
        self.sys_event = 'none'
        
        self.changes = False
    
    def return_prop(self):
        prop = {'connect': self.connect, 'img': self.img, 'name': self.name, 'level': self.level, 'points': self.points, 'inventory': self.inventory, 'location': self.location, 'sys_event': self.sys}
        return prop
    
    def return_prop_str(self):
        return str(self.return_prop())
    
    def is_connect(self):
        return self.connect != False
    
    def companion(self):
        return self.connect
    
    def disconnect(self):
        self.connect = False
    
    def have_change(self):
        self.changes = True
    
    def is_change(self):
        return self.changes
    
    def event_passed(self):
        self.sys_event = 'none'
    