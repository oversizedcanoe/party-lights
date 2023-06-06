import asyncio
import utility
import light_behaviour as lb
from kasa import Discover, SmartBulb
from typing import List

inited_lights = []
kitchen_light_device_name = 'kitchen light '

allowed_behaviours = ['flashRandom', 'raveMode', 'lavaLampMode', 'reset']

async def init_lights() -> List[SmartBulb]:
    global inited_lights
    if len(inited_lights) == 0:

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

        inited_lights = [kitchen_light_one, kitchen_light_two, kitchen_light_three]
    else:
        print("lights already init'd")
    return inited_lights

def get_broadcast_address() -> str:
    ip_address:str = utility.get_ip_address()
    quartets = ip_address.split('.')
    target = quartets[0] + '.' + quartets[1] + '.' + quartets[2] + '.255'
    return target

async def run_app(func):
    print('Run App called with func: ' + str(func))
    lights: List[SmartBulb] = await init_lights()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(func(lights[0]))
        tg.create_task(func(lights[1]))
        tg.create_task(func(lights[2]))

async def run_behaviour(behaviour):
    if behaviour not in allowed_behaviours:
        raise Exception(f'Behaviour "{behaviour}" not allowed.')
    
    match behaviour:
        case 'flashRandom':
            func = lb.flash_random_colors
        case 'raveMode':
            func = lb.rave_mode
        case 'lavaLampMode': 
            func = lb.lava_lamp_mode
        case 'reset', _:
            func = lb.return_to_normal

    lights: List[SmartBulb] = await init_lights()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(func(lights[0]))
        tg.create_task(func(lights[1]))
        tg.create_task(func(lights[2]))

if __name__ == '__main__':
    asyncio.run(run_app(lb.lava_lamp_mode))