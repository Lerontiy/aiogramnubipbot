import asyncio
from stuff.settings import EQUAL_SUBJECTS

def in_both_str(*strs, string:str="None", excepting_string:str="None"):
    for el in strs:
        if ((string=="None") or (string in el)) and ((excepting_string=="None") or (excepting_string not in el)):
            continue
        else:
            return False
    return True


def equal_strings_in_something(main_string:str, something):
    if main_string in EQUAL_SUBJECTS:
        for el in EQUAL_SUBJECTS[main_string]:
            if (el in something):
                return True
            else:
                continue
    return False


async def every(__seconds: float, func, *args, **kwargs):
    while True:
        func(*args, **kwargs)
        await asyncio.sleep(__seconds)