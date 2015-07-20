import os, time, datetime

def dict2tuple(d):
    return tuple(sorted(d.items()))

def touch(fname, times=None):
    with open(fname, 'a'):
            os.utime(fname, times)

def to_timestamp(dt):
    return int(dt.strftime("%s"))

def unallocated_task(file_name):
    if not os.path.exists(file_name + '.todo'):
        return False
    if os.path.exists(file_name + '.finished'):
        return False
    if os.path.exists(file_name + '.failed'):
        return False
    if not os.path.exists(file_name + '.alive'):
        return True

    if to_timestamp(datetime.datetime.now()) - os.path.getmtime(file_name + '.alive') > 10:
        # Heartbeat timeout
        return True
    else:
        return False

def finished(file_name):
    return os.path.exists(file_name + '.finished')

def failed(file_name):
    return os.path.exists(file_name + '.failed')

def heartbeat(file_name):
    touch(file_name + '.alive')

def dead(file_name):
    if not os.path.exists(file_name + '.alive'):
        return False

    if os.path.exists(file_name + '.finished'):
        return False

    touch('current')
    if os.path.getmtime('current') - os.path.getmtime(file_name + '.alive') > 10:
        # Heartbeat timeout
        return True
    else:
        return False

def finish(file_name):
    touch(file_name + '.finished')

def fail(file_name):
    touch(file_name + '.fail')

def allfinish():
    touch('allfinished')

def allfinished():
    return os.path.exists('allfinished')
