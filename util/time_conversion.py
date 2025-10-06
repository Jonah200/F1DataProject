import math

def secs_to_mins(seconds: float):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)

    formatted = f"{minutes:02d}:{secs:02d}:{millis:03d}"
    return formatted


def convert_time(seconds: float):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60

    if seconds == 0:
        return '-'

    if hours > 0:
        # h:mm:ss.mmm
        return f"{hours}:{minutes:02d}:{secs:06.3f}"
    elif minutes > 0:
        # m:ss.mmm
        return f"{minutes}:{secs:06.3f}"
    else:
        # just seconds.mmm
        return f"{secs:.3f}"