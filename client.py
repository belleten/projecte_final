"""
NFCBeer
Usage:
 nfcbeer.py client <id>
 nfcbeer.py server
 nfcbeer.py [-h | --help]
Options:
 -h --help      Shows help
"""
from docopt import docopt
import time
import RPi.GPIO as GPIO
import random
import MFRC522
import sys
import zmq

context = zmq.Context()
sock = context.socket(zmq.REQ)
sock.connect("tcp://127.0.0.1:5678")

class NFCReader(object):

    def __init__(self):
        self.uid = None
	self.nfc = MFRC522.MFRC522()

    def is_card_present(self):
	(status,TagType) = self.nfc.MFRC522_Request(self.nfc.PICC_REQIDL)
	return status ==  self.nfc.MI_OK

    def read_uid(self):
	(status,uid) = self.nfc.MFRC522_Anticoll()
	uid = "".join(format(x, '02x')for x in uid)
        return uid


class FlowControl(object):
    """Controlling FlowControl"""
    def __init__(self, nfc=None, server=None):
        super(FlowControl, self).__init__()
        self.previousTime = 0
        self.service = 0
        self.total = 0
        self.user = -2
        self.nfc = nfc
        self.server = server
	self.id = sys.argv[2]

    def _get_user(self):
        if self.nfc is not None:
            if self.nfc.is_card_present():
                return self.nfc.read_uid()
        return "None"

    def update(self, channel):
        tim = time.time()
        delta = tim - self.previousTime
        if delta < 0.50:
            self.hertz = 1000.0 / delta
            self.flow = self.hertz / 450.0  # Liter/Second
            service = self.flow * (delta / 1000.0)
            self.service  += service
            self.total    += service
        else:
            if self.user != -2:
                print "User", self.user, " drank ", round(self.service, 3)
                print "-" * 60
                mesura = str(round(self.service, 3)) + "," + str(self.user)+ "," + str(self.id)
                sock.send(mesura)
                c = sock.recv()
                print c
            self.service = 0
            self.user = self._get_user()

        self.previousTime = tim

    def _debug_dump(self):
        print "+" * 40
	print "DBG: TOTAL: ", round(self.total,3), "Servei:", round(self.service,3)
	print "+" * 40


class BeerControl(object):
    """Control KEG"""
    def __init__(self):
        super(BeerControl, self).__init__()

    def run(self):
        nf = NFCReader()
        fl = FlowControl(nfc=nf)

        GPIO.setmode(GPIO.BOARD) # use real GPIO numbering
        GPIO.setup(16,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(16, GPIO.RISING, callback=fl.update, bouncetime=20)
	try:
		while True:
			time.sleep(15)
			fl._debug_dump()

	except:
		GPIO.cleanup()


if __name__ == "__main__":
    arguments = docopt(doc=__doc__, version="NFCBEER 1.0")
    print arguments
    if arguments["client"]:
        c = BeerControl()
        c.run()
