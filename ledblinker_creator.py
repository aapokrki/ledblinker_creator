"""
COMP.CS.100 Ohjelmointi 1.
Tekijä: Aapo Kärki
Opiskelijanumero: H292001git
Mail: aapo.karki@tuni.fi

An interactive tool to create simple animations for led blinkers.
Outputs a functional code, ready to be downloaded into a led blinker.
"""

from tkinter import *
from functools import partial
from itertools import product


class Ledivilkutin:
    def __init__(self):
        """
        Created all needed variables(lists and such)
        that get built more during methods
        """
        # all led ids(0-255)
        self.__led_ids = []

        # all currenty lit leds
        self.__lit = []

        # default led color
        self.__lit_color = "pink"

        # all frames as a list (lists of led ids as a list)
        self.__every_state = []

        # dict to connect id(0-255) to corresponding hexadecimal number
        self.__idtohex = {}

        # string of current code that's on the grid
        self.__codestring = ""

        # empty string for time in hex format
        self.__hex_time = ""

        """
        Main window
        Contains the led grid, all buttons and such
        """
        self.__root = Tk()
        self.__frame = Frame(self.__root)
        self.__frame.grid()
        self.__root.minsize(width=270, height=270)
        self.__root.title("Led Blinker Helper")

        # Calls a function to create the 16x16 LED grid
        self.create_grid(self.__frame, 30, 30)

        # Button to convert lit leds to a code and print that code
        # to self.__current text box.
        self.__printcode = Button(self.__frame,
                                  text="Print",
                                  command=self.printcode)
        self.__printcode.grid(column=16,
                              row=1,
                              sticky="W",
                              ipadx=5)

        # Holds current code from the grid as a string.
        self.__currentcode = Text(self.__frame,
                                  height=4,
                                  width=30)
        self.__currentcode.grid(column=16,
                                rowspan=3,
                                columnspan=3,
                                row=2,
                                sticky="N")

        # Applies code from self.__currentcode to the end of self.__finalcode
        # using method self.applycode
        self.__applycode = Button(self.__frame,
                                  text="Add Frame",
                                  command=self.applycode)
        self.__applycode.grid(column=17,
                              row=1,
                              sticky="E",
                              ipadx=5,
                              columnspan=2)

        # Button that clears the led grid and self.__currentcode
        self.__cleargrid = Button(self.__frame,
                                  text="Clear",
                                  command=self.clear,
                                  width=10)
        self.__cleargrid.grid(row=0,
                              column=0,
                              columnspan=3)

        # Button that inverts leds that are on and off
        self.__invert = Button(self.__frame,
                               text="Fill/Invert",
                               command=self.fill_invert,
                               width=10)
        self.__invert.grid(row=0,
                           column=3,
                           columnspan=3)

        # User inputs the pause time between frames (ms)
        self.__wait = Entry(self.__frame,
                            width=10,
                            justify="center")
        # Default pause time is ONE second
        self.__wait.insert(END, "1000")
        self.__wait.grid(column=17,
                         row=4,
                         columnspan=1,
                         sticky="W")
        # Prompt text
        self.__wait_text = Label(self.__frame, text="Pause after frame:")
        self.__wait_text.grid(column=16,
                              row=4,
                              sticky="E",
                              )

        self.__wait_ms = Label(self.__frame, text="ms")
        self.__wait_ms.grid(column=18,
                            row=4,
                            sticky="W")

        # if input != number, display ERROR
        self.__wait_info = Label(self.__frame, fg="red")
        self.__wait_info.grid(row=5,
                              column=16,
                              columnspan=3,
                              rowspan=2,
                              sticky="N")

        # lets user input the led color they want
        self.__user_lit_color = Entry(self.__frame,
                                      width=10,
                                      justify="center")
        self.__user_lit_color.grid(row=6,
                                   column=17,
                                   sticky="W",
                                   columnspan=2)

        # prompt
        self.__user_lit_color_text = Label(self.__frame, text="Led color:")
        self.__user_lit_color_text.grid(row=6,
                                        column=16,
                                        sticky="E",

                                        columnspan=1)

        # applies chosen color
        self.__user_lit_color_apply = Button(self.__frame,
                                             text="Apply",
                                             width=5,
                                             command=self.apply_user_color)
        self.__user_lit_color_apply.grid(row=6,
                                         column=18,
                                         sticky="W",
                                         columnspan=2,)
        # sample of the color in use
        self.__user_lit_color_sample = Label(self.__frame,
                                             width=9,
                                             height=2,
                                             bg=self.__lit_color,
                                             relief=RAISED)
        self.__user_lit_color_sample.grid(row=6,
                                          column=17,
                                          sticky="W",
                                          columnspan=4,
                                          rowspan=3)

        # checkbox for 'Easymode'
        # Checked on startup
        self.__easymodevar = IntVar(value=1)
        self.__easymode = Checkbutton(self.__frame,
                                      text="Easy animation",
                                      variable=self.__easymodevar,
                                      onvalue=1)
        self.__easymode.grid(row=9,
                             column=15,
                             columnspan=3)

        # button to open a new window that allows cycling between frames
        self.__preview = Button(self.__frame,
                                text="Preview",
                                command=self.preview,
                                width=10)
        self.__preview.grid(column=18,
                            row=9,
                            sticky="E")

        # Holds the final code that can be imported to a blinker
        self.__finalcode = Text(self.__frame,
                                height=10,
                                width=30)
        self.__finalcode.grid(column=16,
                              rowspan=5,
                              columnspan=3,
                              row=10,
                              sticky="N")

        # Button to set everything to default values
        self.__restart_program = Button(self.__frame,
                                        text="Restart",
                                        command=self.restart,
                                        width=10)
        self.__restart_program.grid(column=18,
                                    row=16)

    def create_grid(self, window, x, y):
        """
        Method for creating a 16x16 grid of buttons

        :param window: specifies the window in which the grid will be built to
        :param x: button width
        :param y: button height
        :return:
        """
        positions = product(range(1, 17), range(16))
        for i in range(17):
            # shape the grid
            Canvas(window, width=x, height=0).grid(row=15, column=i)
            Canvas(window, width=0, height=y).grid(row=i, column=15)

        # creates buttons for the grid
        for i, item in enumerate(positions):
            self.__led = Button(window,
                                command=partial(self.change, i),
                                bg="chartreuse4")
            self.__led.grid(row=item[0], column=item[1], sticky="n,e,s,w")

            # adds buttons to a list
            self.__led_ids.append(self.__led)

            # converts id to a hexadecimal and stores id and hex(id) to a dict
            hex_clean = hex(i).lstrip("0x")

            # fills hexadecimals to NN (eg. A -> 0A)
            if len(hex_clean) < 2:
                if len(hex_clean) < 1:
                    hex_clean = "0" + hex_clean

                hex_clean = "0" + hex_clean

            self.__idtohex[i] = hex_clean

    def apply_user_color(self):
        """
        Applies user's color of choice as the color of lit leds.
        :return:
        """
        try:
            self.__lit_color = self.__user_lit_color.get()
            self.__user_lit_color_sample.configure(bg=self.__lit_color,
                                                   text="")

        except TclError:
            self.__lit_color = "pink"
            self.__user_lit_color_sample.configure(text="Invalid!",
                                                   bg="grey94",
                                                   fg="red")

    def change(self, i):
        """
        Changes button colour after press
        adds pressed button's id to a list of lit leds
        :param i: button id
        :return:
        """
        # turns led on (AKA. changes bg)
        if i not in self.__lit:
            bname = (self.__led_ids[i])
            bname.configure(bg=self.__lit_color)

            # adds led's id to a list
            self.__lit.append(i)

        # if led is already on, turn it off (AKA. changes bg to dark green)
        else:
            bname = (self.__led_ids[i])
            bname.configure(bg="chartreuse4")

            # led is no longer lit, so it is removed from the list
            self.__lit.remove(i)

    def clear(self):
        """
        Turns all leds off using 'self.change'
        and clears 'self.__currentcode' text box.
        :return:
        """
        # temporary copy to remember how many leds must be turned off
        lit_copy = self.__lit.copy()
        for i in lit_copy:
            self.change(i)

        # clears 'self.__currentcode' text box
        self.__currentcode.delete(1.0, END)

    def fill_invert(self):
        for id in self.__idtohex.keys():
            print(id)
            self.change(id)

    def printcode(self):
        """
        Converts lit leds into a code that a led blinker can read.

        :return:
        """
        # clears codestring before adding anything
        self.__codestring = ""

        # clears 'self.__currentcode' textbox
        self.__currentcode.delete(1.0, END)

        # sets self.__hex_time to empty, so previous time inputs wont worry us
        self.__hex_time = ""

        # creater new self.__hex_time from user's input
        self.wait_time_to_hex()

        # adds 's' in front of led hexs to "select" them for effects
        # the led blinker code requires this
        for id in self.__lit:
            self.__codestring += "s" + self.__idtohex[id].upper()

        # adds "turn leds on 100%" command "e0f" to the start of the string
        self.__codestring = "e0f" + self.__codestring

        # adds pausetime after frame, to the string's end
        self.__codestring += self.__hex_time

        # inserts finished code to 'self.__currentcode' text box
        # for the user to see
        self.__currentcode.insert(END, self.__codestring)

    def wait_time_to_hex(self):
        """
        Converts given inputs (ms) into NNNN hexadecimal numbers
        Adds command 'w' to "Wait", for NNNN time (eg. w0042 = wait 1 second)
        :return:
        """
        try:
            #doesnt add wait 'Wait' command if input is minus or somethin else
            if self.__wait.get() != "f" and int(self.__wait.get()) > 0:
                wait_as_unit = int(int(self.__wait.get())/15)
                print(wait_as_unit)
                self.__hex_time = hex(wait_as_unit).lstrip("0x")

                # makes every hex number have 4 characters
                if len(self.__hex_time) < 4:
                    while len(self.__hex_time) < 4:
                        self.__hex_time = "0" + self.__hex_time

                # add 'w' "Wait" command in front
                self.__hex_time = "w" + self.__hex_time

                # deletes error message
                self.__wait_info.configure(text="")

            elif self.__wait.get() == "f":

                # add 'w' "Wait" command in front
                self.__hex_time = "wfff"

                # deletes error message
                self.__wait_info.configure(text="Loop ends after this frame!")

        except ValueError:
            # user's input cannot be anything else than numbers
            self.__wait_info.configure(text="ERROR\n"
                                             "Input must be a number!")

    def restart(self):
        """
        Returns everything to their base values
        so that the user may start all over again
        note: Doesn't restore led color as the user probably wouldn't want that
        :return:
        """
        self.__finalcode.delete(1.0, END)
        self.__every_state = []
        self.clear()
        self.__wait_info.configure(text="")
        try:
            self.__preview_window.destroy()
        except:
            pass

        self.__wait.delete(0, END)
        self.__wait.insert(END, "1000")




    def applycode(self):
        """
        Adds codestring (same as in self.__currentcode) to final code
        If Easymode is on -> call easymode
        Keeps track of lit leds on each frame using list
        :return:
        """
        # holds information of lit leds from every frame
        self.__every_state.append(list(self.__lit))

        if self.__easymodevar.get() == 1 and len(self.__every_state) > 1:
            self.easymode()

        else:
            self.__finalcode.insert(END, self.__codestring)

    def easymode(self):
        """
        Mode that creates a clutter free code for the led blinker
        Automatically adds a "turn off" command to leds that aren't turned on
        in the next frame.
        Also NEVER turns leds 'on' twice in a row
        Makes animation significantly easier

        :return:
        """
        # base strings of leds to turn on and off
        new_leds_string = ""
        turn_off_string = ""

        # determines which leds must be turned off
        # AKA. what leds were on in the last frame, but aren't on in the next
        leds_to_turn_off = list(set(self.__every_state[-2])
                                .difference((self.__every_state[-1])))

        # doesn't add "Turn off" command if there a no leds to turn off
        if len(leds_to_turn_off) != 0:
            turn_off_string = "e00"

        # adds "select" commad infront of each led
        for id in leds_to_turn_off:
            turn_off_string += "s" + self.__idtohex[id].upper()

        # adds string command to turn off needed leds
        # that the led blinker can read
        self.__finalcode.insert(END, turn_off_string)

        # list of leds that need to be turned on
        # AKA. What leds are on in current frame
        # that were not on in the previous frame
        new_leds = list(
            set(self.__every_state[-1]).difference(self.__every_state[-2]))

        # if no leds to command "On 100%" , dont add command
        if len(new_leds) != 0:
            new_leds_string = "e0f"

        # adds 'select' command infront of leds
        for id in new_leds:
            new_leds_string += "s" + self.__idtohex[id].upper()

        # adds pause time to the end
        # if no new leds turned on, only adds pause time to the final code
        new_leds_string += self.__hex_time

        self.__finalcode.insert(END, new_leds_string)

    def preview(self):
        """
        Opens a new window that allows the user to cycle between saved frames
        using RIGHT ARROW KEY
        :return:
        """

        self.__preview_window = Tk()
        self.__preview_frame = Frame(self.__preview_window)
        self.__preview_window.title("Preview")
        self.__preview_window.minsize(width=200,
                                      height=200)

        # The current frame the user is on at the moment
        self.__current_frame = 0

        # Binds RIGHT ARROW KEY to command self.next_frame
        self.__preview_window.bind('<Right>', self.next_frame)

        # Infobox to show the ropes
        self.__infotext = Label(self.__preview_window,
                                text="Press the \n"
                                     "RIGHT ARROW KEY\n"
                                     "to cycle between frames!")
        self.__infotext.pack(expand=True)

    def next_frame(self, key):
        """
        Allows the user to cycle between frames with a key press
        Loops saved frames as an animation

        #:param key: user input RIGHT ARROW KEY
        :return:
        """
        # clears text box for prettiness
        if self.__currentcode != "":
            self.clear()

        # inputs a single frame's all led ids to self.change through a loop
        # end result shows current frame on the LED grid
        try:
            for led in self.__every_state[self.__current_frame]:
                self.change(led)

            # loops frames
            if len(self.__every_state)-1 != self.__current_frame:
                self.__current_frame += 1

                # info for user to see which frame is on currently
                self.__infotext.configure(
                    text=f"Frame: {self.__current_frame}",
                    fg="black")

            else:
                # info for user to see which frame is on currently
                self.__infotext.configure(
                    text=f"Frame: {self.__current_frame+1}",
                    fg="black")
                self.__current_frame = 0

        # if there are no saved frames, insue ERROR
        except IndexError:
            self.__infotext.configure(text="ERROR\n"
                                           "You must input at least ONE frame!",
                                      fg="red")

    def start(self):
        """
        starts the main window
        :return:
        """
        self.__root.mainloop()


def main():
    kayttaliittyma = Ledivilkutin()
    kayttaliittyma.start()


if __name__ == "__main__":
    main()
