from socketio import AsyncClient
import asyncio
from json import dumps
from base64 import b64encode
import hmac as sinricHmac
from hashlib import sha256
from aioconsole import ainput

class VanetClient:
    def __init__(self,sio: AsyncClient, IpAddress, secretKey):
        self.sio = sio
        self.secretKey = secretKey
        self.IpAddress = IpAddress
        pass

    async def connectToServer(self):
        await self.sio.connect(self.IpAddress)
        await self.sio.wait()
    
    def getSignature(self, payload):
        replyHmac = sinricHmac.new(self.secretKey.encode('utf-8'),
                                   dumps(payload, separators=(',', ':'), sort_keys=True).encode('utf-8'), sha256)

        encodedHmac = b64encode(replyHmac.digest())

        return encodedHmac.decode('utf-8')
        


if __name__ == '__main__':
# -----------------=-------------------------=-------------------=-------------=- 
# -----------------=-------------------------=-------------------=-------------=- 
    
    IpAddress = '192.168.29.151'
    
    PORT = '8080'

    clientName = 'Iron Man'
    
    roomName = 'banglore'

    secretKey = 'fucksit'

    messageToSend = 'One life One love One destiny'

# -----------------=-------------------------=-------------------=-------------=- 
# -----------------=-------------------------=-------------------=-------------=- 

    sio = AsyncClient()
    FullIp = 'http://'+IpAddress+':'+PORT
    ob = VanetClient(sio, FullIp, secretKey)

    @sio.event
    async def connect():
        print('Connected to sever')
        await sio.emit('join_chat', {'room': roomName,'name': clientName})
    
    @sio.event
    async def get_message(message):
        print(message)

    async def send_message():
        while True:
            await asyncio.sleep(0.01)
            messageToSend = await ainput()
            await sio.emit('send_chat_room', {'message': messageToSend,'name': clientName, 'room': roomName, 
                'signature': ob.getSignature({'message':messageToSend})})

    async def main(IpAddress):
         await asyncio.gather(
        ob.connectToServer(),
        send_message()
        )
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(FullIp))