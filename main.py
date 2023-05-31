import asyncio
from random import randint
import socket
from threading import Thread
from typing import List
from kasa import Discover, SmartBulb
from time import sleep


kitchen_light_device_name = 'kitchen light '

async def init_lights() -> List[SmartBulb] :
    target = get_broadcast_address()
    found_devices = await Discover.discover(target=target)

    kitchen_light_one: SmartBulb = None
    kitchen_light_two: SmartBulb = None
    kitchen_light_three: SmartBulb = None

    #print('Found ' + str(len(found_devices)) + ' devices: ' + ', '.join(found_devices.values()))

    for _, device in found_devices.items():
        if device.alias == kitchen_light_device_name + '1':
            kitchen_light_one = device
            await kitchen_light_one.update()
            print(device.alias + ' initialized')
        if device.alias == kitchen_light_device_name + '2':
            kitchen_light_two = device
            await kitchen_light_two.update()
            print(device.alias + ' initialized')
        if device.alias == kitchen_light_device_name + '3':
            kitchen_light_three = device
            await kitchen_light_three.update()
            print(device.alias + ' initialized')

    return [kitchen_light_one, kitchen_light_two, kitchen_light_three]

def get_broadcast_address() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address:str = (s.getsockname()[0])
    quartets = ip_address.split('.')
    target = quartets[0] + '.' + quartets[1] + '.' + quartets[2] + '.255'
    return target

async def pulse_light_forever(light: SmartBulb, sleep_time_sec: float):
    while True:
        await light.turn_on(transition=1)
        await asyncio.sleep(sleep_time_sec)
        await light.turn_off(transition=1)
        await asyncio.sleep(sleep_time_sec)

async def rave_mode(light: SmartBulb):
    hue_change_amount = 10
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


async def run_app():
    lights: List[SmartBulb] = await init_lights()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(flash_random_colors(lights[0]))
        tg.create_task(flash_random_colors(lights[1]))
        tg.create_task(flash_random_colors(lights[2]))


asyncio.run(run_app())


async def get_light_info(light: SmartBulb):
    print(light.alias + ' is _dimmable: ' + str(light.is_dimmable))
    print(light.alias + ' is_color: ' + str(light.is_color))
    print(light.alias + ' is_variable_color_temp: ' + str(light.is_variable_color_temp))
    print(light.alias + ' temp range: ' + str(light.valid_temperature_range))
    # results same for all three lights
    # kitchen light 1 is _dimmable: True
    # kitchen light 1 is_color: True
    # kitchen light 1 is_variable_color_temp: True
    # kitchen light 1 temp range: ColorTempRange(min=2500, max=6500)
