token = 'your bot token here'

# ------
from discord import Client, Embed
from collections import defaultdict
import asyncio

client = Client()

servers = defaultdict(dict)
webhooks = {}

emoji = u'▶';


def getInProgressQuotes(guild):
    if guild not in servers:
        servers[guild] = {}
    return servers[guild]


@client.event
async def on_ready():
    print('The bot is ready!');

@client.event
async def on_message(message):
    user = message.author
    guild = message.guild

    if user in servers[guild]:
        # need to hijack this message

        webhook = webhooks[guild]

        # delete stored thing
        quote = servers[guild][user]
        del servers[guild][user];


        # create the embed
        jump_url = quote.jump_url

        embed = Embed(description=quote.content, timestamp=quote.created_at, color=0xffaa00)
        embed.set_author(name=quote.author.name, icon_url=quote.author.avatar_url)
        # embed.add_field(name="From", value=quote.author.mention)
        embed.add_field(name="Context", value="[Jump!](%s)"%jump_url)

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

    guild_webhooks = await message.channel.webhooks()
    if len(guild_webhooks) == 0:
        # could not find a webhook, can't do anything
        return await asyncio.wait([
            message.remove_reaction(emoji, user),
            message.channel.send('No webhooks exist for this channel! Please create one, moderators.')
        ])

    # save the webhook
    if guild not in webhooks:
        webhooks[guild] = guild_webhooks[0]

    # remove the selection from a previously selected server
    old_message = None
    if user in servers[guild]:
        old_message = servers[guild][user]

    # store the current selection
    servers[guild][user] = message

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
    if user not in servers[guild]:
        return

    # different message (somehow)
    if servers[guild][user] != message:
        return

    # delete it
    del servers[guild][user]

client.run(token)