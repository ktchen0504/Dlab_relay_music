# -*- coding: utf-8 -*-
"""
Created on Mon May 27 15:47:52 2019

@author: KT Chen
"""

import socket
import sys
import re
import time
import os.path
import logging
import pygame
import tkinter as tk # tkinter 8.6

# Create the Interface
window = tk.Tk()
window.geometry("400x300")
window.title("Play Music")

# Initialize some variables
Ev_stat = 0
foo = 0
Ev_break = 1

# Initialize pygame mixer
pygame.mixer.init()

mus_num_d1 = {"con": "9901_SF_continuous_D1",
              "inter": "9905_SF_Intermittent_D1",
              "base": "SF_Normal_D1",
              "prac": "SF_con_prac"}
mus_num_d2 = {"con": "9903_SF_continuous_D2",
              "inter": "9906_SF_Intermittent_D2",
              "base": "SF_Normal_D1",
              "prac": "SF_inter_prac"}

# need change group for mus_num_d[x] and ["con, inter, base"]
py_path = os.path.dirname(__file__)
mus_path = 'Sound_file'  # os.path.join(py_path, 'Sound_file/' + mus_num_d2["inter"] + '.wav')

# Socket initialize
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.20.40', 9002)

def socketinitial():
	global server_address
	global sock
	sock.connect(server_address)
	sock.settimeout(10)	
	print("connecting to %s port: %s" % server_address, file=sys.stderr)


def receive():
    global Ev_stat
    global foo
    global sock

    socketinitial()
    try:
        message = "Event Status..."
        print('Checking %s' % message, file=sys.stderr)
        sock.sendall(str.encode(message))

        # while
        while True:
            time.sleep(1)
            data = sock.recv(1024)
            stringdata = data.decode('utf-8')
            strdata = re.split(r'[~\r\n\t+]', stringdata)
            # print(strdata)
            if int(strdata[foo]) == 1:
                Ev_stat += 1
                foo = 1
                print('Event Status is now: "%s"' % Ev_stat)
                break
            else:
                print('Received event status:"%s"' % Ev_stat, file=sys.stderr)
    except socket.timeout:
        Ev_stat = 2
        print("Time out 1, restart required...")
    finally:
        return Ev_stat


def play_music():
    global mus_path
    try:
        print(mus_path)
        pygame.mixer.music.load(mus_path)
        pygame.mixer.music.play()
    except Exception as e:
        # tkinter.messagebox.showerror('File not found')
        logging.exception(e)
        print("Error")


def stop_music():
    pygame.mixer.music.stop()


def after_mus_play():
    global Ev_stat
    global foo
    global sock

    try:
        message = "Event Status..."
        print('New %s' % message, file=sys.stderr)
        while True:
            time.sleep(1)
            data = sock.recv(1024)
            stringdata = data.decode('utf-8')
            strdata = re.split(r'[~\r\n\t+]', stringdata)
            # print(amount_received)
            print('Received new status:"%s"' % strdata[0], file=sys.stderr)
    except socket.timeout:
        Ev_stat = 2
        print("Time out 2, restart required...")
        stop_music()
    finally:
        sock.close()  # don't close too early
        print('Closing socket...')
        return Ev_stat


def path_change1():
    global mus_num_d1
    global py_path
    global mus_path
    mus_path = os.path.join(py_path, mus_path, mus_num_d1["con"] + '.wav')
    print(mus_num_d1["con"])
    print(mus_path)
    return mus_path
    

def path_change2():
    global mus_num_d1
    global py_path
    global mus_path
    mus_path = os.path.join(py_path, mus_path, mus_num_d1["inter"] + '.wav')
    print(mus_num_d1["inter"])
    return mus_path


def path_change3():
    global mus_num_d1
    global py_path
    global mus_path
    mus_path = os.path.join(py_path, mus_path, mus_num_d1["base"] + '.wav')
    print(mus_num_d1["base"])
    return mus_path


def path_change4():
    global mus_num_d2
    global py_path
    global mus_path
    mus_path = os.path.join(py_path, mus_path, mus_num_d2["con"] + '.wav')
    print(mus_num_d2["con"])
    return mus_path


def path_change5():
    global mus_num_d2
    global py_path
    global mus_path
    mus_path = os.path.join(py_path, mus_path, mus_num_d2["inter"] + '.wav')
    print(mus_num_d2["inter"])
    return mus_path


def path_change6():
    global mus_num_d1
    global py_path
    global mus_path
    mus_path = os.path.join(py_path, mus_path, mus_num_d1["prac"] + '.wav')
    print("Train: Continuous")
    return mus_path

def path_change7():
    global mus_num_d2
    global py_path
    global mus_path
    mus_path = os.path.join(py_path, mus_path, mus_num_d2["prac"] + '.wav')
    print("Train: Intermittent")
    return mus_path

# Ev_num = receive()

# if Ev_num == 1:
#     play_music()

# Ev_break = after_mus_play()

d1_con_btn = tk.Button(window, text = "D1 continuous", command = path_change1)
d1_con_btn.place(x=50, y = 40, width = 100, height = 25)

d1_inter_btn = tk.Button(window, text="D1 intermittent", command = path_change2)
d1_inter_btn.place(x=50, y = 105, width = 100, height = 25)

d1_base_btn = tk.Button(window, text="Normal", bg = 'lightsteelblue', command = path_change3)
d1_base_btn.place(x=50, y = 170, width = 100, height = 25)

d2_con_btn = tk.Button(window, text="D2 continuous", command = path_change4)
d2_con_btn.place(x=250, y = 40, width = 100, height = 25)

d2_inter_btn = tk.Button(window, text="D2 intermittent", command = path_change5)
d2_inter_btn.place(x=250, y = 105, width = 100, height = 25)

prac_con_btn = tk.Button(window, text="Train 1", bg = 'mediumseagreen', command = path_change6)
prac_con_btn.place(x=250, y = 170, width = 45, height = 25)

prac_int_btn = tk.Button(window, text="Train 2", bg = 'mediumseagreen', command = path_change7)
prac_int_btn.place(x=305, y = 170, width = 45, height = 25)

def start(event):
    global Ev_break
    Ev_num = receive()

    if Ev_num == 1:

        play_music()
    Ev_break = after_mus_play()	

receive_btn=tk.Button(window, text="Start Receive", bg='lightcoral')
receive_btn.place(x=150, y=230, width=100, height=25)
receive_btn.bind("<Button-1>", start)

window.mainloop()
