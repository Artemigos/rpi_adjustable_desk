import RPi.GPIO as gpio

def up_off():
    print("[debug] turning UP engines off")
    _OUT.left_up.off()
    _OUT.RIGHT_UP.off()

def up_on():
    print("[debug] turning UP engines on")
    _OUT.left_down.off()
    _OUT.right_down.off()

    _OUT.main.on()
    _OUT.left_up.on()
    _OUT.right_up.on()

def down_off():
    print("[debug] turning DOWN engines off")
    _OUT.left_down.off()
    _OUT.right_down.off()

def down_on():
    print("[debug] turning DOWN engines on")
    _OUT.left_up.off()
    _OUT.right_up.off()

    _OUT.main.on()
    _OUT.left_down.on()
    _OUT.right_down.on()

def all_off():
    print("[debug] turning all engines off")
    _OUT.main.off()
    _OUT.left_up.off()
    _OUT.right_up.off()
    _OUT.left_down.off()
    _OUT.right_down.off()

def initialize(outputs):
    global _OUT
    _OUT = outputs
    all_off()

