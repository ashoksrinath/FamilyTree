# ############################################################
# Debugging
# ------------------------------------------------------------
# Debug levels:
#   0 - No debug messages
#   1 - Some debug messages
#   2 - Many debug messages
NO_DBG  = 0
ERR_DBG = 1
TRC_DBG = 2

DBGLVL  = NO_DBG

def dbgPrint(sDbgMsg, nDbgLvl):
    if (DBGLVL >= nDbgLvl):
        print (sDbgMsg)

    return

# end def dbgPrint



# ############################################################
# Wait for it...
# -------------------------------------------------------------
def pause(sPrompt):
    sReturn = input (sPrompt)
    return;

# end def pause() ############################################




