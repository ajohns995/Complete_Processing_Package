import csv
import math
import numpy
# import operator
import matplotlib.pyplot as plt
# import itertools
# import time
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

# CHANGE BELOW PER EACH PC
PATH = "Z:\\PythonProcess\\AGsurveys\\TESTDATA\\in\\"
OUT_PATH = "Z:\\PythonProcess\\AGsurveys\\TESTDATA\\out\\"  # Path of files
BEACH_NAME = "LLANDUDNO"  # Change as needed
DX = 1000  # incremenation
DY = 1000


def get_output_path():
    tk.Tk().withdraw()
    OUT_PATH = askdirectory()


# Data structure
class DataStruct:
    def __init__(self, x, y, elev, fc):
        self.x = x
        self.y = y
        self.elev = elev  # Elevation
        self.fc = fc  # Feature code (sediment Substrate)
        self.id = "NULL"
        self.chainage = 0
        self.prof = "N/A"
        self.beenSeen = False
        self.been_moved = False

    def setName(self, n):
        self.id = BEACH_NAME + "_" + str(n)

    def printValues(self):  # Print values of object
        print(f"ID: {self.id} x: {self.x} y: {self.y} elevation: {self.elev} "
              f"chainage: {self.chainage} Feature code: {self.fc}")

    def returnList(self):
        object_list = [self.x, self.y, round(self.elev, 3), round(self.chainage, 3), self.fc, self.prof, self.id]
        return object_list

    def returnGridList(self):
        ob_list = [self.x, self.y, round(self.elev, 3), self.fc]
        return ob_list

    def round_data(self, rounding_fac):
        self.xCoord = math.floor(self.x / rounding_fac) * rounding_fac
        self.yCoord = math.floor(self.y / rounding_fac) * rounding_fac

    def set_chainage(self, chain):
        self.chainage = chain

    def return_elevation_and_chainage(self):
        return [self.elev, self.chainage]

    def set_ID(self, Id):
        self.id = Id

    def return_chain_list(self):
        return [self.id, self.chainage, self.elev]

    def been_seen(self):
        self.beenSeen = True

    def moved(self):
        self.been_moved = True


# Data structure for start/end points of profile lines.
class StartEndPoints:
    def __init__(self, Estart, Nstart, Eend, Nend, prof_id):
        self.easting_start = Estart  # x1
        self.northing_start = Nstart  # y1
        self.easting_end = Eend  # x2
        self.northing_end = Nend  # y2
        self.id = prof_id

    def printValues(self):
        print(f"Profile: {self.id}, ESOL: {self.easting_start} NSOL: {self.northing_start} "
              f"EEOL: {self.easting_end}, NEOL: {self.northing_end}")


############################# DONT CHANGE ANYTHING HERE ################################################


# Reads the OS grid file
def read_ostile(filename):
    # Read the OStile map
    source = PATH + filename  # Shouldn't change!
    results = []
    results_2 = []
    with open(source, newline='') as file:
        for row in csv.reader(file):
            results.append(row)
    print(results)
    for i in range(1, len(results)):
        element = []
        element.append(results[i][0])
        element.append(int(results[i][1]))
        element.append(int(results[i][2]))
        element.append(int(results[i][3]))
        element.append(int(results[i][4]))
        results_2.append(element)

    #print(results_2)
    #input()
    return results_2


