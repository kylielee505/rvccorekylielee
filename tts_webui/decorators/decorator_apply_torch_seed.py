from tts_webui.magnet.utils import Seed


def decorator_apply_torch_seed(fn):
    def wrapper(*args, **kwargs):
        with Seed(int(kwargs.get("seed", -1))):
            return fn(*args, **kwargs)

    return wrapper