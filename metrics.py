import psutil


def get_cpu_usage():
    '''
    Returns CPU usage as user, system and idle time as values between 0-1.
    Total sum of user+system+idle is always 1

    :return: dictionary containing user, system and idle as keys
    '''
    times = psutil.cpu_times()
    total = times.idle + times.system + times.user
    return {
        "user": times.user/total,
        "system": times.system/total,
        "idle": times.idle/total
    }
