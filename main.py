import time
import subprocess

import pynput
import psutil

import helpers
import configuration as cfg


class KeyPressListener:

    def __init__(self):
        pass


class Server:

    def __init__(self):
        pass

    def loop_event(self):
        pass


def run():

    print(" --- SERVICE STARTED --- ")

    # check Steam process
    if helpers.get_active_processes(["Steam.exe"]):
        print("Steam process has been found.")
    else:
        print("Steam process NOT DETECTED!\nLaunching Steam...")
        helpers.launch_process(cfg.STEAM_LOCATION)
        print("Steam launched.")

    # check PUBG status
    if helpers.check_game_status(cfg.GAME_PROCESSES):
        game = helpers.get_main_process(cfg.GAME_PROCESSES)
        print("Game process has been found.")
    else:
        print("Game process NOT DETECTED!")
        helpers.launch_process(f"{cfg.STEAM_LOCATION} -applaunch {cfg.PUBG_ID}")
        helpers.countdown("Launching game",
                          cfg.WAITING_FOR_LAUNCH,
                          lambda: helpers.check_game_status(cfg.GAME_PROCESSES))
        game = helpers.get_main_process(cfg.GAME_PROCESSES)
        if game is None:
            helpers.countdown("Error: unable to start the game! Terminate in", 5, shutdown=True)
        else:
            print("Game launched.")

    # handle main loop
    server = Server()

    while game.is_running():
        server.loop_event()
    else:
        helpers.countdown("Game process terminated. Shutdown at", 3, shutdown=True)


if __name__ == "__main__":
    run()
