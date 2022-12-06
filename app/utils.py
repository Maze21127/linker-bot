import re


def get_correct_transfer_string(data_size):
    KB = 1024
    MB = 1024**2
    GB = 1024**3

    if data_size / GB > 1:
        return f"{round(data_size / GB, 2)} GB"
    elif data_size / MB > 1:
        return f"{round(data_size / MB, 2)} MB"
    elif data_size / KB > 1:
        return f"{round(data_size / KB, 2)} KB"
    return f"{data_size} B"


def remove_port_from_ip(ip: str):
    remove_port_regex = r"\d+.\d+.\d+.\d+"
    try:
        return re.match(remove_port_regex, ip).group(0)
    except AttributeError:
        return ""
    return ""