# Checks what OS tile (XX 00 00) the datapoint is in
def read_and_compare_OSTiles(data, results):
    compx = math.floor(data.xCoord / 100000) * 100000
    #print(f"compx = {compx} xGrid = {data.xCoord}")
    compy = math.floor(data.yCoord / 100000) * 100000
    #print(f"compy = {compy} yGrid = {data.yCoord}")
    for i in range(0, len(results)):
        if compx == results[i][3] and compy == results[i][4]:
            x = str(data.xCoord)
            y = str(data.yCoord)
            if data.xCoord < 100000 and data.yCoord < 100000:
                final = f"{results[i][0]} {x[0]}{x[1]}{y[0]}{y[1]}"
                return final
            elif data.xCoord < 100000 and data.yCoord >= 100000:
                final = f"{results[i][0]} {x[0]}{x[1]}{y[1]}{y[2]}"
                return final
            elif data.xCoord >= 100000 and data.yCoord < 100000:
                final = f"{results[i][0]} {x[1]}{x[2]}{y[0]}{y[1]}"
                return final
            else:
                final = f"{results[i][0]} {x[1]}{x[2]}{y[1]}{y[2]}"
                return final


# What do you think
def read_CSV(name):  # reads profile from CSV file.
    source = PATH+name  # Concatenate path and filename.
    results = []
    data_Struct = []
    with open(source, newline='') as inputfile:  # Open CSV file.
        for row in csv.reader(inputfile, delimiter='\t'):
            results.append(row)
    for i in range(1, len(results)):  # Assign values to temporary object.
        if len(results[i]) == 4:
            temp = DataStruct(float(results[i][0]), float(results[i][1]), float(results[i][2]), results[i][3])
            data_Struct.append(temp)  # Append to object list
        else:
            temp = DataStruct(float(results[i][0]), float(results[i][1]), float(results[i][2]), "M")
            data_Struct.append(temp)  # Append to object list
        print(i)
    return data_Struct  # return object


# Reads the profile CSV
def read_profiles_CSV(filename):
    results = []
    structure = []
    source = PATH + filename
    with open(source, newline='') as file:
        for row in csv.reader(file):
            print(row)
            results.append(row)
    for i in range(1, len(results)):
        temp = StartEndPoints(float(results[i][1]), float(results[i][2]),float(results[i][3]),
                              float(results[i][4]), results[i][0])
        structure.append(temp)
    return structure


# Duh
def read_txt(filename):
    source = PATH + filename
    with open(source) as file:
        lines = file.readlines()
    output = []
    print("Reading file...")
    for i in range(1, len(lines)):
        line = lines[i].split()
        if len(line) == 4:
            tmp = DataStruct(float(line[0]), float(line[1]), float(line[2]), line[3])
            output.append(tmp)
        else:
            tmp = DataStruct(float(line[0]), float(line[1]), float(line[2]), "M")
            output.append(tmp)
        print(i)
    return output


# Reads TXT data if its a txt as opposed to a csv
def read_txt_test_data(filename):
    source = PATH + filename
    with open(source) as file:
        lines = file.readlines()
    output = []
    for i in range(1, len(lines)):
        print(lines[i])
        line = lines[i].split()
        tmp  = DataStruct(float(line[0]), float(line[1]), float(line[2]), line[4])
        tmp.set_chainage(float(line[3]))
        tmp.set_ID(line[6])  # MOVE TO 6 IF PROFILE HAS FEATURE CODE
        output.append(tmp)
    return output


def get_input_file():
    tk.Tk().withdraw()
    filename = askopenfilename()
    name_list = filename.split("/")
    name = name_list[-1]
    print(name)
    if name[-4:] == ".csv":
        data = read_CSV(name)
        return data
    if name[-4:] == ".txt":
        data = read_txt(name)
        return data


# Checks the IDs in the old profiles versus the new profiles to make sure we get them all.
def findProfiles(old_data_prof, new_prof):
    profiles = set()
    for i in new_prof:
        for j in old_data_prof:
            if i.id == j.id:
                print(i.id)
                profiles.add(i)
    return profiles


# Writes a CSV line by line, is shit, needs fixing
def write_singleline_CSV(filename, object_list):
    source = OUT_PATH + filename + ".csv"
    header = ["X", "Y", "ELEVATION", "FEATURE CODE"]
    with open(source, "a", newline="") as file:
        writer = csv.writer(file)
        tmp = object_list.returnGridList()
        writer.writerow(tmp)


