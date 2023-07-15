import os

from aiohttp import web
from db_client import Db
from cutter import Cutter
from controller import Controller
from dotenv import load_dotenv

load_dotenv()

db = Db(os.getenv("DATABASE_URL"))
cutter = Cutter()
controller = Controller(db, cutter)


app = web.Application()
app.router.add_get('/save_image', controller.save_image, name='save_image')
app.router.add_get('/get_image', controller.get_image, name='get_image')
web.run_app(app, host="0.0.0.0", port=8080)
