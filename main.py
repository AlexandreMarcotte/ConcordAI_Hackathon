import pandas as pd
import psycopg2
import numpy as np
import matplotlib.pyplot as plt
# import pyqtgraph as pg

def plot_data(data, title):
    plt.plot(list(range(len(data))), data)
    plt.title(title)
    plt.show()


def create_X(cur):
    X = []
    for trip_id in range(100):
        cur.execute(f'SELECT speed from points WHERE id_trip={trip_id};')
        speeds = []
        for speed in cur:
            speeds.append(*speed)
        if speeds != []:
            print('-------------------')
            print('speeds', speeds)
            print('TRIP ID', trip_id)
            y = create_y(cur, id_trip=trip_id)
            print(y)
            X.append(speeds)
            plot_data(speeds, y[1])
    return X


def create_y(cur, id_trip):
    cur.execute(f'SELECT id_trip, mode from trips WHERE id_trip={id_trip};')
    for id_trip, mode in cur:
        return [id_trip, mode]


def main():
    conn = psycopg2.connect(
            "dbname='mtltrajet' user='kyle' host='localhost' password='123'")
    cur = conn.cursor()
    X = create_X(cur)
    # y = create_y(cur)
    # print(X)





if __name__ == '__main__':
    main()




