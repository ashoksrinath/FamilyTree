# CIS 41B
# DeAnza College, Winter 2020
# Ashok Srinath
# -----
import socket
import sys

DEBUG = False

class Sockit(object):
    """General purpose socket client/server class """

    # ********************
    # Initializes instance
    # ********************
    def __init__(self, host=None, port=None, sock=None, addr=None):

        self.sHost      = host
        self.nPort      = port
        self.sock       = sock
        self.tplAddr    = addr

        self.nBACKLOG   = 7
        self.nPRFXLEN   = 6

        self.newsock    = None
        self.newaddr    = None

        if self.sock == None:
            self.create()

        return

    # end __init__ ()
    
    # ***************************
    # Accepts connection requests
    # ***************************
    def accept(self):

        if self.sock != None:
            self.newsock, self.newaddr = self.sock.accept()

            sockit = Sockit (sock=self.newsock, addr=self.newaddr)
            return sockit
        elif DEBUG:
            print("Sockit.accept - socket address not constructed")
            return None

    # end accept()

    # ***********************************************
    # Binds to host and port, sets connection backlog
    # ***********************************************
    def bind(self):

        if self.tplAddr == None:
            self.tplAddr = (self.sHost, self.nPort)

        try:
            self.sock.bind(self.tplAddr)
            self.sock.listen(self.nBACKLOG)
            if DEBUG:
                print("Sockit.bind - listening for connection-requests on {}:{}".format(*self.tplAddr))
        except Exception as exEcution:
            print("Sockit.bind - error", exEcution)

        return

    # end bind()

    # ************************
    # Disconnects from session
    # ************************
    def close(self):

        if self.sock:
            try:
                self.sock.close()
                if DEBUG:
                    print("Sockit.close - success")
            except Exception as exEcution:
                print("Sockit.close - error", exEcution)

        elif DEBUG:
            print("Sockit.close - nothing to close")

        return

    # end close()

    # ******************
    # Connects to server
    # ******************
    def connect(self):

        if self.tplAddr == None:
            self.tplAddr = (self.sHost, self.nPort)

        try:
            self.sock.connect(self.tplAddr)
            if DEBUG:
                print("Sockit.connect - connected to {}:{}".format(*self.tplAddr))
            return True
        except Exception as exEcution:
            print("Sockit.connect - error", exEcution)

        return False

    # end connect()

    # **************
    # Creates socket
    # **************
    def create(self):

        try:
            self.sock = socket.socket()
            if DEBUG:
                print("Sockit.create - success")
        except Exception as exEcution:
            print("Sockit.create - error", exEcution)
           
        return

    # end create()

    # *******************************
    # Receives buffer over connection
    # *******************************
    def recv(self):

        sBuff = ""

        if self.sock == None:
            print("Sockit.recv - invalid socket")
            return sBuff
        elif DEBUG:
            print("Sockit.recv - starting to receive")

        try:
            rMsgSize = self.sock.recv(self.nPRFXLEN)
            if rMsgSize:
                sMsgSize = rMsgSize.decode()
                try:
                    nMsgSize = int(sMsgSize)
                    if DEBUG:
                        print("Sockit.recv - message size is %d" % (nMsgSize))
                    rBuff = self.sock.recv(nMsgSize)
                    if rBuff:
                        sBuff = rBuff.decode()
                        if DEBUG:
                            print("Sockit.recv - received message")
                    elif DEBUG:
                        print("Sockit.recv - failed to read message")
                except ValueError:
                    print("Sockit.recv - failed to convert message-size %d into integer" % (sMsgSize))
            elif DEBUG:
                print("Sockit.recv - failed to read message size")
        except Exception as exEcution:
            print("Sockit.recv - error", exEcution)


        return sBuff

    # end recv()


    # ****************************
    # Sends buffer over connection
    # ****************************
    def send(self, sBuff):

        if self.sock != None:
            try:
                sMsgSize = str(len(sBuff)).zfill(self.nPRFXLEN)
                if DEBUG:
                    print("Sockit.send - sending data-size", sMsgSize)
                self.sock.sendall(sMsgSize.encode())
                if DEBUG:
                    print("Sockit.send - sending data")
                self.sock.sendall(sBuff.encode())
                return True
            except Exception as exEcution:
                print("Sockit.send - error", exEcution)
                return False
        else:
            print("Sockit.send - invalid socket")
            return False

    # end send()

# end class Sockit

if __name__ == "__main__":

    bSuccess = True
    sOutBuff = ""

    if len(sys.argv) >= 2:
        sOutBuff = ""
        for nIdx in range(1, len(sys.argv)):
            sOutBuff += sys.argv[nIdx]
            if nIdx < len(sys.argv) - 1:
                sOutBuff += " "

    sockit = Sockit(host="localhost", port=8192)
    if not sockit.connect():
        bSuccess = False

    while bSuccess:
        if sOutBuff == "":
            sOutBuff = input("Command: ")
        if sOutBuff:
            print("Sending message", sOutBuff)
            if sockit.send(sOutBuff):
                sInBuff = sockit.recv()
                print("Received data of length %d:" % (len(sInBuff)))
                print(sInBuff)
            sOutBuff = ""
        else:
            bSuccess = False

    sockit.close()
        
# end __main__