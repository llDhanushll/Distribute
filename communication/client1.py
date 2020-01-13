import asyncio
import time
import socketio

loop = asyncio.get_event_loop()
sio = socketio.AsyncClient()
start_timer = None

IP = '192.168.29.142'
PORT = '8080'

async def send_ping():
    global start_timer
    start_timer = time.time()
    await sio.emit('ping_from_client')


@sio.event
async def connect():
    print('connected to server')
    await send_ping()

@sio.event
def my_response(message):
    print(message)

@sio.event
async def pong_from_server(data):
    global start_timer
    latency = time.time() - start_timer
    print('latency is {0:.2f} ms'.format(latency * 1000))
    await sio.sleep(1)
    await send_ping()

@sio.event
async def get_message(message):
    print(message)

async def start_server():
    await sio.connect('http://'+IP+':'+PORT)
    await sio.wait()



if __name__ == '__main__':
    loop.run_until_complete(start_server())
