import time

def tstamp():
    return time.strftime('%Y%m%dT%H%M%S')
    
def str_time():
    return time.strftime('%Y-%m-%dT%H:%M:%S')

def print_message(level, cmd, str):
    cmd_box = '[{0}]'.format(cmd)
    print "%-23s %-20s %-43s %s" % (cmd_box,str_time(),level,str)

def message(cmd, str):
    print_message('INFO', cmd, str)

def warning(cmd, str):
    print_message('WARNING', cmd, str)

def error_no_exit(cmd, str):
    print_message('ERROR', cmd, str)
