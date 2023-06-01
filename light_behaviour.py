import asyncio
from kasa import SmartBulb
from random import randint

async def pulse_light_forever(light: SmartBulb, sleep_time_sec: float):
    while True:
        await light.turn_on(transition=1)
        await asyncio.sleep(sleep_time_sec)
        await light.turn_off(transition=1)
        await asyncio.sleep(sleep_time_sec)

async def lava_lamp_mode(light: SmartBulb):
    hue_change_amount = 5
    hue = randint(0, 360)
    num_iter_until_reverse = randint(20,100)

    iter_count = 0
    add_to_hue = True

    while True:
        await light.set_hsv(hue, 100, 100)
        iter_count += 1
        await asyncio.sleep(0.02)

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
    while True:
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

