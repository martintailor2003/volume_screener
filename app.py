from flask import Flask,render_template
#from algo import get_lists
import json
from algo import get_lists
from flask_apscheduler import APScheduler
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__,template_folder='templates')

@app.route("/")
def hello_world():
    bull_list, bear_list = get_lists()


    #bull_list = ['BTCUSDT','ETHUSDT','ADAUSDT','TRXUSDT']
    #bear_list = ['BTCUSDT ETHUSDT TRXUSDT']

    return render_template("index.html",bull_list=bull_list,bear_list=bear_list)


def my_job():
    bull_list, bear_list = get_lists()
    print(bull_list)


if __name__ == '__main__':   
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=my_job, trigger="interval", seconds=500)
    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    app.run(debug=True)