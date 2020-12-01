# 更新pip全部依赖包
from pip._internal.utils.misc import get_installed_distributions
from subprocess import call

for dist in get_installed_distributions():
    call("pip install --upgrade " + dist.project_name, shell=True)