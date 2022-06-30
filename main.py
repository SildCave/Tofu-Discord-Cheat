import discum
from tinydb import TinyDB
import time
import random
import threading
from multiprocessing import Manager
from humanfriendly import format_timespan
import discord
from discord.ui import Select, View
from discord.ext import commands
from config import *

if __name__ == '__main__':

    db = TinyDB('workers.json')
    db_workers = db.table('workers')

    class worker_unit:
        def __init__(self, bot, name, id):
            self.name = name
            self.bot = bot
            self.drop_cooldown = time.time() - drop_cd + random.randint(1, 50)
            self.tmg_cooldown = time.time() - tmg_cd + random.randint(1, 50)
            self.daily_cooldown = time.time() - daily_cd + random.randint(1, 50)
            self.id = id

    drop_cd = (20 * 60) + 2
    tmg_cd = (3 * 60) + 2
    daily_cd = ((60 * 60) * 24) + 2

    cooldowns_shared_list = Manager().list()
    workers = []

    select_menu_options = []

    for worker in db_workers:
        bot = discum.Client(token = worker['worker_personal_token'], log=False)
        name = worker['worker_friendly_name']
        id = worker['worker_id']

        worker = worker_unit(bot = bot, name = name, id = id)
        workers.append(worker)

        shared_worker_info = {
            'name': worker.name,
            'daily_cooldown': worker.daily_cooldown,
            'drop_cooldown': worker.drop_cooldown,
            'tmg_cooldown': worker.tmg_cooldown
        }

        cooldowns_shared_list.append(shared_worker_info)

        select_opt = discord.SelectOption(
                        label = worker.name,  
                        description='worker unit'
                        )

        select_menu_options.append(select_opt)

    def working_cycle(worker, cooldowns_shared_list):

        for index, shared_worker_info in enumerate(cooldowns_shared_list):
            if shared_worker_info['name'] == worker.name:
                shared_worker_info_index =  index
                break


        if time.time() - worker.drop_cooldown >= drop_cd:
            worker.bot.sendMessage(tofu_channel_id, f'{prefix}s')
            worker.drop_cooldown = time.time()
        else:
            #print(f"DROP | {worker.name} | {int(time.time() - worker.drop_cooldown)} out of {drop_cd} seconds")
            cooldowns_shared_list_cache = cooldowns_shared_list[shared_worker_info_index]
            cooldowns_shared_list_cache['drop_cooldown'] = drop_cd - (int(time.time() - worker.drop_cooldown))

            cooldowns_shared_list[shared_worker_info_index] = cooldowns_shared_list_cache

        if time.time() - worker.tmg_cooldown >= tmg_cd:
            worker.bot.sendMessage(tofu_channel_id, f'{prefix}mg 4')
            worker.tmg_cooldown = time.time()
        else:
            #print(f"TMG | {worker.name} | {int(time.time() - worker.tmg_cooldown)} out of {tmg_cd} seconds")
            cooldowns_shared_list_cache = cooldowns_shared_list[shared_worker_info_index]
            cooldowns_shared_list_cache['tmg_cooldown'] = tmg_cd - (int(time.time() - worker.tmg_cooldown))

            cooldowns_shared_list[shared_worker_info_index] = cooldowns_shared_list_cache

        if time.time() - worker.daily_cooldown >= daily_cd:
            worker.bot.sendMessage(tofu_channel_id, f'{prefix}daily')
            worker.daily_cooldown = time.time()
        else:
            #print(f"DAILY | {worker.name} | {int(time.time() - worker.daily_cooldown)} out of {daily_cd} seconds")
            cooldowns_shared_list_cache = cooldowns_shared_list[shared_worker_info_index]
            cooldowns_shared_list_cache['daily_cooldown'] = daily_cd - (int(time.time() - worker.daily_cooldown))

            cooldowns_shared_list[shared_worker_info_index] = cooldowns_shared_list_cache


        #print('\n' * 2)


    def tofu_loop(cooldowns_shared_list):
        while True:

            for worker in workers:
                working_cycle_thread = threading.Thread(target = working_cycle, args = [worker, cooldowns_shared_list])
                working_cycle_thread.start()

            time.sleep((random.randint(10,30)) / 10)


    tofu_loop_process = threading.Thread(target = tofu_loop, args = [cooldowns_shared_list])
    tofu_loop_process.start()




    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix='!', intents = intents)


    @bot.command()
    async def cd(ctx):
        select = Select(
            min_values = 1,
            max_values = 1,
            placeholder ="select",
            options = select_menu_options,
            row=2
        )




        async def select_callback(interaction):
            
            for worker in workers:
                if worker.name == select.values[0]:
                    worker_id = int(worker.id)
                    break

            for index, shared_worker_info in enumerate(cooldowns_shared_list):
                if shared_worker_info['name'] == worker.name:
                    shared_worker_info_index =  index
                    break
                
            embed = discord.Embed(title = "Cooldowns", colour = discord.Colour(0x1493ef), description = f"Cooldowns for {worker.name}")
            embed.set_footer(text="https://github.com/SildCave/Tofu-Discord-Cheat", icon_url="https://findicons.com/files/icons/2808/jolly_icons_free/128/github.png")
            embed.set_thumbnail(url = ctx.guild.get_member(worker_id).avatar.url)


            summon_temp_cd = format_timespan(cooldowns_shared_list[shared_worker_info_index]['drop_cooldown'])
            tmg_temp_cd = format_timespan(cooldowns_shared_list[shared_worker_info_index]['tmg_cooldown'])
            daily_temp_cd = format_timespan(cooldowns_shared_list[shared_worker_info_index]['daily_cooldown'])

            embed.add_field(name=f":alarm_clock: · Summon · {summon_temp_cd}\n:alarm_clock: · Minigame · {tmg_temp_cd}\n:alarm_clock: · Daily · {daily_temp_cd}", value="\u200b", inline = False)


            await interaction.response.send_message(embed = embed)

        select.callback = select_callback

        view = View()
        view.add_item(select)


        await ctx.send('Select worker', view=view)


    @bot.listen('on_message')
    async def handle_drop(message):
        if ' is summoning 2 cards!' in message.content:

            for worker in workers:
                if int(worker.id) == int(message.content.replace(' is summoning 2 cards!', '').replace('>', '').replace('<@', '')):
                    worker = worker
                    break
                    
            worker.bot.addReaction(str(message.channel.id), str(message.id), '❓')

        if ' grabbed a **Fusion Token**!<a:token:973893149770522674>' in message.content:
            for worker in workers:
                if int(worker.id) == int(message.content.replace(' grabbed a **Fusion Token**!<a:token:973893149770522674>', '').replace('>', '').replace('<@', '')):
                    worker = worker
                    break

            worker.bot.sendMessage(str(message.channel.id), f'{prefix}open fusion token')

        if (message.author.id == 792827809797898240) and ('receive a random card from' in message.embeds[0].description):
            fusion_worker_id = int(message.embeds[0].author.icon_url.split('/')[4])

            for worker in workers:
                if int(worker.id) == fusion_worker_id:
                    worker = worker
                    time.sleep(1)
                    worker.bot.addReaction(str(message.channel.id), str(message.id), '✅')

                    break
        
    bot.run(bot_token)

