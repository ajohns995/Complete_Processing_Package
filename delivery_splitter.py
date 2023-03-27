################################################################
#                                                              #
#                AG Surveys Delivery Splitter V1.0             #
#                                                              #
#   Author: Nicholas Fairburn                                  #
#   Version: 1.0                                               #
#   Description: Takes basefile and profiles and splits        #
#                them into deliverables.                       #
#   Changelog: none                                            #
#                                                              #
#   IMPORTANT INFORMATION - only change stuff if its           #
#                           yellow and has a file type         #
#                           after it OR you know what          #
#                           you're doing!! There are           #
#                           more functions available           #
#                           for use, just ask me and           #
#                           I'll enable/write one for          #
#                           you. Happy surveying! :-)          #
#                                                              #
################################################################

from funcs import *
# from sort_csv import *
# from func_scripts import success_msg
import time


def delivery_main():
    # profiles_d = read_profiles_CSV("TSW4_All_Profiles.csv")  # PROFILES GO HERE (ESOL, NSOL, ETC)
    # get_output_path()

    #data = read_txt("7dPARR2_20220812tb.txt")  # 1m BASE FILE GOES HERE
    data = get_input_file()
    #data2 = read_txt("")  # 0.1m BASE FILE GOES HERE
    # old_data = read_txt_test_data("7dBURN3_20120112tp.txt")  # STICK SOME OLD PROFILE DATA HERE (UNLESS YOUVE SCANNED NEW PROFILES SINCE)
    # profs = findProfiles(old_data, profiles_d)  # Makes sure it only checks the profiles on the beach.
    # input()
    # print(profs)
    start = time.time()  # Make sure we're going sonic speed.
    # out = chainage(data, profs)
    #out2 = chainage(data2, profs) # Workout the chainage
    # write_chainage_csv(out, "Burnham3_2022tp.csv")  # Writes the chainage to file.
    #write_chainage_csv(out2, "profs2.csv")
    # input("PLEASE STOP ME")
    find_structures(data)  # divides the structures up.
    grid_division(data, 1000)  # Divides the beach into a grid (change the number for different sized grids!!! although OS ref will be wrong)
    addHeaders() # YOU CAN TEST ME, IF I DON'T WORK PUT A # IN FRONT OF THE LINE
    end = time.time()
    bigboy = end - start  # timing variable

    print(f" completed in {bigboy / 60} minutes")  # "Was I a fast boy?" "No... You were the fastest"
