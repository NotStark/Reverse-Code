from pyrogram import Client,idle
from pyrogram import filters
import asyncio
import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

bot_token = "6141435415:AAE4HkjvE-BzwrfNMsNqYX-9mH87ca87qHg"

app = Client(
    "reverse_bot",
    api_id = 11674810,
    api_hash="9a64eb6bf7a4e8ba17dfa06efe6f2c6c",
    bot_token="6141435415:AAE4HkjvE-BzwrfNMsNqYX-9mH87ca87qHg"
)


@app.on_message(filters.command("start"))
async def _start(_,msg):
    await msg.reply("hey there")

@app.on_message(filters.command("pp"))
async def _pp(_,msg):
    replied = msg.reply_to_message
    if not replied:
        return await msg.reply("reply to a message")
    if not replied.photo:
        return await msg.reply("reply to a photo pls")
    file_id = replied.photo.file_id
    r = requests.post(f'https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}').json()
    file_path = r['result']['file_path']
    headers = {'User-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'}
    to_parse = f"https://images.google.com/searchbyimage??safe=off&sbisrc=tg&image_url=https://api.telegram.org/file/bot{bot_token}/{file_path}"
    r = requests.get(to_parse,headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    result = {                            
             "similar": '',
             'output': ''
         }
    for similar_image in soup.find_all('input', {'class': 'gLFyf'}):
         url = f"https://www.google.com/search?tbm=isch&q={quote_plus(similar_image.get('value'))}"
         result['similar'] = url
    for best in soup.find_all('div', {'class': 'r5a77d'}):
        output = best.get_text(strip=True)
        decoded_text = text.encode('utf-8').decode('unicode_escape')
        result["output"] = decoded_text.replace("Results for",'')       
    await msg.reply(result)

 
                      
    
async def main():
    await app.start()
    print("bot started")
    await idle()
    print("bot stopped")
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