################################# YOU CAN CHANGE/ADD FROM HERE ON ############################################

# This isn't used
def square_solve(data, bl, tr):
    if data.x >= bl[0] and data.x <= tr[0] and data.y >= bl[1] and data.y >= tr[1]:
        return True
    else:
        return False


# Divides Base file into X-Km grid, where X is specified
def grid_division(data_z, size_m):
    os_grid = read_ostile("OStilesGRID.csv")
    data = data_z
    grid = []  # Empty list to append to
    for i in range(0, len(data)):
        data[i].round_data(size_m)  # figure out what OSTile the data point is in.
        grid.append((data[i].xCoord, data[i].yCoord))  # Append tuple
    grid = list(dict.fromkeys(grid))  # Not sure why this is here but it works??
    print(grid)  # Print grid for testing
    for j in range(0, len(data)):
        for k in range(0, len(grid)):
            if data[j].xCoord == grid[k][0] and data[j].yCoord == grid[k][1]:  # Checks if data point is within current OS tile
                write_singleline_CSV(read_and_compare_OSTiles(data[j], os_grid), data[j])  # Write data point to file
                print(j)
                # print(read_and_compare_OSTiles(data[j], os_grid))


# Don't change this
def write_chainage_csv(data, filename):
    source = OUT_PATH + filename
    header = ["Easting", "Northing", "Elevation_OD", "Chainage", "FC", "Profile", "Reg_ID"]
    with open(source, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for i in data:
            tmp = i.returnList()
            writer.writerow(tmp)


# Original chainage function, isn't used now
def lines(startx, endx, starty, endy, data, id):
    start = (startx, starty)
    end = (endx, endy)
    m = (end[1] - start[1]) / (end[0] - start[0])
    # print(m)
    c = starty - (m * startx)
    # print(f"y = {m}x + {c}")
    # input()
    A = -m
    C = -c
    B = 1
    h = numpy.sqrt(((end[0] - start[0]) ** 2) + ((end[1] - start[1]) ** 2))
    output = []
    for p in data:
        dist = numpy.abs((A * p.x) + (B * p.y) + C) / numpy.sqrt((A ** 2) + (B ** 2))
        if dist <= 1:
                # print("success!!")
            len = numpy.sqrt(((p.x - start[0]) ** 2) + ((p.y - start[1]) ** 2))
            hS = numpy.sqrt(((p.x - start[0]) ** 2) + ((p.y - start[1]) ** 2))
            hF = numpy.sqrt(((p.x - end[0]) ** 2) + ((p.y - end[1]) ** 2))

            theta = numpy.arccos(((hS ** 2) + (h ** 2) - (hF ** 2))/ (2 * h * hS))
            if theta > (numpy.pi / 2):
                len = -len
            p.set_chainage(len)
            p.set_ID(id)
            p.been_seen()
            output.append(p)
    return output


# This works out the chainage of a given point along a profile. Pretty slow but lots of math
def chainage(data, prof_data):
    count = 0
    # count2 = 0
    #array_out = []
    output = []

    for p in prof_data:
        print(p.id)
        #y = []
        #cnge = []
        #output = lines(p.easting_start, p.easting_end, p.northing_start, p.northing_end, data, p.id)
        # sortedByName = sorted(output, key=lambda x: x.elev)
        # array_out.append(output)

        startx = p.easting_start
        starty = p.northing_start
        endx = p.easting_end
        endy = p.northing_end
        start = (startx, starty)
        end = (endx, endy)
        m = (end[1] - start[1]) / (end[0] - start[0])
        # print(m)
        c = starty - (m * startx)
        # print(f"y = {m}x + {c}")
        # input()
        A = -m
        C = -c
        B = 1
        h = numpy.sqrt(((end[0] - start[0]) ** 2) + ((end[1] - start[1]) ** 2))

        for b in data:
            dist = numpy.abs((A * b.x) + (B * b.y) + C) / numpy.sqrt((A ** 2) + (B ** 2))
            if dist <= 0.1:
                # print("success!!")
                len = numpy.sqrt(((b.x - start[0]) ** 2) + ((b.y - start[1]) ** 2))
                hS = numpy.sqrt(((b.x - start[0]) ** 2) + ((b.y - start[1]) ** 2))
                hF = numpy.sqrt(((b.x - end[0]) ** 2) + ((b.y - end[1]) ** 2))

                theta = numpy.arccos(((hS ** 2) + (h ** 2) - (hF ** 2)) / (2 * h * hS))
                if theta > (numpy.pi / 2):
                    len = -len
                b.set_chainage(len)
                b.set_ID(p.id)
                # b.been_seen()
                output.append(b)
                print(count)
                # count += 1

                count += 1

    return output


# Finds structures in a file
def find_structures(data):
    print("Finding Structures...")
    count = 0
    for datum in data:
        if datum.fc == "SD":
            write_singleline_CSV("STRUCTURES_FOR_YOUR_BEACH_2022rev1", datum)
        count += 1


############################## MOST STUFF BELOW IS FOR PLOTTING AND ISN'T USED ############################


def split_chain_by_id(data):
    types = []
    for d in data:
        if not d.id in types:
            types.append(d.id)
    return types


def sort_two_values(d2_arr):
    for i in range(0, len(d2_arr[1]) - 1):
        for j in range(0, len(d2_arr[1]) - i - 1):
            if d2_arr[1][j] > d2_arr[1][j + 1]:
                tmp1 = d2_arr[0][j]
                tmp2 = d2_arr[1][j]
                d2_arr[0][j] = d2_arr[0][j+1]
                d2_arr[1][j] = d2_arr[1][j + 1]
                d2_arr[0][j+1] = tmp1
                d2_arr[1][j+1] = tmp2


def sort_old_data(odata):
    ids = split_chain_by_id(odata)
    for i in range(0, len(ids)):
        thing = []
        thing2 = []
        for j in range(0, len(odata)):
            if ids[i] == odata[j].id:
                thing.append(odata[j].chainage)
                thing2.append(odata[j].elev)

        xs, ys = zip(*sorted(zip(thing, thing2)))
        return xs, ys


def sort_by_id_and_plot(new_data, old_data):
    ids = {d.id for d in new_data}
    for i in ids:
        current_id = []
        current_id_old = []
        for n in new_data:
            for o in old_data:
                if i == n.id and i == o.id:
                    current_id.append(n)
                    current_id_old.append(o)
        plot_chainage(current_id, current_id_old)


def plot_chainage(data, old_data):
    xy1 = []
    xy2 = []
    for i in data:
        xy1.append((i.chainage, i.elev))
    for j in old_data:
        xy2.append((j.chainage, j.elev))
    x1 = numpy.zeros((2, len(xy1)))
    x2 = numpy.zeros((2, len(xy2)))
    for i in range(0, len(xy1)):
        x1[0][i] = xy1[i][0]
        x1[1][i] = xy1[i][1]
    for i in range(0, len(xy2)):
        x2[0][i] = xy2[i][0]
        x2[1][i] = xy2[i][0]
    #x1_ready = x1[x1[:,0].argsort()]
    #x2_ready = x2[x2[:,0].argsort()]
    plt.plot(x1[0], x1[1])
    plt.plot(x2[0], x2[1])
    plt.title(f'{data[0].id}')
    plt.xlabel('Chainage (m)')
    plt.ylabel('Elevation (m)')

    plt.show()


def bringDownProfile(prof_data, ID, start_chain, end_chain, decrease_factor):
    from random import uniform
    for d in prof_data:
        if d.id == ID and start_chain <= d.chainage <= end_chain:
            d.elev = d.elev - decrease_factor + (uniform(-1, 1) / 10)





