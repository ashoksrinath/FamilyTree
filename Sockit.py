import socket
import sys
from   Utils import *

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

        if self.sock == None:
            dbgPrint(ERR_DBG, "Sockit.accept - invalid server socket")
            return None

        self.newsock, self.newaddr = self.sock.accept()
        sockit = Sockit (sock=self.newsock, addr=self.newaddr)

        return sockit

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

            dbgPrint(INF_DBG, ("Sockit.bind - listening for connection-requests on %d:%d" % \
                (self.tplAddr[0], self.tplAddr[1])))
            return(True)
        except Exception as exEcution:
            dbgPrint(ERR_DBG, ("Sockit.bind - exception %s" % repr(exEcution)))
            return(False)

    # end bind()

    # ************************
    # Disconnects from session
    # ************************
    def close(self):

        if not self.sock:
            return True

        try:
            self.sock.close()
            dbgPrint(INF_DBG, "Sockit.close - success")
            return True
        except Exception as exEcution:
            dbgPrint(ERR_DBG, ("Sockit.close - exception %s" % repr(exEcution)))
            return False

    # end close()

    # ******************
    # Connects to server
    # ******************
    def connect(self):

        if self.tplAddr == None:
            self.tplAddr = (self.sHost, self.nPort)

        try:
            self.sock.connect(self.tplAddr)
            dbgPrint(INF_DBG, ("Sockit.connect - connected to %d:%d" % \
                (self.tplAddr[0], self.tplAddr[1])))
            return True
        except Exception as exEcution:
            dbgPrint(ERR_DBG, ("Sockit.connect - exception %s" % repr(exEcution)))
            return False

    # end connect()

    # **************
    # Creates socket
    # **************
    def create(self):

        try:
            self.sock = socket.socket()
            dbgPrint(INF_DBG, "Sockit.create - success")
            return True
        except Exception as exEcution:
            dbgPrint(ERR_DBG, ("Sockit.create - exception %s" % repr(exEcution)))
            return False

    # end create()

    # *******************************
    # Receives buffer over connection
    # *******************************
    def recv(self):

        sBuff = ""

        if self.sock == None:
            dbgPrint(ERR_DBG, "Sockit.recv - invalid socket")
            return sBuff

        dbgPrint(INF_DBG, "Sockit.recv - starting to receive")
        try:
            rMsgSize = self.sock.recv(self.nPRFXLEN)
            if rMsgSize:
                sMsgSize = rMsgSize.decode()
                try:
                    nMsgSize = int(sMsgSize)
                    dbgPrint(INF_DBG, ("Sockit.recv - message size is %d" % (nMsgSize)))
                    rBuff = self.sock.recv(nMsgSize)
                    if rBuff:
                        sBuff = rBuff.decode()
                        dbgPrint(INF_DBG, "Sockit.recv - received message")
                    else:
                        dbgPrint(ERR_DBG, "Sockit.recv - failed to receive message")
                except ValueError:
                    dbgPrint(ERR_DBG, ("Sockit.recv - failed to convert message-size %s into integer" % (sMsgSize)))
            elif DEBUG:
                dbgPrint(ERR_DBG, "Sockit.recv - failed to read message size")
        except Exception as exEcution:
            dbgPrint(ERR_DBG, ("Sockit.recv - unhandled exception %s" % repr(exEcution)))


        return sBuff

    # end recv()


    # ****************************
    # Sends buffer over connection
    # ****************************
    def send(self, sBuff):

        if self.sock != None:
            try:
                sMsgSize = str(len(sBuff)).zfill(self.nPRFXLEN)
                dbgPrint(INF_DBG, ("Sockit.send - sending data-size %s" % sMsgSize))
                self.sock.sendall(sMsgSize.encode())

                dbgPrint(INF_DBG, "Sockit.send - sending data")
                self.sock.sendall(sBuff.encode())
                return True
            except Exception as exEcution:
                dbgPrint(ERR_DBG, ("Sockit.send - unhandled exception %s" % repr(exEcution)))
                return False
        else:
            dbgPrint(ERR_DBG, "Sockit.send - invalid socket")
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