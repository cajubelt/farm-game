import turtle

class Constants:
    """Constants for game settings"""
    PLOT_SIZE = 100
    INITIAL_BALANCE = 500
    X_MAXIMUM = 8
    Y_MAXIMUM = 6
    BUY_PRICE = {"tomato": 100, "eggplant": 150, "corn": 250}
    GROW_TIME = {"tomato": 3, "eggplant": 4, "corn": 5}
    SELL_PRICE = {"tomato": 300, "eggplant": 500, "corn": 1000}

class Plot:
    def __init__(self, x, y, side_len, texture = None, time_remaining = None):
        """"
        Initialize a new Plot.
        Args:
            x (int), y (int) = coordinates of lower left corner
            side_len (int)
            texture (string) = current type of the plot (eggplant, tomato, corn)
            time_remaining (int) = remaining grow-time in rounds
        """
        self.x = x
        self.y = y
        self.side_len = side_len
        self.texture = texture
        self.time_remaining = time_remaining

class Farm:
    def __init__(self):
        """Initialize a new Farm and begin the game."""
        self.state = 'setup'
        self.balance = Constants.INITIAL_BALANCE
        self.plots = {(x, y): Plot(x, y, Constants.PLOT_SIZE) for x in range(Constants.X_MAXIMUM) for y in range(Constants.Y_MAXIMUM)}
        self.current_plot = self.plots[0,0]
        self.rt = turtle.Turtle()
        self.round = 0

    def drawsquare(self, t, plot):
        """
        Helper for render.
        Args: turtle instance, Plot instance.
        """
        t.pen({"speed": 0, "pencolor": "white", "pensize": 2, "pendown": False, "shown": False})
        x = Constants.PLOT_SIZE * (plot.x - Constants.X_MAXIMUM/2)
        y = Constants.PLOT_SIZE * (plot.y - Constants.Y_MAXIMUM/2)
        side = plot.side_len

        if plot == self.current_plot:
            t.pen({"pencolor": "blue", "pensize": 3})

        #Draw outline of square
        t.goto(x,y)
        t.pendown()
        t.setx(x+side)
        t.sety(y+side)
        t.setx(x)
        t.sety(y)

        #Add textures!
        if plot.texture != None:
            t.goto(x+side/2, y+side/2)
            if plot.time_remaining == 1:
                t.shape("money.gif")
            else:
                t.shape(plot.texture + ".gif")
            t.stamp()


    def write_balance(self):
        x = Constants.PLOT_SIZE*Constants.X_MAXIMUM/2
        y = Constants.PLOT_SIZE*Constants.Y_MAXIMUM/2
        self.rt.penup()
        self.rt.goto(x,y)
        self.rt.pendown()
        self.rt.write(str(self.balance), font=("Arial", 12, "normal"))

    def write_round(self, round):
        x = -Constants.PLOT_SIZE*Constants.X_MAXIMUM/2
        y = Constants.PLOT_SIZE*Constants.Y_MAXIMUM/2
        self.rt.penup()
        self.rt.goto(x,y)
        self.rt.pendown()
        self.rt.write("Round: " + str(round+1), font=("Arial", 12, "normal"))

    def write_score(self):
        self.rt.clear()
        self.rt.penup()
        self.rt.goto(0,0)
        self.rt.pendown()
        self.rt.write("SCORE: " +  str(self.balance), font=("Arial", 48, "normal"), align = "center")
        turtle.update()

    def write_instructions(self):
        x = -Constants.PLOT_SIZE*(Constants.X_MAXIMUM/2 - 1.5)
        y = -Constants.PLOT_SIZE*(Constants.Y_MAXIMUM/2 + .75)
        instruct_turtle = turtle.Turtle()
        instruct_turtle.hideturtle()
        instruct_turtle.speed(10)
        instruct_turtle.penup()
        instruct_turtle.goto(x,y)
        instruct_turtle.pendown()
        instruct_turtle.write("T = Tomato: Buy = 100, Sell = 300, Time = 3\nE = Eggplant: Buy = 150, Sell = 500, Time = 4\nC = Corn: Buy = 250, Sell = 1000, Time = 5\nP = Progress to Next Round", font=("Arial", 10, "normal"), align = "left")

    def render(self):
        """"Renders all plots on the screen."""
        self.rt.clear()
        self.rt.hideturtle()
        self.rt.tracer(0,0)
        for plot in self.plots.values():
            if plot != self.current_plot:
                self.drawsquare(self.rt, plot)
        self.drawsquare(self.rt, self.current_plot)
        self.write_balance()
        self.write_round(self.round)
        turtle.update()

    """
    Helper functions for setup. Change the highlighted plot based on
    the keypress.
    """
    def select_up(self):
        if self.current_plot.y != Constants.Y_MAXIMUM - 1:
            self.current_plot = self.plots[self.current_plot.x, self.current_plot.y+1]

    def select_down(self):
        if self.current_plot.y != 0:
            self.current_plot = self.plots[self.current_plot.x, self.current_plot.y-1]

    def select_left(self):
        if self.current_plot.y != 0:
            self.current_plot = self.plots[self.current_plot.x-1, self.current_plot.y]

    def select_right(self):
        if self.current_plot.y != Constants.X_MAXIMUM - 1:
            self.current_plot = self.plots[self.current_plot.x+1, self.current_plot.y]

    def buy(self, texture):
        if self.current_plot.texture == None and self.balance >= Constants.BUY_PRICE[texture]:
            self.current_plot.texture = texture
            self.current_plot.time_remaining = Constants.GROW_TIME[texture]
            self.balance -= Constants.BUY_PRICE[texture]

    def buy_corn(self):
        self.buy("corn")

    def buy_eggplant(self):
        self.buy("eggplant")

    def buy_tomato(self):
        self.buy("tomato")

    def play(self):
        self.write_instructions()
        while self.round <= 9:
            self.setup()
            self.timestep()
            self.round += 1
        self.write_score()

    def setup(self):
        """
        Manual stage of each turn. The blue highlight indicates currently-selected plot.
        Player-controlled buy/sell transactions occur here.
        """
        while(self.state == 'setup'):
            self.render()
            turtle.onkey(self.select_up, "Up")
            turtle.onkey(self.select_down, "Down")
            turtle.onkey(self.select_left, "Left")
            turtle.onkey(self.select_right, "Right")
            turtle.onkey(self.buy_corn, "c")
            turtle.onkey(self.buy_eggplant, "e")
            turtle.onkey(self.buy_tomato, "t")
            turtle.onkey(self.start_timestep, "p")
            turtle.listen()

    def start_timestep(self):
        self.state = "timestep"

    def timestep(self):
        for plot in self.plots.values():
            if plot.texture != None and plot.time_remaining > 0:
                plot.time_remaining -= 1
            if plot.time_remaining == 0:
                self.balance += Constants.SELL_PRICE[plot.texture]
                plot.texture = None
                plot.time_remaining = None
        self.state = "setup"


if __name__ == '__main__':
    wn = turtle.Screen()
    wn.bgpic('grass.gif')
    wn.register_shape('tomato.gif')
    wn.register_shape('corn.gif')
    wn.register_shape('eggplant.gif')
    wn.register_shape('seed.gif')
    wn.register_shape('money.gif')
    f = Farm()
    f.play()
    wn.exitonclick()
