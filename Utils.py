# ############################################################
# Debugging
# ------------------------------------------------------------
# Debug bits:
#   000 - (0) No debug messages       
#   001 - (2) Error messages          
#   010 - (4) Trace messages          
#   100 - (8) Informational messages
NO_DBG  = 0
ERR_DBG = 2
INF_DBG = 4

DBGMASK = NO_DBG

def dbgPrint(nDbgLvl, sDbgMsg):
    if (nDbgLvl & DBGMASK):
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




