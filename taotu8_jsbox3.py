import asyncio
import os
import time
import webbrowser
import aiohttp
from progressbar import widgets, ProgressBar
import sys
import console

folder_name = sys.argv[1]
urls = sys.argv[2].split(',')
doc_path = os.path.join(os.path.expanduser('/private/var/mobile/Library/Mobile Documents/iCloud~com~omz-software~Pythonista3/Documents/Downloads'),'TaoTu8_Images')
folder_path = os.path.join(doc_path, folder_name)
if not os.path.isdir(folder_path):
  os.makedirs(folder_path)

loop = asyncio.get_event_loop()


class Progress:
    def __init__(self, sum_exp):
        new_widgets = [
            widgets.Percentage(),
            ' (', widgets.SimpleProgress(),
            ') ', widgets.Bar(),
            ' ', widgets.Timer(format='Elapsed Timer: %(seconds_elapsed).3fs'),
        ]
        self.bar = ProgressBar(max_value=sum_exp, widgets=new_widgets)
        self.finished = 0
        
    def update(self, job_size) -> None:
        self.finished += job_size
        self.bar.update(self.finished)
        
    def finish(self) -> None:
        self.bar.finish()
        
    def start(self) -> None:
        self.bar.start()


async def get_url(url, session, progress):
    file_name = url.split('/')[-1]
    while True:
        try:
            with open(f'{folder_path}/{file_name}', 'wb') as fd:
                async with session.get(url) as rsp:
                    async for i in rsp.content:
                        fd.write(i)
            break
        except Exception as e:
            pass
            # print(file_name, '网络异常', e.__class__.__name__)
    progress.update(1)
    # print(progress.finished, file_name)


async def main():
    console.clear()
    len_chunck = 100
    len_urls = len(urls)
    
    progress = Progress(len_urls)
    progress.start()
    
    timeout = aiohttp.ClientTimeout(total=2.5)
    async with aiohttp.ClientSession(timeout=timeout) as ss:
        for i in range(0, len_urls, len_chunck):
            tasks = [loop.create_task(
                get_url(url, ss, progress)) for url in urls[i: i+len_chunck]]
            await asyncio.wait(tasks)
    progress.finish()


start = time.time()
loop.run_until_complete(main())
