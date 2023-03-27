import pandas as pd
import numpy as np
# import time
import tkinter as t_k     # from tkinter import Tk for Python 3.x
# from tkinter.filedialog import askopenfilename
# from tkinter.filedialog import askdirectory
from delivery_splitter import *

inp = None


def success_msg():
    msg = t_k.Tk()
    msg.geometry("300x300")
    lb = t_k.Label(msg, text="Success!")
    lb.pack()
    b_ = t_k.Button(msg, text="OK", command=lambda: msg.destroy())
    b_.pack()


def get_output_dir():
    t_k.Tk().withdraw()
    var = askdirectory()
    var += "/"
    return var


def file_dialog():
    t_k.Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    print(filename)
    return filename


def read_data(filename, delimiter=','):
    data = pd.read_table(filename, sep=delimiter, low_memory=False)
    print(data)
    return data


def split_csv(data, file_name):
    out = get_output_dir()
    print(out)
    amount_of_lines = len(data)
    print(amount_of_lines)
    file_numbers = round(amount_of_lines, -6) // 1_000_000
    print(file_numbers)
    if amount_of_lines < 1_000_000:
        print("Too small!")
    else:
        sep_files = np.array_split(data, file_numbers + 1)
        for i in range(0, len(sep_files)):
            sep_files[i].to_csv(f"{out}{file_name}_{i}.csv", sep='\t', index=False)
        success_msg()


def split_call(filename, delim):
    name_list = filename.split("/")
    name = name_list[-1]
    name = name[:-4]
    print(name)
    if delim == "comma":
        dat = read_data(filename)
        split_csv(dat, name)
        success_msg()
    elif delim == "tab":
        dat = read_data(filename, delimiter="\t")
        split_csv(dat, name)
        # success_msg()


def split_csv_dialog():
    file_t = file_dialog()
    root = t_k.Tk()
    root.title("How is the current file delimited?")
    root.geometry('700x500')
    # TextBox Creation
    print_button = t_k.Button(root, text="Comma", command=lambda: split_call(file_t, "comma"))
    print_button.pack()
    print2_button = t_k.Button(root, text="Tab", command=lambda: split_call(file_t, "tab"))
    print2_button.pack()


def convert_csv():
    file_t = file_dialog()
    out = get_output_dir()
    name_list = file_t.split("/")
    name = name_list[-1]
    name = name[:-4]
    data_t = read_data(file_t)
    print(f"{out}{name}.csv")
    data_t.to_csv(f"{out}{name}.csv", sep='\t', index=False)
    success_msg()


def merge_continued(num_of_merges):
    file_list = []
    data_list = []
    for i in range(0, num_of_merges):
        print(f"\n{i}")
        tmp = file_dialog()
        file_list.append(tmp)
    out_name = file_list[0].split("/")
    name = out_name[-1]
    name = name[:-4]
    for x in file_list:
        tmp = pd.read_table(x, delimiter="\t", low_memory=False)
        print(tmp)
        data_list.append(tmp)
    out_data = pd.concat(data_list, ignore_index=True)
    out = get_output_dir()
    out_data.to_csv(f"{out}{name}_MERGED.csv", sep="\t", index=False)
    print(out_data)
    success_msg()


def merge_csvs():
    root = t_k.Tk()
    root.geometry("400x200")
    text_out = ""
    var = t_k.StringVar()

    def take_input():
        global inp
        INPUT = inputtxt.get("1.0", "end-1c")
        inp = INPUT
        print(inp)
        inp = int(inp)
        merge_continued(inp)

    lab_ = t_k.Label(root, text="How many CSVs do you need to merge?")
    inputtxt = t_k.Text(root,
                        height=10,
                        width=25,
                        bg="light yellow")
    display = t_k.Button(root,
                         text="Okay",
                         command=lambda: take_input())
    inputtxt.pack()
    display.pack()
    lab_.pack()


def main_menu():
    # Create the default window
    root = t_k.Tk()
    root.title("CSV/TXT Merge/split/convert")
    root.geometry('700x500')

    # Submit button
    # Whenever we click the submit button, our submitted
    # option is printed ---Testing purpose
    convert_button = t_k.Button(root,
                                height=5,
                                width=60,
                                text='Convert from comma delimited to tab delimited',
                                command=convert_csv)
    convert_button.pack(side=t_k.BOTTOM)
    split_button = t_k.Button(root,
                              height=5,
                              width=60,
                              text='Split CSV file',
                              command=split_csv_dialog)
    split_button.pack(side=t_k.BOTTOM)
    merge_button = t_k.Button(root,
                              height=5,
                              width=60,
                              text='Merge CSV',
                              command=merge_csvs)
    merge_button.pack(side=t_k.BOTTOM)
    delivery_button = t_k.Button(root,
                                 height=5,
                                 width=60,
                                 text='Split Base into OSTiles',
                                 command=delivery_main)
    delivery_button.pack(side=t_k.BOTTOM)
