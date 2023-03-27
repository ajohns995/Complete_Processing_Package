import pandas
import numpy
import matplotlib.pyplot as plt

PI = 3.14159


PATH_OLD = "Z:\\PythonProcess\\AGsurveys\\BeachPlotter_bigPC\\plots\\old\\"  # change me!!
PATH_NEW = "Z:\\PythonProcess\\AGsurveys\\BeachPlotter_bigPC\\plots\\new\\"  # change me!!
PATH_MID = "C:\\Users\\Admin\\Documents\\AGSurveys\\Profiling\\python\\BeachPlotter\\plots\\middle\\"  # change me!!


def path_concat(filename, type_t = None):
    if type_t == "old":
        return PATH_OLD + filename
    if type_t == "new":
        return PATH_NEW + filename
    if type_t == "middle":
        return PATH_MID + filename


def read_file(source, filetype):
    if filetype == "txt":
        df = pandas.read_csv(source, delimiter = "\t")
        return df
    elif filetype == "csv":
        data = pandas.read_csv(source)
        return data


# Function to let you zoom in using the mousewheel
def zoom_factory(ax,base_scale = 2.):
    def zoom_fun(event):
        # get the current x and y limits
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
        cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
        xdata = event.xdata # get event x location
        ydata = event.ydata # get event y location
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1/base_scale
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
            print(event.button)
        # set new limits
        ax.set_xlim([xdata - cur_xrange*scale_factor,
                     xdata + cur_xrange*scale_factor])
        ax.set_ylim([ydata - cur_yrange*scale_factor,
                     ydata + cur_yrange*scale_factor])
        plt.draw() # force re-draw

    fig = ax.get_figure() # get the figure of interest
    # attach the call back
    fig.canvas.mpl_connect('scroll_event',zoom_fun)

    #return the function
    return zoom_fun


def view_specific():
    xx = False
    yes_no = input("Would you like to view a specific profile?(y/n)")
    if yes_no == "y" or yes_no == "Y":
        xx = True
        id = input("Please enter profile ID")
        return id
    else:
        xx = False
        return xx


if __name__ == '__main__':

    data_old = pandas.read_table(path_concat("BURN3_Profiles.csv", "old"),sep='\t')  # put 2012 or nearest data here IF FILE IS COMMA DELIMITED ADD ,sep=',' in between two brackets
    #data_mid = pandas.read_csv(path_concat("data3.txt", "middle"))  # put 2017 or nearest data here IF FILE IS COMMA DELIMITED ADD ,sep=',' in between two brackets
    data_new = pandas.read_table(path_concat("Burnham3_2022tp.csv", "new"),sep='\t')  # put latest data here IF FILE IS COMMA DELIMITED ADD ,sep=',' in between two brackets

    print(data_old)
    print(data_new)

    x1 = numpy.array([data_old.loc[:,"Chainage"], data_old.loc[:,"Reg_ID"]])
    print(x1.shape)
    #x2 = numpy.array(data_mid.loc[:,"Chainage"], data_mid.loc[:,"Reg_ID"])
    x3 = numpy.array([data_new.loc[:,"Chainage"], data_new.loc[:,"Reg_ID"]])
    print(x3)

    y1 = numpy.array([data_old.loc[:, "Elevation_OD"], data_old.loc[:, "Reg_ID"]])
    #y2 = numpy.array(data_mid.loc[:, "Elevation_OD"], data_mid.loc[:, "Reg_ID"])
    y3 = numpy.array([data_new.loc[:, "Elevation_OD"], data_new.loc[:, "Reg_ID"]])

    ids = numpy.array([data_old.loc[:,"Reg_ID"]])
    numpy.append(ids, [data_new.loc[:,"Reg_ID"]])
    print(ids)
    id_final = numpy.unique(ids)

    for i in range(0, len(id_final)):
        current_x = numpy.full(len(x1[0]), PI)
        current_y = numpy.full(len(y1[0]), PI)
        old_x = numpy.full(len(x3[0]), PI)
        old_y = numpy.full(len(y3[0]), PI)
        for x in range(0, len(x1[0])):
            if id_final[i] == x1[1][x]:
                current_x[x] = x1[0][x]
                current_y[x] = y1[0][x]

        for y in range(0, len(x3[0])):
            if id_final[i] == x3[1][y]:
                old_x[y] = x3[0][y]
                old_y[y] = y3[0][y]


        print(current_x)
        print(current_y)
        fig, ax = plt.subplots()

        ax.plot(current_x[current_x != PI], current_y[current_y != PI], color='g', label='2012 data', linewidth='0.5')
        ax.plot(old_x[old_x != PI], old_y[old_y != PI], color='r', label='2017 data', linewidth='0.5')
        plt.xlabel("Chainage (m)")
        plt.ylabel("Elevation (m)")
        plt.legend()
        plt.title(id_final[i])
        ax.grid()
        scale = 1.1
        f = zoom_factory(ax, base_scale=scale)
        plt.show()  # Move me back a tab to see all figures at once
