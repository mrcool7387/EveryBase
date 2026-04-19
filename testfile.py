######################################
#  _______        _    __ _ _        #
# |__   __|      | |  / _(_) |       #
#    | | ___  ___| |_| |_ _| | ___   #
#    | |/ _ \/ __| __|  _| | |/ _ \  #
#    | |  __/\__ \ |_| | | | |  __/  #
#    |_|\___||___/\__|_| |_|_|\___|  #
######################################
# This file is just used for testing #
# some python functions.             #
######################################

# region Markers
def unfunctional(func):
    return func

def functional(func):
    return func
# endregion Markers

@unfunctional
def plusequal_for_sets():
    x = {1, 2, 3}
    x += set([4])

@functional
def plusequal_for_lists():
    x = [1, 2, 3]
    x += [4]

if __name__ == "__main__":
    plusequal_for_lists()