import sys
import os
import subprocess

try:
    import rez
except ImportError:
    sys.stdin = open(os.devnull, "r")
    if sys.platform != "win32":
        cmd = "printenv PWD"
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        result, err = process.communicate()
        print(f"RESULT: {result}")
        print(f"ERR: {err}")
    python_version = f"{sys.version_info[0]}.{sys.version_info[1]}"
    if sys.platform == "win32":
        rez_cmd = f"rez-env rez python-{python_version} .dcc-shotgun -- echo %REZ_REZ_ROOT%"
    else:
        rez_cmd = f"rez-env rez python-{python_version} .dcc-shotgun -- printenv REZ_REZ_ROOT"

    process = subprocess.Popen(
        rez_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    rez_path, err = process.communicate()

    if err or not rez_path:
        raise Exception(err)
        # raise ImportError(
        # "Failed to find Rez as a package in the current environment! "
        # "Try 'rez-bind rez'!"
        # )

    else:
        rez_path = rez_path.decode(encoding="utf-8", errors="ignore").strip()
        if os.path.exists(os.path.join(rez_path, "python")):
            rez_path = os.path.join(rez_path, "python")
        if rez_path not in sys.path:
            sys.path.append(rez_path)
        if "SGTK_DESKTOP_ORIGINAL_PYTHONPATH" in os.environ:
            ";".join([os.environ["SGTK_DESKTOP_ORIGINAL_PYTHONPATH"], rez_path])
        elif "PYTHONPATH" in os.environ:
            ";".join([os.environ["PYTHONPATH"], rez_path])
        else:
            os.environ["PYTHONPATH"] = rez_path


def combine_in_sys_path(package_list):
    from rez.resolved_context import ResolvedContext

    context = ResolvedContext(package_list, caching=False)
    for path in context.get_environ().get("PYTHONPATH", "").split(";"):
        if path not in sys.path:
            sys.path.append(path)
