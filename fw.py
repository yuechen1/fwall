# pylint: disable=C0103
# pylint: disable=C1001
# pylint: disable=R0903
# pylint: disable=C0301
import sys
from netaddr import IPNetwork, IPAddress

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
        self.addresses = addr
        self.port = por.split(',')
        self.flag = fl

    def inrange(self, adder, por):
        """see if incoming address is in this rules range"""
        if IPAddress(adder) in IPNetwork(self.addresses):
            if por in self.port:
                self.tostring(por)
                return True
            return False
        else:
            return False

    def tostring(self, por):
        """print the rule when something goes through"""
        print '{2}({1}) {0} {3} {4} {5}\n'.format(self.direction, self.linenumber, self.action, adder, por, self.flag)



#check the number of arguments
if sys.argv[1] < 2:
    sys.exit('invalid input')

#open configuration file
FILENAME = sys.argv[1]
CONFIGURATION = open("%s" % sys.argv[1], 'r')


inest = list()
innest = list()
outest = list()
outnest = list()

#read rule from file
# if it start with # then the line is droped
# if line is empty drop
# other wise keep it in the appropret list
atline = 0
for line in CONFIGURATION:
    output = line.split()
    if output == '\n':
        pass
    elif output[1][0] == '#':
        pass
    else:
        #see if the flag is there
        if len(output) == 4:
            x = RULE(output[0], atline, output[1], output[2], output[3], 0)
            if output[0] == 'in':
                innest.append(x)
            elif output[0] == 'out':
                outnest.append(x)
            else:
                pass
        #see if the flag is set
        elif len(output) == 5:
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


#get connections from console, check to see if its one of the rules
rulefound = False
while True:
    connection = raw_input()
    conn = connection.split()
    if len(conn) != 4:
        pass
    else:
        if conn[0] == 'in' and conn[3] == 0:
            for rule in innest:
                if rule.inrange(conn[1], conn[2]) == True:
                    break
        else:
            pass
