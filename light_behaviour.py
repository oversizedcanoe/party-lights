import asyncio
from kasa import SmartBulb
from random import randint

stop_event = None

async def pulse_light_forever(light: SmartBulb, sleep_time_sec: float):
    global stop_event
    while not stop_event.is_set():
        await light.turn_on(transition=1)
        await asyncio.sleep(sleep_time_sec)
        await light.turn_off(transition=1)
        await asyncio.sleep(sleep_time_sec)

async def rave_mode(light: SmartBulb):
    await _flow_through_colors(light, 10, 0.01)

async def lava_lamp_mode(light: SmartBulb):
    await _flow_through_colors(light, 5, 0.4)

async def _flow_through_colors(light: SmartBulb, hue_change_amount: int, sleep_time_ms: float):
    hue_change_amount = hue_change_amount
    hue = randint(0, 360)

    max_iter = 360 / hue_change_amount
    num_iter_until_reverse = randint(int(max_iter/2), int(max_iter))

    iter_count = 0
    add_to_hue = True

    global stop_event
    while not stop_event.is_set():
        await light.set_hsv(hue, 100, 100)
        iter_count += 1
        await asyncio.sleep(sleep_time_ms)

        if add_to_hue:
            hue += hue_change_amount
            if hue > 360:
                hue = 0
        else:
            hue -= hue_change_amount
            if hue < 0:
                hue = 360

        if iter_count > num_iter_until_reverse:
            add_to_hue = not add_to_hue
            iter_count = 0
            num_iter_until_reverse = randint(20,100)

async def flash_random_colors(light: SmartBulb):

    global stop_event
    while not stop_event.is_set():
        hue = randint(0, 360)
        await light.set_hsv(hue, 100, 100)
        await light.turn_on(transition=1)
        await asyncio.sleep(0.1)
        await light.turn_off(transition=1)
        await asyncio.sleep(0.1)

# sets to warm white/yellow
async def return_to_normal(light: SmartBulb):
    await light.set_color_temp(2700)
    await light.set_brightness(25)
    await light.set_hsv(0, 0, 25) 
    await light.turn_on()

