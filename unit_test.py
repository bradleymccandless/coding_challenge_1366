import asyncio
from aiohttp import web
import json
import random

async def camera(request):
    delay = 0 #random.randint(0, 60) #create a random delay for timeout testing
    await asyncio.sleep(delay)
    images = []
    # on average 5000 images per camera for testing 10million images
    for image in range(1,random.randint(2, 10001)):
        #images randomly sized anywhere from 1B to 1MB
        image_size = random.randint(1,1000001)
        images.append({ 'file_size' : image_size })
    data = {'camera_id': int(request.match_info['id']), 'images':images}
    return web.json_response(data)

app = web.Application()
app.add_routes([web.get('/camera/{id}', camera)])

if __name__ == '__main__':
    web.run_app(app)