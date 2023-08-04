# File containing constants that configure the script's operation,
# intended for manual editing in an editor.

# Path to the executable file of the Steam application store differs for different users
STEAM_LOCATION = r"S:\Software\Steam\steam.exe"

# PUBG: BATTLEGROUNDS Steam AppID
# It may change over time, and if there is an issue with an incorrect identifier,
# it should be corrected when unable to launch game using the script.
PUBG_ID = 578080

# List of Windows processes, presence of which in the list of running processes
# indicates correct operation of game.
GAME_PROCESSES = ["TslGame.exe",
                  "TslGame.exe",
                  "ExecPubg.exe",
                  "zksvc.exe"]

# Maximum waiting time, after which, in case any of specified game processes are absent,
# game will be considered as not working correctly or not launched.
WAITING_FOR_LAUNCH = 30
