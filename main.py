import asyncio
import utility
import light_behaviour as lb
from kasa import Discover, SmartBulb
from typing import List


kitchen_light_device_name = 'kitchen light '

async def init_lights() -> List[SmartBulb] :
    target = get_broadcast_address()
    found_devices = await Discover.discover(target=target)

    kitchen_light_one: SmartBulb = None
    kitchen_light_two: SmartBulb = None
    kitchen_light_three: SmartBulb = None
    
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
    ip_address:str = utility.get_ip_address()
    quartets = ip_address.split('.')
    target = quartets[0] + '.' + quartets[1] + '.' + quartets[2] + '.255'
    return target

async def run_app():
    lights: List[SmartBulb] = await init_lights()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(lb.lava_lamp_mode(lights[0]))
        tg.create_task(lb.lava_lamp_mode(lights[1]))
        tg.create_task(lb.lava_lamp_mode(lights[2]))


asyncio.run(run_app())