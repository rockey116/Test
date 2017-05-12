#   _____                _        __     _
#  /__   \_ __ __ _  ___| | __ /\ \ \___| |_
#    / /\/ '__/ _` |/ __| |/ //  \/ / _ \ __|
#   / /  | | | (_| | (__|   '/ /\  /  __/ |_
#   \_\  |_|  \__,_|\___|_|\_\_\ \_\\___|\__|
#
# Copyright (c) 2016 Trackio International AG
# All rights reserved.
#

import asyncio
import ujson
import websockets

async def test(uri, ownerid):
    try:
        print(uri)
        async with websockets.connect(uri) as aws:
            req={"owner": ownerid}
            await aws.send(ujson.dumps(req))
            print("> {}".format(req))
            res = await aws.recv()
            print("< {}".format(res))
            res = ujson.loads(res)
            uri = res["appx_list"][0]["uri"]
        print(uri)
        aws = await websockets.connect(uri)
        while True:
            print("Waiting for data from APPX for ownerid=%s ..." % ownerid)
            m = await aws.recv()
            print(m)
    except asyncio.CancelledError:
        print("CanceledError")
        raise
    except Exception as exc:
        print('Got exception! %s' % exc)
        raise

# ------------------------------------------------------------        
URI = 'ws://rc.dev.tracknet.io:7000/owner-info'
OWNER = "c::1"
task = asyncio.ensure_future(test(URI,OWNER))
asyncio.get_event_loop().run_forever()
