'''
Y1CS version of Brendan's game:

state: the state of the farm in a given timestep
 - represented as a list of lists, 
 - each entry of each sublist is a plot
 - indices of plots give their position on the farm

plot: a square on the farm grid
 - represented as a length 2
 - zeroth entry is type ("EMPTY", "TOMATO", "EGGPLANT", "CORN")
 - first entry is time remaining (integer)

'''
import turtle

##### Plot pseudo-class

# static properties for a plot
PLOT_SIZE = 100
TIME_REMAINING_IDX = 1
PLOT_TYPE_IDX = 0
EMPTY_PLOT = ("EMPTY", 0)


# get the image name for a plot
def get_image(plot_tuple):
    return plot_tuple[PLOT_TYPE_IDX] + ".gif"

# get the buying price for a plot
def get_buy_price(plot_tuple):
    plot_type = plot_tuple[PLOT_TYPE_IDX].upper()
    if plot_type == "TOMATO":
        return 100
    elif plot_type == "EGGPLANT":
        return 150
    elif plot_type == "CORN":
        return 250
    else:
        raise Exception("Cannot get price for plot of type " + plot_type)

def get_sell_price(plot_tuple):
    pass # TODO implement

def get_grow_time(plot_tuple):
    pass #TODO implement


###### Farm pseudo-class

# static properties for a farm
START_PHASE = "setup"
INITIAL_BALANCE = 500
NUM_ROWS = 6
NUM_COLS = 8

# instance properties of a farm
current_plot_xy = (0, 0)
phase = START_PHASE
balance = INITIAL_BALANCE
turtle = turtle.Turtle()
state = [[EMPTY_PLOT]*NUM_COLS for row in range(NUM_ROWS)] # obvi students dont know comprehensions... but ya kno


