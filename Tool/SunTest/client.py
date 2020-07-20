import asyncio
import websockets
import base64
import time


def image_to_base64(path):
    '''
    :param path:
    :return:
    '''
    with open(path, 'rb') as f:
        image = f.read()
        image_base64 = str(base64.b64encode(image), encoding='utf-8')
    return image_base64


async def send_msg(websocket):
    '''
    :param websocket:
    :return:
    '''
    while True:
        t = input("please enter your context: ")
        # _text = image_to_base64(str(t)+".jpg")
        await websocket.send(t)


async def main_logic(hello):
    '''
    :return:
    '''
    url = "ws://221.226.81.54:30009"
    while True:
        print(hello)
        try:
            async with websockets.connect(url) as websocket:
                while True:
                    t = input("please enter your context: ")
                    await websocket.send(t)
                    print(f'client send message to server {url} successfully')
                    # time.sleep(10)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    hello = "123"
    # asyncio.new_event_loop()
    asyncio.new_event_loop().run_until_complete(main_logic(hello))
    print("---------------------")
