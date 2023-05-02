from pyrogram import Client,idle
from pyrogram import filters
import asyncio
import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from unidecode import unidecode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 

bot_token = "6141435415:AAE4HkjvE-BzwrfNMsNqYX-9mH87ca87qHg"

app = Client(
    "reverse_bot",
    api_id = 11674810,
    api_hash="9a64eb6bf7a4e8ba17dfa06efe6f2c6c",
    bot_token="6141435415:AAE4HkjvE-BzwrfNMsNqYX-9mH87ca87qHg"
)


async def Sauce(bot_token,file_id):
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
        output = best.get_text()
        decoded_text =  unidecode(output)
        result["output"] = decoded_text
        
    return result
    
@app.on_message(filters.command("start"))
async def _start(_,msg):
    await msg.reply("hey there")

@app.on_message(filters.command("pp"))
async def _pp(_,msg):
    text = await msg.reply("wait a sec...")
    replied = msg.reply_to_message
    if not replied:
        return await text.edit("reply to a message")
    if not replied.photo:
        return await text.edit("reply to a photo pls")
    await text.edit("Requesting to Google....")
    file_id = replied.photo.file_id
    result = await Sauce(bot_token,file_id)
    await text.edit(f'[{result["output"]}]({result["similar"]})',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open Link",url=result["similar"])]]))
   
 
                      
    
async def main():
    await app.start()
    print("bot started")
    await idle()
    print("bot stopped")
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
