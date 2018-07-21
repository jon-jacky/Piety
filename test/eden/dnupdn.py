# dnupdn.py - Just run cursor down, then up, then down with ^N and ^P
import eden, ed, samysh
from keyboard import * # ^N ^P keycodes, and all the others

keycodes = 3*C_n + 6*C_p +3*C_n  # just a string, all keycodes are single chars

# define a function so we can call it many times
def main():
    ed.E('lines20.txt')
    ed.l(10)
    eden.base_do_command('C')
    samysh.run_script('0 1', keycodes, eden.eden.handle_key)

# so we don't have to call main after initial import
main()
