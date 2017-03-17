class rule:
    """to hold all the rules"""
    str direction = 'in'
    str action = 'drop'
    str ports = '*'
    bool flag = False

    def __init__(self, dirt, act, po, fl):
        self.direction = dirt
        self.action = act
        self.ports = po
        self.flag = fl

    def inrange(self, port):
        