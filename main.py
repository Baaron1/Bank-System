import discord
from discord.ext import commands
from discord import DMChannel
import random
import time
import os
import asyncio
import datetime

from discord.ext.commands.bot import Bot
from apikeys import *


#This is a discord bot used for money and gambling stuff


client = commands.Bot(command_prefix= "~")


@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am the bank manager")


@client.event
async def on_member_join(member):
    channel = client.get_channel(920843623967383613)
    await channel.send(f"{member} Has been welcomed to the government")


@client.command()
async def roll_dice(ctx):
    dice1 = random.randint(1, 6)
    await ctx.send(dice1)


@client.command()
async def usage(ctx):
    await ctx.send("Hello, I am the bank manager. Some of the things you can tell me to do are, ~open_account [Credit Value], ~view_account, ~deposit [Amount], ~transfer [The person you are transfering to] [The amount you are transfering]")
    await ctx.send("The ~reset_file command will DM a Administrator asking them to reset the contents of your credit file. The Administrator will reach out to you soon. When your file is reset you will keep your current credits this just makes your channel more clean.")
    await ctx.send("You are also able to gamble by using ~gamble [Amount] [Your number guess] The number you are guessing is always between 1 and 10. If you win the money you won will be doubled, however if you lose you will lose the money you gambled")
    await ctx.send("Please remember that my mind is still being molded, and if you need any help contact Baaron1")


@client.command()
async def bank_deposit(ctx, user_go_to, amount):
    username = str(ctx.author).split('#')[0]
    try:
        with open(f"{user_go_to}.txt", 'r+') as f:
            for line in f.readlines():
                data = line.rstrip()
                user, amnt = data.split("|")
                newamount = int(amount) + int(amnt)
                newamount = int(newamount)
                f.write(user_go_to + "|" + newamount + "\n")
                await ctx.send("Process complete")
    except FileNotFoundError:
        await ctx.send("Selected user does not have an account")



@client.command()
async def open_account(ctx, currentamount):
    username = str(ctx.author).split('#')[0]
    with open(f"{username}.txt", 'a') as f:
        f.write(username + "|" + currentamount + "\n")
    with open(f"logs.txt", 'a') as f:
        f.write(username + " Has opened an account starting at " + currentamount + " credits\n")
    await ctx.send(f"Successfully created an account containing {currentamount} credits")


@client.command()
async def view_account(ctx):
    username = str(ctx.author).split('#')[0]
    try:
        with open(f"{username}.txt", 'r') as f:
            for line in f.readlines():
                data = line.rstrip()
                user, amnt = data.split("|")
                await ctx.send(line.rstrip())
        with open(f"logs.txt", 'a') as f:
            f.write(username + " Has viewed their account\n")
    except FileNotFoundError:
        await ctx.send("You do not have an account yet, please use ~open_account to create one")


@client.command()
async def deposit(ctx, amount):
    username = str(ctx.author).split('#')[0]
    now = datetime.datetime.now()
    try:
        with open(f"{username}.txt", 'r+') as f:
            for line in f.readlines():
                data = line.rstrip()
                user, amnt = data.split("|")
                newamount = int(amnt) + int(amount)
                newamount = str(newamount)
                print(f"Adding {amount} to {username} new total is {newamount}")
                f.write(username + "|" + newamount + "\n")
        await ctx.send(f"Added {amount} to your account. You are able to view your account with ~view_account")
        with open(f"logs.txt", 'a') as f:
            f.write(username + " Has deposited " + amount + " credits\n")
    except FileNotFoundError:
        await ctx.send("Sorry, you do not have an account. Please use ~open_account to create one")


@client.command()
async def withdrawal(ctx, amount):
    username = str(ctx.author).split('#')[0]
    try:
        with open(f"{username}.txt", 'r+') as f:
            for line in f.readlines():
                data = line.rstrip()
                user, amnt = data.split("|")
                newamount = int(amnt) - int(amount)
                newamount = str(newamount)
                print(f"Subtracting {amount} credits from {username} new total is {newamount}")
                f.write(username + "|" + newamount + "\n")
        await ctx.send(f"Subtracted {amount} credits from your account. If this was a mistake please contact an Administrator")
        with open(f"logs.txt", 'a') as f:
            f.write(username + " Has subtracted " + amount + " credits from their account\n")
    except FileNotFoundError:
        await ctx.send("Sorry, it looks like you do not have an account use ~open_account to create one")


