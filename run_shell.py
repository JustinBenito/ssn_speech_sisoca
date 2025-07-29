import subprocess
import shlex

env_path = "/home/sltlab/espnet/tools/activate_python.sh"

# Run each command separately
subprocess.run(f"source {env_path}", shell=True, cwd="/home/sltlab/espnet/tools", executable="/bin/bash", check=True)
subprocess.run("source cmd.sh", shell=True, executable="/bin/bash", check=True)
subprocess.run("source path_try.sh", shell=True, executable="/bin/bash", check=True)
subprocess.run(shlex.split("./main_run.sh home/sltlab/vsa/TDSC/moderate/FBL/audio/FBL3.wav"), shell=True, executable="/bin/bash", check=True, cwd="/home/sltlab/kaldi/egs/SISOCADEMO")