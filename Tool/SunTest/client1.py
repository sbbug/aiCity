import asyncio
import websockets
import base64
import threading


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
        _text = image_to_base64("temp.jpg")
        await websocket.send(t)


async def main_logic(hello):
    '''
    :return:
    '''
    url = "ws://221.226.81.54:30009"
    print(threading.currentThread().name)
    print(threading.currentThread().ident)
    while True:
        print(hello)
        try:
            async with websockets.connect(url) as websocket:
                while True:
                    t = input("please enter your context: ")
                    _text = image_to_base64("./img/" + str(t) + ".jpg")
                    await websocket.send(_text)
                    print(f'client send message to server {url} successfully')
                    # time.sleep(10)
        except Exception as e:
            print(e)


def run():
    asyncio.run(main_logic("hello"))


if __name__ == "__main__":
    hello = "123"
    t1 = threading.Thread(target=run)
    t1.start()
    print("---------------------")
