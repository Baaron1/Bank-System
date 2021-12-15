import discord
from discord.ext import commands
import random
import time
import os
import asyncio
import datetime

from discord.ext.commands.bot import Bot
from apikeys import *

client = commands.Bot(command_prefix= "~")


@client.event
async def on_ready():
    print("The bot is ready")
    print("################")


@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am the bank manager")


@client.command()
async def open_account(ctx, currentamount):
    username = str(ctx.author).split('#')[0]
    with open(f"{username}.txt", 'a') as f:
        f.write(username + "|" + currentamount + "\n")


@client.command()
async def view_account(ctx):
    username = str(ctx.author).split('#')[0]
    with open(f"{username}.txt", 'r') as f:
        for line in f.readlines():
            data = line.rstrip()
            user, amnt = data.split("|")
            await ctx.send(line.rstrip())


@client.command()
async def deposit(ctx, amount):
    username = str(ctx.author).split('#')[0]
    now = datetime.datetime.now()
    with open(f"{username}.txt", 'r+') as f:
        for line in f.readlines():
            data = line.rstrip()
            user, amnt = data.split("|")
            newamount = int(amnt) + int(amount)
            newamount = str(newamount)
            print(f"Adding {amount} to {username} new total is {newamount}")
            f.write(username + "|" + newamount + "\n")
    await ctx.send(f"Added {amount} to your account. You are able to view your account with ~view_account")


@client.command()
async def transfer(ctx, receiver, amount:int):
    username = str(ctx.author).split('#')[0]
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


@client.command()
async def gamble(ctx, amount, guess):
    username = str(ctx.author).split('#')[0]
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