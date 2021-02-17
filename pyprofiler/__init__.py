import flameprof
import cProfile
import pstats
from functools import wraps


def pyprofiler(
    output_file=None, sort_by="time", lines_to_print=None, strip_dirs=True, flame_file=None
):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _output_file = output_file or func.__name__ + ".prof"
            pr = cProfile.Profile()
            pr.enable()
            retval = func(*args, **kwargs)
            pr.disable()
            pr.dump_stats(_output_file)
            if flame_file:
                s = pstats.Stats(_output_file)
                with open(flame_file, "w") as f:
                    flameprof.render(s.stats, f, "svg")
            with open(_output_file, "w") as f:
                ps = pstats.Stats(pr, stream=f)
                if strip_dirs:
                    ps.strip_dirs()
                if isinstance(sort_by, (tuple, list)):
                    ps.sort_stats(*sort_by)
                else:
                    ps.sort_stats(sort_by)
                ps.print_stats(lines_to_print)
            return retval

        return wrapper

    return inner
