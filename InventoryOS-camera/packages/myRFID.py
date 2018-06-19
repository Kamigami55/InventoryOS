from __future__ import print_function
from .MFRC522 import MFRC522


userList = [
    {'uid' : [152,44,161,89], 'name' : 'BlueGuy'}
]


class RFIDReader():

    def __init__(self):

        self.MIFAREReader = MFRC522()
        self.currentUser = None


    def read(self):
        # Scan for cards
        MIFAREReader = self.MIFAREReader
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        if status == MIFAREReader.MI_OK:
            # card is found
            # Get the UID of the card
            (status,uid) = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK:
                # found UID
                # Print UID
                print("Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
                for user in userList:
                    userUid = user['uid']
                    if userUid[0] == uid[0] and userUid[1] == uid[1] and userUid[2] == uid[2] and userUid[3] == uid[3]:
                        # UID matched
                        if self.currentUser != user['name']:
                            print("User changed to '%s'" % user['name'])
                            self.currentUser = user['name']
                            return self.currentUser
                        break

        return None



