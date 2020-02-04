import networkx as nx
import subprocess as sp
import matplotlib.pyplot as plt

from collections import deque
from queue import heappop, heappush
from math import inf
from sys import exit

class Grafik:

    def __init__(self, directed = True):
        self.edges = {}
        self.directed = directed

    def tambah_rute(self, kota1, kota2, cost = 1, __reversed = False):

        self.tambah_rute2(kota2, kota1, cost)

        cost = int(cost)
        gambar(kota1, kota2, cost)

        try:
            neighbors = self.edges[kota1]
        except KeyError:
            neighbors = {}

        neighbors[kota2] = cost
        self.edges[kota1] = neighbors

        if not self.directed and not __reversed:
            self.tambah_rute(kota2, kota1, cost, True)

    def tambah_rute2(self, kota1, kota2, cost = 1, __reversed = False):

        cost = int(cost)
        gambar(kota1, kota2, cost)

        try:
            neighbors = self.edges[kota1]
        except KeyError:
            neighbors = {}

        neighbors[kota2] = cost
        self.edges[kota1] = neighbors

        if not self.directed and not __reversed:
            self.tambah_rute(kota2, kota1, cost, True)

    def neighbors(self, kota):
        try:
            return self.edges[kota]
        except KeyError:
            return []

    def cost(self, kota1, kota2):
        try:
            return self.edges[kota1][kota2]
        except:
            return inf

    def breadth_first_search(self, asal, tujuan):
        found, fringe, visited, sumber = False, deque([asal]), set([asal]), {asal: None}

        while not found and len(fringe):
            kota_sekarang = fringe.pop()

            if kota_sekarang == tujuan:
                found = True
                break

            for kota in self.neighbors(kota_sekarang):
                if kota not in visited:
                    visited.add(kota)
                    fringe.appendleft(kota)
                    sumber[kota] = kota_sekarang

        print("\nBreadth First Search", end = '')

        if found:
            print()
            return sumber
        else:
            print('\nTidak Ada Rute dari {} ke {}'.format(asal, tujuan))

    def depth_first_search(self, asal, tujuan):
        found, fringe, visited, sumber = False, deque([asal]), set([asal]), {asal: None}

        while not found and len(fringe):
            kota_sekarang = fringe.pop()

            if kota_sekarang == tujuan:
                found = True
                break

            for kota in self.neighbors(kota_sekarang):
                if kota not in visited:
                    visited.add(kota)
                    fringe.append(kota)
                    sumber[kota] = kota_sekarang

        print("\nDepth First Search", end = '')

        if found:
            print()
            return sumber
        else:
            print('\nTidak Ada Rute dari {} ke {}'.format(asal, tujuan))

    def uniform_cost_search(self, asal, tujuan):
        found, fringe, visited, sumber, cost_so_far = False, [(0, asal)], set([asal]), {asal: None}, {asal: 0}

        while not found and len(fringe):
            _, kota_sekarang = heappop(fringe)

            if kota_sekarang == tujuan:
                found = True;
                break

            for kota in self.neighbors(kota_sekarang):
                new_cost = cost_so_far[kota_sekarang] + self.cost(kota_sekarang, kota)

                if kota not in visited or new_cost < cost_so_far[kota] :
                    visited.add(kota)
                    sumber[kota] = kota_sekarang
                    cost_so_far[kota] = new_cost
                    heappush(fringe, (new_cost, kota))

        print("\nUniform Cost Search", end = '')

        if found:
            print()
            return sumber, cost_so_far[tujuan]
        else:
            print('\nTidak Ada Rute dari {} ke {}'.format(asal, tujuan))
            return None, 0

    @staticmethod
    def cetak_rute(sumber, tujuan):
        parent = sumber[tujuan]

        if parent:
            Grafik.cetak_rute(sumber, parent)
        else:
            print(tujuan, end='')
            return

        print(' =>', tujuan, end='')

    def __str__(self):
        return str(self.edges)

    def cetak(self, metode, asal, tujuan):
        if metode == "B":
            sumber = self.breadth_first_search(asal, tujuan)

        elif metode == "U":
            sumber, cost = self.uniform_cost_search(asal, tujuan)

        elif metode == "D":
            sumber = self.depth_first_search(asal, tujuan)

        if (sumber):
            print('Arah  : ', end = '')
            Grafik.cetak_rute(sumber, tujuan)
            print('')

            if metode == "U":
                print("Biaya :", cost)

    @staticmethod
    def reset():
        Gambar.clear()
        Grafik.edges.clear()

Gambar = nx.Graph()

def gambar(kota1, kota2, cost):
	Gambar.add_edge(kota1, kota2, cost = cost)

Grafik = Grafik(directed = True)

