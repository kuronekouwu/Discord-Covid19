import discord
import aiohttp 
import json
from discord.ext import commands

TOKEN = '' #เอา Token Bot มาใช้งานได้เล๊ยย!!
PREFIX = '>>' #คำนำหน้า

bot = commands.Bot(command_prefix=PREFIX)

@bot.event 
async def on_ready() :
	print(f"Bot {bot.user.name} has started!")

@bot.event
async def on_message(message) :
	await bot.process_commands(message)

async def get_data_url(url) :
	async with aiohttp.ClientSession() as session :
		html = await fetch(session, url)

		return html

async def fetch(session, url) :
	async with session.get(url) as respones :
		return await respones.text()

@bot.command()
async def covid19(ctx) :
	thai = await get_data_url('https://covid19.th-stat.com/api/open/timeline')
	thai = json.loads(thai)

	e = discord.Embed(
		title="ข้อมูล COVID-19",
		description=f"อัพเดตล่าลุดเมื่อ {thai['UpdateDate']}",
		color=0xf2466c
	)

	e.add_field(name=':thermometer_face: ผู้ป่วยสะสม',value=f"{thai['Data'][-1]['Confirmed']} คน")
	e.add_field(name=':mask: ผู้ป่วยรายใหม่',value=f"{thai['Data'][-1]['NewConfirmed']} คน")
	e.add_field(name=':homes:  ผู้ป่วยรักษาหายแล้ว',value=f"{thai['Data'][-1]['Recovered']} คน")
	e.add_field(name=':skull_crossbones: ผู้ป่วยเสียชีวิต',value=f"{thai['Data'][-1]['Deaths']} คน")
	e.set_footer(text=f'''ข้อมูลจาก {thai["Source"]}''')

	await ctx.send(embed=e)

bot.run(TOKEN)
