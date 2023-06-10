python -m venv .venv
. .venv/bin/activate
pip install -r requirements_cuda.txt
pip install -r requirements.txt
mkdir -p model
mkdir -p input
mkdir -p output

user=$(id -un)
group=$(id -gn)
script_path=$(dirname "$(readlink -f "$0")")

exec 3<> sd-gen.service
    echo "[Unit]" >&3
    echo "Description = Stable Difussion Generation Service" >&3
    echo "After = network.target" >&3 
    echo "" >&3
    echo "[Service]" >&3
    echo "Type = simple" >&3
    echo "ExecStart = $script_path/.venv/bin/python $script_path/index.py" >&3
    echo "User = $user" >&3
    echo "Group = $group" >&3
    echo "Restart = on-failure " >&3
    echo "SyslogIdentifier = sd-gen.log" >&3
    echo "RestartSec = 5" >&3
    echo "TimeoutStartSec = infinity" >&3
    echo "" >&3
    echo "[Install]" >&3
    echo "WantedBy = multi-user.target" >&3
exec 3>&-
    