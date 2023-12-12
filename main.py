import discord
from discord.ext import commands, tasks
from bs4 import BeautifulSoup
import requests

# Khởi tạo bot Discord
bot = commands.Bot(command_prefix='!')

# Token bot Discord
TOKEN = 'MTE4Mzc3MDQxNTE3MzIxNDI0OQ.GbF5ZO.LtR0BBnN9XE11dWuPTVV9GZbAkAct3d9N1NOEc'

# Kênh Discord để gửi tin tức
NEWS_CHANNEL_ID = 1184021970317234226  # Thay ID bằng ID của kênh Discord bạn muốn sử dụng

# Từ khoá để tìm kiếm tin tức trên Naver
SEARCH_KEYWORDS = ['TEMPEST', 'TXT', 'KARD', 'ONEUS', 'AB6IX', 'DKZ', 'TOMORROW X TOGETHER']  # Thay đổi theo nhu cầu của bạn

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    news_update.start()

@tasks.loop(minutes=1)  # Cập nhật tin tức mỗi 1 phút
async def news_update():
    news_channel = bot.get_channel(NEWS_CHANNEL_ID)

    for keyword in SEARCH_KEYWORDS:
        news_url = f'https://search.naver.com/search.naver?query={keyword}&where=news&ie=utf8&sm=nws_hty'

        # Lấy dữ liệu từ trang web Naver
        response = requests.get(news_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Xử lý dữ liệu để lấy các tiêu đề tin tức
        news_titles = soup.select('.news_tit')

        # Gửi tiêu đề tin tức mới nhất vào kênh Discord
        if news_titles:
            latest_news_title = news_titles[0].text.strip()
            await news_channel.send(f'Latest news in {keyword}: {latest_news_title}')

# Khởi động bot
bot.run(TOKEN)