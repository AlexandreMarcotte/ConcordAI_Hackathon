import psycopg2
import numpy as np
import matplotlib.pyplot as plt
from time import sleep


def plot_data(data, title):
    plt.plot(list(range(len(data))), data)
    plt.title(title)
    plt.show()


def create_X(cur):
    X = []
    speeds = []
    Y = create_y(cur)
    cur.execute(f'SELECT id_trip, speed from points ORDER BY id_trip limit 100000;')
    trip_no = 0
    for id_trip, speed in cur:
        speeds.append(speed)
        if id_trip != trip_no:
            # print(id_trip)
            try:
                mode = Y[id_trip]
                # print(mode)
                if len(speeds) > 10:
                    print('ID_X', id_trip, ' = ', 'ID_Y', mode)
                    print('x_id_trip', id_trip)
                    print('y_val', Y[id_trip])
                    print('------------------')
                    print(speeds)
                    if mode == 'À pied':
                        sleep(0.5)
                        plot_data(speeds, mode)
                    X.append(speeds)
            except:
                'no mode associated'
            # reset value for next trip
            speeds = []
            trip_no = id_trip

        # print(id_trip, speed)

def create_y(cur):
    Y = {}
    y_cur = cur
    y_cur.execute(f'SELECT id_trip, mode from trips ORDER BY id_trip;')
    for id_trip, mode in y_cur:
        if mode != None:
            if not ('/' in mode or ',' in mode):
                Y[id_trip] = mode
    print(Y)
    return Y










def main():
    conn = psycopg2.connect(
            "dbname='mtltrajet' user='kyle' host='localhost' password='123'")
    cur = conn.cursor()
    X = create_X(cur)
    # y = create_y(cur)
    # print(X)





if __name__ == '__main__':
    main()




"""
 speeds = []
 for speed in cur:
     speeds.append(*speed)
 if len(speeds) > 10:
     y = create_y(cur, id_trip=trip_id)
     print(y)
     if len(y) == 1:  # Only one golden truth
         print('-------------------')
         print('speeds', speeds)
         print('TRIP ID', trip_id)
         print(y)
         X.append(speeds)
         Y.append(y)
         plot_data(speeds, y)
 return X
"""
