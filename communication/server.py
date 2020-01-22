import asyncio
from aiohttp import web
import socketio
import hmac as sinricHmac
from hashlib import sha256
from json import dumps
from base64 import b64encode

class Signature:
    def __init__(self, secretKey):
        self.secretKey = secretKey

    def verifySignature(self, payload, signature) -> bool:
        self.myHmac = sinricHmac.new(self.secretKey.encode('utf-8'),
                                     dumps(payload, separators=(',', ':'), sort_keys=True).encode('utf-8'), sha256)
        return b64encode(self.myHmac.digest()).decode('utf-8') == signature

    def getSignature(self, payload):
        replyHmac = sinricHmac.new(self.secretKey.encode('utf-8'),
                                   dumps(payload, separators=(',', ':'), sort_keys=True).encode('utf-8'), sha256)

        encodedHmac = b64encode(replyHmac.digest())

        return encodedHmac.decode('utf-8')

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

secret_key = 'fucksit'

async def background_task():
    count = 0
    while True:
        await sio.sleep(10)
        count += 1
        await sio.emit('get_message', {'data': 'Room generated event'}, room="some_room")

@sio.event
async def join_chat(sid,message):
    print(message.get('name', sid) + ' joined to {}'.format(message['room']))
    sio.enter_room(sid, message['room'])

@sio.event
async def exit_chat(sid):
    sio.leave_room(sid, 'dazz_room')

@sio.event
async def send_chat_room(sid, message):
     ob = Signature(secret_key)
     if ob.verifySignature({'message': message['message']},message['signature']):
        await sio.emit('get_message', {'message': message['message'], 'from': sid}, room=message['room'])
     else:
        print('Signature Verification failed : ',message['name'])

@sio.event
async def connect(sid, environ):
    print(sid)
    await sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)


@sio.event
def disconnect(sid):
    print('Client disconnected')


if __name__ == '__main__':
    sio.start_background_task(background_task)
    web.run_app(app)
