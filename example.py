from vanetSign import Signature

if __name__ == '__main__':

    secret = 'somethingsecretKey'
    
    signOb = Signature(secret)

    data = {
        'name': 'yourname',
        'message': 'some message'
    }

    signedData = signOb.getSignature(data)

    print(signedData)
    
    print(signOb.verifySignature(data, signedData['HMAC']))
