import matplotlib.pyplot as plt
import base64
from io import BytesIO
import psycopg2
import os
from matplotlib import dates
import datetime

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
    plt.switch_backend('AGG')

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111, alpha=0.9)
    hfmt = dates.DateFormatter('%H:%M:%S')
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(hfmt)

    conn = psycopg2.connect(host=os.environ.get('DB_HOST'), dbname=os.environ.get('DB_NAME'), user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASS'))
    cur = conn.cursor()
    query = 'SELECT device,datetime + \'3 hour\'::INTERVAL,value ' \
            'FROM ' \
            'public.graps_iotdata ' \
            'WHERE ' \
            'datetime >= (Select MAX(datetime) - \'1 day\'::INTERVAL FROM public.graps_iotdata)' \
            'ORDER BY ' \
            'datetime desc'
    cur.execute(query)

    values = {}
    for r in cur:
        series = values.get(r[0])
        if series == None:
            series = {'timeseries': [], 'values':[]}
        series.get('timeseries').append(r[1])
        series.get('values').append(r[2])
        values[r[0]]=series

    for v in values:
        ax.plot(values.get(v).get('timeseries'), values.get(v).get('values'), label=v)

    ax.set_title('Devices', fontsize=16)
    ax.set_ylabel('Percent')
    ax.grid(True)
    ax.legend(loc='upper right')
    fig.autofmt_xdate()
    plt.tight_layout()

    graph = get_graph()

    conn.close()

    return graph


def get_devices():

    conn = psycopg2.connect(host=os.environ.get('DB_HOST'), dbname=os.environ.get('DB_NAME'), user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASS'))
    cur = conn.cursor()
    query = 'SELECT DISTINCT SUBSTRING(device, 1, strpos(device,%s) - 1) FROM public.graps_iotdata'
    cur.execute(query,'/')

    result = []
    for r in cur:
        result.append(r[0].replace('/', '_'))
    conn.close()

    return result


def set_current_state(device, state):

    conn = psycopg2.connect(host=os.environ.get('DB_HOST'), dbname=os.environ.get('DB_NAME'), user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASS'))
    cur = conn.cursor()
    query = 'INSERT INTO public.graps_tasks (datetime, device, task) VALUES (%s, %s, %s)'
    if state == 'on':
        state_req = 1
    else:
        state_req = 0
    cur.execute(query,(datetime.datetime.now(),device, state_req))
    conn.commit()
    conn.close()
    print(device, state)