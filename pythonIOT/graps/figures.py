import matplotlib.pyplot as plt
import base64
from io import BytesIO
import psycopg2
import os
from matplotlib import dates

def db_client(db_host, db_name, dn_user, db_pass):
    conn = psycopg2.connect(dbname=db_name, user=dn_user, password=db_pass, host=db_host)
    db_client = conn.cursor()
    return db_client

def my_figure():

    plt.switch_backend('AGG')
    fig, ax = plt.subplots()
    ax.plot([1, 3, 4], [3, 2, 5])
    #   return fig
    graph = get_graph()
    return graph


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_plot():
    cur = db_client(os.environ.get('DB_HOST'), os.environ.get('DB_NAME'), os.environ.get('DB_USER'), os.environ.get('DB_PASS'))
    cur.execute('SELECT datetime,value FROM public.graps_iotdata WHERE device=%s ORDER BY datetime desc LIMIT 1000', ['home/temperature'])

    plt.switch_backend('AGG')

    timeseries = []
    avg_io_wait = []
    for r in cur:
        timeseries.append(r[0])
        avg_io_wait.append(r[1])

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111, alpha=0.9)
    hfmt = dates.DateFormatter('%H:%M:%S')
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(hfmt)
    ax.plot(timeseries, avg_io_wait, color='blue', label='Temperature')
    ax.set_title('Temperature', fontsize=16)
    ax.set_ylabel('Percent')
    ax.grid(True)
    ax.legend(loc='upper right')
    fig.autofmt_xdate()
    plt.tight_layout()

    graph = get_graph()

    return graph
