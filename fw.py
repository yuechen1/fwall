# pylint: disable=C0103
# pylint: disable=C1001
# pylint: disable=R0903
# pylint: disable=C0301
import sys
import ipaddress

class RULE:
    """"to hold the rule, the direction of packet and establishment is not kept here"""
    direction = 'in'
    linenumber = 0
    action = 'drop'
    addresses = '*'
    port = list()
    flag = 0

    def __init__(self, dire, number, act, addr, por, fl):
        self.direction = dire
        self.linenumber = number
        self.action = act
        if addr == '*':
            self.addresses = addr
        else:
            try:
                self.addresses = ipaddress.IPv4Network(addr, False)
            except ValueError:
                print(':',addr)
        self.port = por.split(',')
        self.flag = fl

    def inrange(self, adder, por, flae):
        """see if incoming address is in this rules range"""
        try:
            tempadr = ipaddress.ip_address(adder)
        except ValueError:
            print('not a valid address: ', adder)
        if self.addresses == '*':
            if '*' in self.port:
                self.tostring(adder, por, flae)
                return True
            elif por in self.port:
                self.tostring(adder, por, flae)
                return True
        elif tempadr in self.addresses:
            if '*' in self.port:
                self.tostring(adder, por, flae)
                return True
            elif por in self.port:
                self.tostring(adder, por, flae)
                return True
            return False
        else:
            return False

    def tostring(self, adder, por, flae):
        """print the rule when something goes through"""
        print ("{2}({1}) {0} {3} {4} {5}".format(self.direction, self.linenumber, self.action, adder, por, flae))

    def printself(self):
        """print the rule out, for debuging only"""
        print ("{0} {1} {2} {3} {4} {5}".format(self.direction, self.linenumber, self.action, self.addresses, self.port, self.flag))



#check the number of arguments
if len(sys.argv) < 2:
    sys.exit('invalid input')

#open configuration file
FILENAME = sys.argv[1]
CONFIGURATION = open("%s" % sys.argv[1], 'r')


inest = []
innest = []
outest = []
outnest = []

#read rule from file
# if it start with # then the line is droped
# if line is empty drop
# other wise keep it in the appropret list
atline = 1
for line in CONFIGURATION:
    output = line.split()
    if not (len(output) == 4 or len(output) == 5):
        pass
    elif output[0][0] == '#':
        pass
    else:
        #see if the flag is there
        if len(output) == 4:
            x = RULE(output[0], atline, output[1], output[2], output[3], 0)
            if output[0] == 'in':
                innest.append(x)
                inest.append(x)
            elif output[0] == 'out':
                outnest.append(x)
                outest.append(x)
            else:
                pass
        #see if the flag is set
        elif len(output) == 5 and output[4] == 'established':
            if output[4] == 'established':
                x = RULE(output[0], atline, output[1], output[2], output[3], 1)
                if output[0] == 'in':
                    inest.append(x)
                elif output[0] == 'out':
                    outest.append(x)
        #not a comment and not a rule
        else:
            pass
        #increment line number
    atline += 1


#debuging stuff
#print('in and not established')
#for rule in innest:
#    rule.printself()
#print('in and established')
#for rule in inest:
#    rule.printself()
#print('out and not established')
#for rule in outnest:
#    rule.printself()
#print('out and established')
#for rule in outest:
#    rule.printself()



#get connections from console, check to see if its one of the rules
rulefound = False
for connection in sys.stdin:
    conn = connection.split()
    if len(conn) != 4:
        print(len(conn))
        pass
    else:
        if conn[0] == 'in' and conn[3] == '0':
            for rule in innest:
                rulefound = rule.inrange(conn[1], conn[2], conn[3])
                if rulefound:
                    break
            if not rulefound:
                print("drop() {0} {1} {2} {3}".format(conn[0], conn[1], conn[2], conn[3]))
        elif conn[0] == 'in' and conn[3] == '1':
            for rule in inest:
                rulefound = rule.inrange(conn[1], conn[2], conn[3])
                if rulefound:
                    break
            if not rulefound:
                print("drop() {0} {1} {2} {3}".format(conn[0], conn[1], conn[2], conn[3]))
        elif conn[0] == 'out' and conn[3] == '0':
            for rule in outnest:
                rulefound = rule.inrange(conn[1], conn[2], conn[3])
                if rulefound:
                    break
            if not rulefound:
                print("drop() {0} {1} {2} {3}".format(conn[0], conn[1], conn[2], conn[3]))
        elif conn[0] == 'out' and conn[3] == '1':
            for rule in outest:
                rulefound = rule.inrange(conn[1], conn[2], conn[3])
                if rulefound:
                    break
            if not rulefound:
                print("drop() {0} {1} {2} {3}".format(conn[0], conn[1], conn[2], conn[3]))
        else:
            print("drop() {0} {1} {2} {3}".format(conn[0], conn[1], conn[2], conn[3]))
