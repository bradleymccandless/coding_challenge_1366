import asyncio
import aiohttp
#this should be set using config lib so when we push to production it just works
production = 0
if production:
    proto='https'
    domain='domain.com'
    port='443'
    #change this from a generated list to a database lookup for production
    cameras = range(0,20)
    #wait up to 30 seconds for each individual request
    timeout = aiohttp.ClientTimeout(total=None,sock_read=30)
else:
    proto='http'
    domain='localhost'
    port='8080'
    #2000 cameras for testing to 10million images
    cameras = range(0,2000)
    #gotta go fast
    timeout = aiohttp.ClientTimeout(total=None,sock_read=1)
urls = []
for camera in cameras:
    urls.append(proto+'://'+domain+':'+port+'/camera/'+str(camera))
    
def most_data(dataset):
    cameras = {}
    for camera in dataset:
        total_size = 0
        for images in camera['images']:
            total_size += images['file_size']
        cameras[camera['camera_id']] = total_size
    print('Cameras that use the most data: '+str(sorted(cameras, key=cameras.get, reverse=True)[:3]))
def most_images(dataset):
    cameras = {}
    for camera in dataset:
        total_size = 0
        for images in camera['images']:
            total_size += 1
        cameras[camera['camera_id']] = total_size
    print('Cameras that have the highest number of images: '+str(sorted(cameras, key=cameras.get, reverse=True)[:3]))
def largest_image(dataset):
    cameras = {}
    print('Largest image per camera:')
    for camera in dataset:
        total_size = 0
        for images in camera['images']:
            if images['file_size'] > total_size:
                total_size = images['file_size'] 
        cameras[camera['camera_id']] = total_size
    print(cameras)
async def fetch(session, url):
    async with session.get(url, timeout=timeout) as response:
        if response.status != 200:
            response.raise_for_status()
        return await response.json()

async def fetch_all(session, urls):
    results = await asyncio.gather(*[asyncio.create_task(fetch(session, url)) for url in urls])
    return results

async def main():
    try:
        async with aiohttp.ClientSession() as session:
            results = await fetch_all(session, urls)
    except(asyncio.TimeoutError):
        #here we can do more things. Should we retry? Send an email?
        print('A request timed out.')
        exit()
    most_data(results)
    most_images(results)
    largest_image(results)
if __name__ == '__main__':
    asyncio.run(main())