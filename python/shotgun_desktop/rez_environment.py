import sys
import os
import subprocess

try:
    import rez
except ImportError:
    sys.stdin = open(os.devnull, "r")

    if sys.platform == "win32":
        rez_cmd = 'rez-env rez -- echo %REZ_REZ_ROOT%'
    else:
        rez_cmd = 'rez-env rez -- printenv REZ_REZ_ROOT'

    process = subprocess.Popen(rez_cmd, stdout=subprocess.PIPE, shell=True)
    rez_path, err = process.communicate()

    if err or not rez_path:
        raise ImportError(
            "Failed to find Rez as a package in the current environment! "
            "Try 'rez-bind rez'!"
        )

    else:
        rez_path = rez_path.decode(encoding="utf-8", errors="ignore").strip()
        rez_python = os.path.join(rez_path, "python")
        if rez_python not in sys.path:
            sys.path.append(rez_python)


def resolve_rez_environment(package_list):
    from rez.resolved_context import ResolvedContext
    context = ResolvedContext(package_list, caching=False)
    context.apply()


def combine_in_sys_path(package_list):
    from rez.resolved_context import ResolvedContext
    context = ResolvedContext(package_list, caching=False)
    for path in context.get_environ().get("PYTHONPATH", "").split(";"):
        if path not in sys.path:
            sys.path.append(path)

def combine_environments(package_list, parent_variables):
    from rez.resolved_context import ResolvedContext
    from rez.config import config
    current_path = sys.path
    config.parent_variables = parent_variables
    resolve_rez_environment(package_list)
    sys.path.extend(current_path)
