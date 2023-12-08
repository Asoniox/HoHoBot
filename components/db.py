"""
components.db
~~~~~~~~~~~~~~~~~~~~~

Extension for asynchronous MongoDB connection.
"""

import os
from motor.motor_asyncio import AsyncIOMotorClient
from colorama import init as colorama_init
from colorama import Fore, Style

DB_USERNAME = os.environ['DB_USERNAME']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_CLUSTER = os.environ['DB_CLUSTER']

uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_CLUSTER}.mongodb.net/?retryWrites=true&w=majority"
client = AsyncIOMotorClient(uri)

colorama_init(autoreset=True)

c = (
    Style.RESET_ALL,
    Fore.LIGHTBLACK_EX,
    Fore.LIGHTGREEN_EX
    )

try:
    client.admin.command('ping') #type: ignore
    print(f"{c[1]}----------------------\n{c[2]}Pinged deployment{c[0]} - Successfully connected to MongoDB!")
except Exception as e:
    print(e)