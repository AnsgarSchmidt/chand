import paho.mqtt.publish as publish

class HandTranslate:

    def __init__(self):
        self._command_list = {"highFive":[4,4,4,4,4],
                              "Victory" :[0,4,4,0,0],
                              "Time"    :[0,0,0,0,0],
                              "Devil"   :[0,4,0,0,4],
                              "Bird"    :[0,0,4,0,0],
                              "DrEvil"  :[0,0,0,0,4]
                             }
        self._finger_name = ["Thump","Index","Middle","Ring","Pinkie"]
        self._version = 0.01

    def getVersion(self):
        return self._version

    def getHandHelp(self):
        return "Hand help text blub"

    def getHandCommands(self):
        return self._command_list.keys()

    def translate(self, command):
        if command not in self._command_list:
            raise NotImplementedError("Command not implemented")
        rlist = []
        for i in range(5):
            rlist.append(("Hand/"+self._finger_name[i], self._command_list[command][i]))
        return rlist

if __name__ == "__main__":
    print "Testing Hand translate"
    myHand = HandTranslate()
    print myHand.getHandHelp()
    for i in myHand.getHandCommands():
        print "Command for controlling the hand: %s" % i
    for i in myHand.translate("Bird"):
        publish.single(i[0], i[1], hostname="c-beam.cbrp3.c-base.org")
