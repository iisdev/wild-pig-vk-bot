MAX_WEIGHT = 4

class Player:
    def __init__(self, player_id, prop):
        self.player_id = player_id
        self.player_id_str = str(player_id)
        
        self.connect = prop['connect'] #{'connect': False, 'img': None, 'name': None, 'level': 1, 'points': 0, 'inventory': {}, 'location': '', 'other': {}}
        self.name = prop['name']
        self.img = prop['img']
        self.level = prop['level']
        self.points = prop['points']
        self.inventory = prop['inventory'] # max lot: 3 lots: 4
        self.location = prop['location'] 
        self.other = prop['other']
        
        
        self.sys_event = 'none'
        self.changes = False
        self.trade_buff = []
        
    
    def return_prop(self):
        prop = {'connect': self.connect, 'img': self.img, 'name': self.name, 'level': self.level, 'points': self.points, 'inventory': self.inventory, 'location': self.location, 'other': self.other}
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
    
     # INVENTORY
    
    def return_inventory(self):
        inv = "Твой инвентарь:"
        if len(self.inventory) == 0:
            inv += ' пуст...'
        else:
            for item in self.inventory:
                count = self.inventory[item]
                inv += '\n - '+ item + ': ' + str(count) + ' шт.'
        return inv
    
    def inventory_weight(self):
        items = self.inventory
        weight = 0
        for item in items:
            weight += items[item]
        
        return weight
    
    def have_item(self, item):
        return item in self.inventory
    
    def delete_item(self, item):
        items = self.inventory
        if not(item in items):
            return False
        
        items[item] -= 1
        
        if items[item] == 0:
            del items[item]
        
        return True
    
    def get_item(self, item):
        items = self.inventory
        
        weight = self.inventory_weight()
        if weight == MAX_WEIGHT:
            return (False, 'У тебя перегруз!')
            
        if item in items:
            items[item] += 1
        else:
            items[item] = 1
        return (True,)
    
    # TRADE_BUFFER
        
    