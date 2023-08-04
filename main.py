import time

import pynput

import helpers
import configuration as cfg


class KeyPressHandler:

    def __init__(self):
        self.mouse_listener = pynput.mouse.Listener(self.mouse_move, self.mouse_click, self.mouse_scroll)
        self.keyboard_listener = pynput.keyboard.Listener(self.keyboard_press, self.keyboard_release)
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def mouse_move(self, x, y):
        print(f"mouse move at: x:{x}, y:{y}")

    def mouse_click(self, x, y, button, pressed):
        print("{0} button {1} at x: {2}, y: {3}".format(button, "pressed" if pressed else "released", x, y))

    def mouse_scroll(self, x, y, dx, dy):
        print("Scrolled {0} at {1}".format("down" if dy < 0 else "up", (x, y)))

    def keyboard_press(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed'.format(key))

    def keyboard_release(self, key):
        print('{0} released'.format(key))


class Server:

    def __init__(self):
        self.keypress_handler = KeyPressHandler()

    def loop_event(self):
        time.sleep(0.001)


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
