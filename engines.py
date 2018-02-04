import RPi.GPIO as gpio

def up_off():
    print("[debug] turning UP engine off")
    gpio.output(_UP_PIN, _OFF_STATE)

def up_on():
    print("[debug] turning UP engine on")
    gpio.output(_DOWN_PIN, _OFF_STATE)
    gpio.output(_UP_PIN, _ON_STATE)

def down_off():
    print("[debug] turning DOWN engine off")
    gpio.output(_DOWN_PIN, _OFF_STATE)

def down_on():
    print("[debug] turning DOWN engine on")
    gpio.output(_UP_PIN, _OFF_STATE)
    gpio.output(_DOWN_PIN, _ON_STATE)

def initialize(up_pin, down_pin, on_state=0):
    global _UP_PIN
    global _DOWN_PIN
    global _ON_STATE
    global _OFF_STATE
    _UP_PIN = up_pin
    _DOWN_PIN = down_pin
    _ON_STATE = on_state
    _OFF_STATE = 1 - on_state
    up_off()
    down_off()

