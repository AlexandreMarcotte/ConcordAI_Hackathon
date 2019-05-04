import pandas as pd
import psycopg2
import numpy as np
import matplotlib.pyplot as plt
# import pyqtgraph as pg


def main():
    conn = psycopg2.connect(
            "dbname='mtltrajet' user='kyle' host='localhost' password='123'")
    cur = conn.cursor()
    for trip_id in range(100):
        lats = []
        lons = []
        speeds = []
        cur.execute(f'SELECT latitude, longitude, speed from points WHERE id_trip={trip_id};')
        for lat, lon, speed in cur:
            lats.append(lat)
            lons.append(lon)
            speeds.append(speed)

        if lats != []:
            plt.plot(lats, lons)
            plt.show()

            plt.plot(list(range(len(speeds))), speeds)


    # DATABASE_URI = 'postgres://kyle:123@localhost/mtltrajet'
    # eng = create_engine(DATABASE_URI)
    #
    # with eng.connect() as con:
    #     rs = con.execute('SELECT 5')
    #     data = rs.fetchone()[0]
    #     print(f'Data: {data}', data)
    # df = pd.read_sql(engine.)

if __name__ == '__main__':
    main()