"""
Can we read from stdin in python unikernel? - simplified excerpt from pysh.ph
"""

def main():
    print("echo, type any string, q to exit")
    command = ''
    while command != 'q':
        command = input('>> ')
        print(command)

if __name__ == '__main__':
    main()
