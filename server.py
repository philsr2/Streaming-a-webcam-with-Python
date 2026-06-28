import asyncio
import websockets

clients = set()

async def handler(ws):
    clients.add(ws)
    try:
        async for msg in ws:
            # broadcast to all connected clients
            for c in clients:
                if c != ws:
                    await c.send(msg)
    finally:
        clients.remove(ws)
    #
    # that clients.remove needs to be in a try/except block too
    #
async def main():
    # the server listens on all IPs this server has, might need to change that
    # my server is very locked down as to what IP's can connect to it on
    # this port.
    #
    async with websockets.serve(handler, "0.0.0.0", 5000):
        await asyncio.Future()

asyncio.run(main())
