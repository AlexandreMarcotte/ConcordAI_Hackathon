import psycopg2
import numpy as np
import matplotlib.pyplot as plt
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import sys


def plot_data(data, title):
    plt.plot(list(range(len(data))), data)
    plt.title(title)
    plt.show()


def create_X(cur):
    X = []
    speeds = []
    Y = create_y(cur)
    cur.execute(f'SELECT id_trip, speed from points ORDER BY id_trip limit 1000000;')
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
                    # print('x_id_trip', id_trip)
                    # print('y_val', Y[id_trip])
                    # print('------------------')
                    # print(speeds)
                    # plot_data(speeds, mode)
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
                Y[id_trip] = id_trip
    print(Y)
    return Y


class Visualizer:
    def __init__(self):
        self.traces = {}
        self.app = QtGui.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 40
        self.w.setGeometry(0, 110, 1920, 1080)
        self.w.show()

        self.phase = 0
        self.lines = 100
        self.points = 100
        self.y = np.linspace(-10, 10, self.lines)
        self.x = np.linspace(-10, 10, self.points)

        for i, line in enumerate(self.y):
            self.traces[i] = gl.GLLinePlotItem()
            self.w.addItem(self.traces[i])

    def set_plotdata(self, name, points, color, width):
        self.traces[name].setData(pos=points, color=color, width=width)

    def update(self):
        for i, line in enumerate(self.y):
            y = np.array([line] * self.points)

            amp = 10 / (i + 1)
            phase = self.phase * (i + 1) - 10
            freq = self.x * (i + 1) / 10

            sine = amp * np.sin(freq - phase)
            pts = np.vstack([self.x, y, sine]).transpose()

            print('i', i, 'self.lines', self.lines)
            print(pg.glColor((i, self.lines*4)))
            self.set_plotdata(
                name=i, points=pts,
                color=pg.glColor((i, self.lines * 4)),
                width=1)
            self.phase -= .0002

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(10)
        QtGui.QApplication.instance().exec_()






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
