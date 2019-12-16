import discord
import datetime
import asyncio

# id = 655760058390544384
token = "NjU1NzYwNTUxMzc2NDUzNjMz.XfZDUQ.TMU-q_l9HxQ7tJj5HLAv0KOH0bQ"
messages = joined = 0
message_count_dict = {}
client = discord.Client()


async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {datetime.datetime.utcnow()}, Messages: {messages}, Member Joined: {joined}\n")
            messages = 0
            joined = 0

            with open("userstats.txt", "a") as f:
                for message_author in message_count_dict.keys():
                    f.write(f"Update Time: {datetime.datetime.utcnow()}, User: {message_author}, # of Messages: {message_count_dict[message_author]}\n")

            await asyncio.sleep(60)
        except Exception as e:
            print(e)
            await asyncio.sleep(60)
@client.event
async def on_member_update(before, after):
    n = after.nick
    if n:
        if n.lower().count("teemo") > 0:
            last = before.nick
            if last:
                await after.edit(nick=last)
                channel = client.get_channel(655760058390544387)
                await channel.send(f"Remember, Teemo is Satan! {before.mention}")
            else:
                await after.edit(nick="NO STOP THAT")
                channel = client.get_channel(655760058390544387)
                await channel.send(f"Remember, Teemo is Satan! {before.mention}")

@client.event
async def on_member_join(member):
    global joined
    joined += 1
    for channel in member.guild.channels:
        if channel.name == "general":
            await channel.send(f"""Welcome to the server!!! {member.mention}""")

@client.event
async def on_message(message):
    global messages, message_count_dict
    messages += 1
    client_id = client.get_guild(655760058390544384)
    channels = ["commands"]
    valid_users = ["David#1720", "BOT#8464"]
    bad_words = ["bad", "stop"]

    # help instruction
    if message.content == "!help":
        embed = discord.Embed(title="Help on BOT", description="Some useful commands")
        embed.add_field(name="!hi", value="Greet back the user")
        embed.add_field(name="!users", value="Prints number of users")
        await message.channel.send(content=None, embed=embed)

    # user commands
    if message.content.startswith("!") and message.content != "!help":  # ! - command
        if message.channel.name in channels and str(message.author) in valid_users:
            if message.content.find("!hi") != -1:
                await message.channel.send("hi")
            elif message.content == "!users":
                await message.channel.send(f"""# of Members: {client_id.member_count}""")
        else:
            print(f"""Users: {message.author} tried to do command {message.content}, in channel {message.channel}""")
            await message.channel.send(f"""Hey {message.author}, cant do this here!""")

    # message count
    if not str(message.author) in message_count_dict.keys():
        message_count_dict[str(message.author)] = 1
    else:
        message_count_dict[str(message.author)] = message_count_dict[str(message.author)] + 1

    # swear word filter
    for word in bad_words:
        if message.content.count(word) > 0:
            print("A bad word was said")
            await message.channel.purge(limit=1)

client.loop.create_task(update_stats())
client.run(token)
