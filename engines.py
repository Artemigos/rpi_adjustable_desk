import RPi.GPIO as gpio

def up_off():
    print("[debug] turning UP engines off")
    gpio.output(_LEFT_UP_PIN, _OFF_STATE)
    gpio.output(_RIGHT_UP_PIN, _OFF_STATE)

def up_on():
    print("[debug] turning UP engines on")
    gpio.output(_LEFT_DOWN_PIN, _OFF_STATE)
    gpio.output(_RIGHT_DOWN_PIN, _OFF_STATE)

    gpio.output(_MAIN_PIN, _ON_STATE)
    gpio.output(_LEFT_UP_PIN, _ON_STATE)
    gpio.output(_RIGHT_UP_PIN, _ON_STATE)

def down_off():
    print("[debug] turning DOWN engines off")
    gpio.output(_LEFT_DOWN_PIN, _OFF_STATE)
    gpio.output(_RIGHT_DOWN_PIN, _OFF_STATE)

def down_on():
    print("[debug] turning DOWN engines on")
    gpio.output(_LEFT_UP_PIN, _OFF_STATE)
    gpio.output(_RIGHT_UP_PIN, _OFF_STATE)

    gpio.output(_MAIN_PIN, _ON_STATE)
    gpio.output(_LEFT_DOWN_PIN, _ON_STATE)
    gpio.output(_RIGHT_DOWN_PIN, _ON_STATE)

def all_off():
    print("[debug] turning all engines off")
    gpio.output(_MAIN_PIN, _OFF_STATE)
    gpio.output(_LEFT_UP_PIN, _OFF_STATE)
    gpio.output(_RIGHT_UP_PIN, _OFF_STATE)
    gpio.output(_LEFT_DOWN_PIN, _OFF_STATE)
    gpio.output(_RIGHT_DOWN_PIN, _OFF_STATE)

def initialize(
        main_pin,
        left_up_pin,
        left_down_pin,
        right_up_pin,
        right_down_pin,
        on_state=0):
    global _MAIN_PIN
    global _LEFT_UP_PIN
    global _LEFT_DOWN_PIN
    global _RIGHT_UP_PIN
    global _RIGHT_DOWN_PIN
    global _ON_STATE
    global _OFF_STATE
    _MAIN_PIN = main_pin
    _LEFT_UP_PIN = left_up_pin
    _LEFT_DOWN_PIN = left_down_pin
    _RIGHT_UP_PIN = right_up_pin
    _RIGHT_DOWN_PIN = right_down_pin
    _ON_STATE = on_state
    _OFF_STATE = 1 - on_state
    all_off()

