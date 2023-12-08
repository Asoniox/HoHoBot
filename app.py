"""
app.py
---
Flask app file.
"""
import sys
import json
from quart import Quart, render_template, redirect
from api import eec

#DON'T GENERATE __PYCACHE__
sys.dont_write_bytecode = True

#FLASK APP
app = Quart(__name__)

@app.route("/")
async def pageHome():
    return await render_template('index.html')

@app.route("/invite")
async def redirectInvite():
    return redirect("https://discord.com/api/oauth2/authorize?client_id=1181439234553413632&permissions=0&scope=bot+applications.commands", code=301)
