import discord

class NewMember(discord.Client):
    async def on_member_join(self, member):
        guild = member.guild
        if guil