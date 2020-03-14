import subprocess

from django.conf import settings


def hexo_build():
    ret = subprocess.run(
        # ' '.join(settings.CMD_LIST),
        settings.CMD_STR,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        timeout=120
    )
    return ret.stdout + ret.stderr