@client.command(name='reset_file', pass_context=True)
async def reset_file(ctx):
    username = str(ctx.author).split('#')[0]
    user = await client.fetch_user("407036243138838529")
    await DMChannel.send(user, f"{username} Would like to request a File Reset")
    await ctx.send("Successfully requested a File Reset please be patient until an Administrator can contact you")


@client.command()
async def transfer(ctx, receiver, amount:int):
    username = str(ctx.author).split('#')[0]
    try:
        with open(f"{username}.txt", 'r+') as f:
            for line in f.readlines():
                data = line.rstrip()
                user, amnt = data.split("|")
                newamount = int(amnt) - int(amount)
                newamount = str(newamount)
                print(f"Transfering {amount} credits from {username} to" + receiver)
                f.write(username + "|" + newamount + "\n")
        with open(f"{receiver}.txt", "r+") as f:
            for line in f.readlines():
                data = line.rstrip()
                user2, amnt2 = data.split("|")
                newamount2 = int(amnt2) + int(amount)
                newamount2 = str(newamount2)
                f.write(user2 + "|" + newamount2 + "\n")
        await ctx.send(f"Successfully transfered {amount} to {receiver}")
        with open(f"logs.txt", 'a') as f:
            f.write(username + " Has transfered " + str(amount) + " credits to " + str(receiver) + "\n")
    except FileNotFoundError:
        await ctx.send("You or the selected user does not have an account. Please try again")


@client.command(name='jm', pass_context=True)
async def jm(ctx):
    username = str(ctx.author).split('#')[0]
    user = await client.fetch_user("407036243138838529")
    await DMChannel.send(user, f"{username} Requests to join the mafia")
    await ctx.send("Your request is being processed please be patient and wait for further notice")
    


@client.command()
async def gamble(ctx, amount, guess):
    username = str(ctx.author).split('#')[0]
    with open(f"logs.txt", 'a') as f:
        f.write(username + " Has gambled " + amount + " credits" + "\n")
    answ = random.randint(1, 10)
    if int(guess) == int(answ):
        amount = int(amount) * 2
        amount = int(amount)
        with open(f"{username}.txt", 'r+') as f:
            for line in f.readlines():
                data = line.rstrip()
                user, theirtotal = data.split("|")
                newamnt = int(amount) + int(theirtotal)
                newamnt = str(newamnt)
                f.write(username + "|" + newamnt + "\n")
        print(f"{username} won {amount} their new total is {newamnt}")
        await ctx.send(f"{username} won {amount} credits!")
    elif int(guess) != int(answ):
        await ctx.send(f"Wrong! The correct answer was {answ} but you guessed {guess}")
        with open(f"{username}.txt", 'r+') as f:
            for line in f.readlines():
                data = line.rstrip()
                user, theirtotal = data.split("|")
                newamnt = int(theirtotal) - int(amount)
                newamnt = str(newamnt)
                f.write(username + "|" + newamnt + "\n")
        ouramnt = int(amount) / 2
        with open(f"Baaron1.txt", 'r+') as f:
            for line in f.readlines():
                data = line.rstrip()
                user, theirtotal = data.split("|")
                newamnt = int(ouramnt) + int(theirtotal)
                newamnt = str(newamnt)
                f.write("Baaron1" + "|" + newamnt + "\n")
        with open(f"hi213213EVOLVED.txt", 'r+') as f:
            for line in f.readlines():
                data = line.rstrip()
                user, theirtotal = data.split("|")
                newamnt = int(ouramnt) + int(theirtotal)
                newamnt = str(newamnt)
                f.write("hi213213EVOLVED" + "|" + newamnt + "\n")


client.run(token) 