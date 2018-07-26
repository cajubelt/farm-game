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

def get_new_plot(type):
    type = type.upper()
    time = get_grow_time(type)
    return type, time

# helper for get_new_plot
def get_grow_time(type):
    if type == "TOMATO":
        return 3
    elif type == "EGGPLANT":
        return 4
    elif type == "CORN":
        return 5
    elif type == "EMPTY":
        return 0
    else:
        raise Exception("cannot get new plot of type {}".format(type))

# get the image name for a plot
def get_image(plot_tuple):
    type = plot_tuple[PLOT_TYPE_IDX]
    if type == "EMPTY":
        return None
    else:
        return type.lower() + ".gif"

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
        raise Exception("Cannot get buy price for plot of type " + plot_type)

def get_time_remaining(plot_tuple):
    return plot_tuple[TIME_REMAINING_IDX]

def get_sell_price(plot_tuple):
    plot_type = plot_tuple[PLOT_TYPE_IDX].upper()
    if plot_type == "TOMATO":
        return 300
    elif plot_type == "EGGPLANT":
        return 500
    elif plot_type == "CORN":
        return 1000
    elif plot_type == "EMPTY":
        return 0
    else:
        raise Exception("Cannot get sell price for plot of type " + plot_type)

def decrement_time(plot_tuple):
    return plot_tuple[0], max(plot_tuple[1] - 1, 0)

###### Farm pseudo-class

# static properties for a farm
START_PHASE = "setup"
INITIAL_BALANCE = 500
NUM_COLS = 6
NUM_ROWS = 6
COORD_TUPLE_X_IDX = 0
COORD_TUPLE_Y_IDX = 1

# instance properties of a farm
current_plot_xy = (0, 0)
phase = START_PHASE
balance = INITIAL_BALANCE
farm_turtle = turtle.Turtle()
state = [[EMPTY_PLOT]*NUM_COLS for row in range(NUM_ROWS)] # obvi students dont know comprehensions... but ya kno
round = 0

def draw_square(plot_tuple, plot_coords):
    farm_turtle.pen({"speed": 0, "pencolor": "white", "pensize": 2, "pendown": False, "shown": False})
    x_coord = plot_coords[COORD_TUPLE_X_IDX]
    x = PLOT_SIZE * (x_coord - NUM_COLS / 2) # changed to turtle frame
    y_coord = plot_coords[COORD_TUPLE_Y_IDX]
    y = PLOT_SIZE * (y_coord - NUM_ROWS / 2) # changed to turtle frame
    side = PLOT_SIZE
    if plot_coords==current_plot_xy:
        farm_turtle.pen({"pencolor": "blue", "pensize": 3})

    # Draw outline of square
    farm_turtle.goto(x, y)
    farm_turtle.pendown()
    farm_turtle.setx(x + side)
    farm_turtle.sety(y + side)
    farm_turtle.setx(x)
    farm_turtle.sety(y)

    # Add textures!
    image_filename = get_image(plot_tuple)
    if image_filename != None:
        farm_turtle.goto(x+side/2, y+side/2)
        time_remaining = get_time_remaining(plot_tuple)
        if time_remaining == 1:
            farm_turtle.shape("money.gif")
        else:
            farm_turtle.shape(image_filename)
        farm_turtle.stamp()

