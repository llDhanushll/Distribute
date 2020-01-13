import asyncio
import time
import socketio
from aioconsole import ainput
from vanetSign import Signature
from secret_key import secretKey

loop = asyncio.get_event_loop()
sio = socketio.AsyncClient()
start_timer = None

IP = '192.168.29.151'
PORT = '8080'

@sio.event
async def connect():
    print('connected to server')
    await sio.emit('join_chat', {'room': 'some_room'})

async def start_client():
    await sio.connect('http://'+IP+':'+PORT)
    await sio.wait()

@sio.event
async def get_message(message):
    print(message)

async def send_message():
    ob = Signature(secretKey)
    while True:
        await asyncio.sleep(0.01)
        k = await ainput()
        await sio.emit('send_chat_room', {'message': k, 'room': 'some_room', 'signature': ob.getSignature({'message':k})})


async def main():

    await asyncio.gather(
        start_client(),
        send_message()
    )

if __name__ == '__main__':
    loop.run_until_complete(main())