def data_romania():

    Grafik.tambah_rute('A', 'S', 140)
    Grafik.tambah_rute('A', 'T', 118)
    Grafik.tambah_rute('A', 'Z', 75)
    Grafik.tambah_rute('Z', 'O', 71)
    Grafik.tambah_rute('O', 'S', 151)
    Grafik.tambah_rute('S', 'R', 80)
    Grafik.tambah_rute('S', 'F', 99)
    Grafik.tambah_rute('F', 'B', 211)
    Grafik.tambah_rute('T', 'L', 111)
    Grafik.tambah_rute('L', 'M', 70)
    Grafik.tambah_rute('R', 'C', 146)
    Grafik.tambah_rute('R', 'P', 97)
    Grafik.tambah_rute('M', 'D', 75)
    Grafik.tambah_rute('C', 'P', 138)
    Grafik.tambah_rute('P', 'B', 101)
    Grafik.tambah_rute('D', 'R', 120)

print("\n(>_<) Program Searching Sederhana\n")

fitur = 0
while fitur != "X":
    print('===============')
    print('Daftar Fitur')
    print('(D) Data Romania')
    print('(T) Tambah')
    print('(C) Cari')
    print('(G) Gambar')
    print('(R) Reset')
    print('(X) Keluar')
    print('===============', end = '')
    fitur = input('\nPilih Fitur : ').upper()
    tmp = sp.call('cls', shell = True)

    if fitur == "D":
        data_romania()
        print('\n\(^^)/ Pakai Data Romania\n')

    elif fitur == "T":
        print('\n(+) Tambah Kota\n')

        a, b, cost = "", "", ""
        while a == "" or a.isalpha() == False:
            a = input('Kota Pertama : ')
            if a != "" and a.isalpha():

                while b == "" or b.isalpha() == False:
                    b = input('Kota Kedua   : ')
                    if b != "" and b.isalpha():

                        while cost == "" or cost.isdigit() == False:
                            cost = input('Biaya        : ')
                            if cost != "" and cost.isdigit():

                                Grafik.tambah_rute(a, b, cost)
                                tmp = sp.call('cls', shell = True)

                            else:
                                tmp = sp.call('cls', shell = True)
                                print('\n(!) Mohon Isi cost dengan Angka\n')

                    else:
                        tmp = sp.call('cls', shell = True)
                        print('\n(!) Mohon Isi Kota Kedua dengan Karakter Huruf\n')

            else:
                tmp = sp.call('cls', shell = True)
                print('\n(!) Mohon Isi Kota Pertama dengan Karakter Huruf\n')

        print('\n\(^^)/ Berhasil\n')

    elif fitur == "C":
        print('\n(?) Cari Rute\n')

        sumber, tujuan, metode = "", "", ""
        while sumber == "":
            sumber = input('Kota Pertama : ')
            if sumber != "":
                while tujuan == "":
                    tujuan = input('Kota Kedua   : ')
                    if tujuan != "":

                        while metode != "B" and metode != "D" and metode != "U":

                            print('\n(B) Breadth First Search')
                            print('(D) Depth First Search')
                            print('(U) Uniform Cost Search')
                            metode = input('\nMetode Pencarian : ').upper()

                            if metode == "B" or metode == "D" or metode == "U":
                                Grafik.cetak(metode, sumber, tujuan)
                            else:
                                tmp = sp.call('cls', shell = True)
                                print('\n(!) Pilih Metode Pencarian B, D, atau U dengan Benar')

                    else:
                        tmp = sp.call('cls', shell = True)
                        print('\n(!) Mohon Isi Kota Kedua\n')

            else:
                tmp = sp.call('cls', shell = True)
                print('\n(!) Mohon Isi Kota Pertama\n')

        input("\nLanjut? Tekan Enter")
        tmp = sp.call('cls', shell = True)

    elif fitur == "G":
        pos = nx.spring_layout(Gambar, seed = 11)
        nx.draw(Gambar, pos, node_size=700)
        nx.draw_networkx_labels(Gambar, pos)

        labels = nx.get_edge_attributes(Gambar, 'cost')
        nx.draw_networkx_edge_labels(Gambar, pos, edge_labels=labels)

        plt.show(Gambar)

        tmp = sp.call('cls', shell = True)
        print('\n(G) Silakan Cek di Plot\n')

    elif fitur == "R":
        Grafik.reset()
        print('\n\(^^)/ Data Disetel Ulang\n')

    elif fitur == "X":
        exit

    else:
        print('\n(!) Pilih Fitur D, T, C, G, R, X dengan Benar\n')

print('\n(~^.^)~ Terima kasih telah berkunjung')

input("\n(->) Tekan Enter Untuk Menutup Konsol")
tmp = sp.call('cls', shell = True)