def write_balance():
    balance_msg = "Balance: " + str(balance)
    x = PLOT_SIZE * (NUM_COLS // 2) - len(balance_msg)*8  # make sure balance msg fits
    y = PLOT_SIZE * (NUM_ROWS // 2)
    farm_turtle.penup()
    farm_turtle.goto(x,y)
    farm_turtle.pendown()
    farm_turtle.write(balance_msg, font=("Arial", 12, "normal"))
    
def write_round():
    x = -PLOT_SIZE*NUM_COLS/2
    y = PLOT_SIZE*NUM_ROWS/2
    farm_turtle.penup()
    farm_turtle.goto(x,y)
    farm_turtle.pendown()
    farm_turtle.write("Round: " + str(round+1), font=("Arial", 12, "normal"))
    
def write_score():
    farm_turtle.clear()
    farm_turtle.penup()
    farm_turtle.goto(0, 0)
    farm_turtle.pendown()
    farm_turtle.write("SCORE: " + str(balance), font=("Arial", 48, "normal"), align="center")
    turtle.update()


def render(wn):
    """"Renders all plots on the screen."""
    farm_turtle.clear()
    farm_turtle.hideturtle()
    wn.tracer(0, 0)
    global current_plot_xy
    global state
    for row_idx in range(NUM_ROWS):
        for col_idx in range(NUM_COLS):
            plot = state[row_idx][col_idx]
            plot_coords = row_idx, col_idx
            draw_square(plot, plot_coords)
    current_plot = state[current_plot_xy[0]][current_plot_xy[1]]
    draw_square(current_plot, current_plot_xy)
    write_balance()
    write_round()
    turtle.update()

"""
Helper functions for setup. Change the highlighted plot based on
the keypress.
"""
def select_up():
    global current_plot_xy
    current_plot_xy = current_plot_xy[0], min(current_plot_xy[1]+1, NUM_COLS - 1)

def select_down():
    global current_plot_xy
    current_plot_xy = current_plot_xy[0], max(current_plot_xy[1]-1,0)

def select_left():
    global current_plot_xy
    current_plot_xy = max(current_plot_xy[0] - 1, 0), current_plot_xy[1]

def select_right():
    global current_plot_xy
    current_plot_xy = min(current_plot_xy[0] + 1, NUM_ROWS-1), current_plot_xy[1]

# buy the current highlighted plot
def buy(plot_type):
    global current_plot_xy
    global balance
    global state
    new_plot = get_new_plot(plot_type)
    if balance >= get_buy_price(new_plot):  # NOTE: allows you to buy / plant over an existing crop
        state[current_plot_xy[0]][current_plot_xy[1]] = new_plot
        balance -= get_buy_price(new_plot)

def buy_corn():
    buy("corn")

def buy_eggplant():
    buy("eggplant")

def buy_tomato():
    buy("tomato")

def play(wn):
    global round
    while round <= 9:
        setup(wn)
        timestep()
        round += 1
    write_score()

def setup(wn):
    """
    Manual stage of each turn. The blue highlight indicates currently-selected plot.
    Player-controlled buy/sell transactions occur here.
    """
    global phase
    while phase == 'setup':
        render(wn)
        turtle.onkey(select_up, "Up")
        turtle.onkey(select_down, "Down")
        turtle.onkey(select_left, "Left")
        turtle.onkey(select_right, "Right")
        turtle.onkey(buy_corn, "c")
        turtle.onkey(buy_eggplant, "e")
        turtle.onkey(buy_tomato, "t")
        turtle.onkey(start_timestep, "p")
        turtle.listen()


def start_timestep():
    global phase
    phase = "timestep"


def timestep():
    global state
    global balance
    for row_idx in range(NUM_ROWS):
        for col_idx in range(NUM_COLS):
            plot = state[row_idx][col_idx]
            new_plot = decrement_time(plot)
            state[row_idx][col_idx] = new_plot
            if new_plot[TIME_REMAINING_IDX] == 0:
                balance += get_sell_price(new_plot)
                state[row_idx][col_idx] = EMPTY_PLOT
    global phase
    phase = "setup"

if __name__ == '__main__':
    wn = turtle.Screen()
    # wn.setup(width=(PLOT_SIZE*NUM_COLS + 5), height=(PLOT_SIZE*NUM_ROWS + 5))
    wn.setup(width=(NUM_COLS*PLOT_SIZE + 60), height=(NUM_ROWS*PLOT_SIZE + 60))
    wn.bgpic('grass.gif')
    wn.register_shape('tomato.gif')
    wn.register_shape('corn.gif')
    wn.register_shape('eggplant.gif')
    wn.register_shape('seed.gif')
    wn.register_shape('money.gif')
    play(wn)
    wn.exitonclick()
