import curses
from time import gmtime, strftime, sleep
class ClientGUI():
    def __init__(self):
        self.history = []

    def __timestamp(self):
        return strftime("%H:%M:%S", gmtime())

    def getch(self):
        self.stdscr.getch()

    def g_onliners(self, onl_list):
        win = self.onliners_win
        win.clear()
        win.box()
        win.addstr(1,1,self.onl_win_header)
        out_x_limit = curses.LINES - 1
        x = 2
        for onl in onl_list:
            try:
                win.addstr(x, 2, str(onl))
                x += 1
                if x > out_x_limit:
                    break
            except Exception:
                pass
        win.refresh()
    
    def g_input_clear(self):
        win = self.input_win
        win.clear()
        win.box()

    def g_input(self, message=None, color_num = 2):
        if message:
            self.g_print(message, color_num)
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
                win.clear()
                win.box()
                return None
            if c == curses.KEY_ENTER or c == 10 or c == 13:
                if result:
                    break
                else:
                    win.clear()
                    win.box()
                    return None
            if c == 27:
                pass
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
        win.clear()
        win.box()
        return result

    def g_print(self, data, color_num=2):
        if data == '\n' or data is None or data == "":
            return
        data = str(data)

        data = self.__timestamp() + " >> " + data

        while len(data) >= self.io_width:
            self.history.append((data[:self.io_width ], color_num))
            data = data[self.io_width:]
        self.history.append((data, color_num))
        if len(self.history) > 2 * self.o_height:
            last_history = self.history[self.o_height:]
        else:
            last_history = self.history.copy()
        last_history.reverse()

        win = self.output_win
        win.clear()
        win.box()
        out_x_limit = 1
        out_x = self.o_height - 1
        for message in last_history:
            if out_x < out_x_limit:
                break
            win.addstr(out_x, 2, message[0], curses.color_pair(message[1]))
            out_x -= 1
        win.refresh()

    def refresh_all(self):
        self.stdscr.refresh()
        for win in self.wins:
            win.refresh()

    def _set_scr_properties(self):
        self.wins = []

        #_onliners_win
        self.onl_win_header = "  Online:  "
        onl_win_begin_x = 0
        onl_win_begin_y = 0
        onl_win_height = curses.LINES
        onl_win_width = len(self.onl_win_header) + 2

        #_output_win
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
        self.input_win.bkgd(curses.color_pair(2))
        self.input_win.box()
        self.wins.append(self.input_win)
        self.output_win = curses.newwin(o_win_height, o_win_width, o_win_begin_y, o_win_begin_x)
        self.output_win.bkgd(curses.color_pair(2))
        self.output_win.box()
        self.wins.append(self.output_win)
        self.onliners_win = curses.newwin(onl_win_height, onl_win_width, onl_win_begin_y, onl_win_begin_x)
        self.onliners_win.bkgd(curses.color_pair(2))
        self.onliners_win.box()
        self.onliners_win.addstr(1,1, self.onl_win_header)
        self.wins.append(self.onliners_win)

        self.refresh_all()

    def init_gui(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(1)
        curses.start_color()
        #DEBUG text
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        #INFO text; defaut
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        #SYSTEM text
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        #ERROR text
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        #CRITICAL text
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_RED)

        self.stdscr.bkgd(curses.color_pair(2))
        self._set_scr_properties()

    def del_gui(self):
        """
        Deletes GUI and returns to basic console screen
        """
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()
