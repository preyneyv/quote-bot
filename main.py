from discord import Client, Embed
from collections import defaultdict
import asyncio
import os
import json

client = Client()

# set up variables
messages = defaultdict(dict)

# load the config
# config = json.load(open('config.json'))
emoji = u"▶"
token = os.environ['token']
# token = config['token']

def tag(user):
    return "%s#%s" % (user.name, user.discriminator)

@client.event
async def on_ready():
    print('Quote Bot is ready to rumble!');

async def make_webhook(channel):
    guild = channel.guild
    print('Creating a webhook for #%s in "%s" (%i)'% (channel.name, guild.name, guild.id))
    return await channel.create_webhook(name="Quote Bot #%s"%channel.name, reason="For Quote Bot to send messages in #%s"%channel.name)

@client.event
async def on_guild_join(guild):
    print('Joined "%s" (%i)' % (guild.name, guild.id))

@client.event
async def on_message(message):
    user = message.author
    guild = message.guild

    if user in messages[guild]:
        # need to hijack this message
        quote = messages[guild][user]
        print('Hijacking message from %s quoting %s' % (tag(user), tag(quote.author)))

        channel_webhooks = await message.channel.webhooks()
        if len(channel_webhooks) == 0:
            channel_webhooks = [await make_webhook(message.channel)]
        webhook = channel_webhooks[0]

        # delete stored thing
        del messages[guild][user];

        jump_url = quote.jump_url

        # create the embed
        embed = Embed(description=quote.content, timestamp=quote.created_at, color=0xffaa00)
        embed.set_author(name=quote.author.display_name, icon_url=quote.author.avatar_url)
        embed.add_field(name="Context", value="[Jump!](%s)"%jump_url)
        embed.set_footer(text="In #%s" % quote.channel.name)

        content = message.content
        await asyncio.wait([
            quote.remove_reaction(emoji, user), # remove the reaction
            webhook.send(
                content=content,
                embed=embed,
                username=user.display_name,
                avatar_url=user.avatar_url
            ), # send via webhook

            message.delete() # delete the original message
        ])        

@client.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    guild = message.guild

    # not the emoji we're looking for.
    if reaction.emoji != emoji:
        return

    print ('Listening for a message from %s to quote %s' % (tag(user), tag(message.author)))

    channel_webhooks = await message.channel.webhooks()
    if len(channel_webhooks) == 0:
        # no webhook exists, create one
        channel_webhooks = [await make_webhook(message.channel)]

    # remove the selection from a previously selected server
    old_message = None
    if user in messages[guild]:
        old_message = messages[guild][user]

    # store the current selection
    messages[guild][user] = message

    if old_message:
        # remove the existing reaction
        await old_message.remove_reaction(emoji, user)

@client.event
async def on_reaction_remove(reaction, user):
    message = reaction.message
    guild = message.guild

    # not the emoji we're looking for
    if reaction.emoji != emoji:
        return

    # untracked user
    if user not in messages[guild]:
        return

    # different message (somehow)
    if messages[guild][user] != message:
        return

    print ('No longer listening for a message from %s' % tag(user))

    # delete it
    del messages[guild][user]

client.run(token)