import curses
from time import gmtime, strftime, sleep
import curses.textpad
from curses import wrapper
class Client():

    def __init__(self):
        self.history = []

    def timestamp(self):
        return strftime("%H:%M:%S", gmtime())

    def main(self):
        while True:
            try:
                data = self.win_input()
            except KeyboardInterrupt:
                break
            if not data:
                break
            sleep(0.05) #чтоб нормально отрисовалось
            self.win_print(data)
    def win_input(self):
        win = self.input_win
        win.clear()
        win.box()
        result = ""
        c = "ey"
        x, y = 2, 2
        while True:
            if y > self.io_width + 1:
                y = 2
                x += 1
            if x >= self.i_height:
                break
            try:
                c = win.getch(x,y)
            except KeyboardInterrupt:
                return
            if c == curses.KEY_ENTER or c == 10 or c == 13:
                if result:
                    break
                else:
                    return "\n"
            if c == 27:
                raise KeyboardInterrupt
            if c == curses.KEY_BACKSPACE or c == 127:
                c = 10
                if len(result) > 0:
                    result = result[ : -1]
                    y -= 1
                    if y < 2:
                        x, y =2, self.io_width + 1
                    win.addstr(x,y,' ')
                    win.refresh()
            else:
                c = chr(c)
                win.addstr(x,y,c)
                result += c
                y += 1
        return result

    def win_print(self, data, msgqueue = None):
        if not data or data == '\n':
            return
        if msgqueue is None:
            msgqueue = self.history
        data = self.timestamp() + " >> " + data
        
        while len(data) >= self.io_width:
            msgqueue.append(data[ : self.io_width ])
            data = data[self.io_width : ]
        msgqueue.append(data)
        if len(self.history) > 2 * self.o_height:
            last_history = msgqueue[self.o_height : ]
        else:
            last_history = msgqueue.copy()
        last_history.reverse()
        win = self.output_win
        win.clear()
        win.box()
        out_x_limit = 1
        out_x = self.o_height - 1
        for message in last_history:
            if out_x < out_x_limit:
                break
            win.addstr(out_x, 2, message)
            out_x -= 1
        win.refresh()



    def __call__(self, stdscr):
        self.stdscr = stdscr
        self.wins = []

        #_onliners_win
        onl_win_header = "   Online:   "
        onl_win_begin_x = 0
        onl_win_begin_y = 0
        onl_win_height = curses.LINES
        onl_win_width = len(onl_win_header)

        #_output_win
        o_win_header = "Output field"
        o_win_begin_x = onl_win_width
        o_win_begin_y = 0
        o_win_height = curses.LINES - 7
        o_win_width = curses.COLS - onl_win_width

        #_input_win
        i_win_begin_y = o_win_height
        i_win_begin_x = onl_win_width
        i_win_height = curses.LINES - i_win_begin_y
        i_win_width = o_win_width

        #_general_consts
        self.io_width = i_win_width - 4
        self.i_height = i_win_height - 1
        self.o_height = o_win_height - 1 

        self.input_win = curses.newwin(i_win_height, i_win_width, i_win_begin_y, i_win_begin_x)
        self.input_win.box()
        self.wins.append(self.input_win)
        self.output_win = curses.newwin(o_win_height, o_win_width, o_win_begin_y, o_win_begin_x)
        self.output_win.box()
        self.wins.append(self.output_win)
        self.onliners_win = curses.newwin(onl_win_height, onl_win_width, onl_win_begin_y, onl_win_begin_x)
        self.onliners_win.box()
        self.wins.append(self.onliners_win)

        self.refresh_all()
        self.main()
    def refresh_all(self):
        self.stdscr.refresh()
        for win in self.wins:
            win.refresh()
if __name__ == "__main__":
    c = Client()
    wrapper(c)
