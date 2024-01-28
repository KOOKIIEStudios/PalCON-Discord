#!/bin/bash
# This script starts the Python program
# @author KOOKIIE

echo "This script will launch the program."
PS3="Please select the environment to run the source code with: "
run_options=("Virtual Python Environment (recommended)" "Global Python Environment" "Quit")
select opt in "${run_options[@]}"
do
    case $opt in
        "${run_options[0]}")
            echo "[INFO] You have selected:  $REPLY) $opt"
            source "$PWD"/venv/bin/activate
            python3 main.py
            break
            ;;
        "${run_options[1]}")
            echo "[INFO] You have selected:  $REPLY) $opt"
            python3 main.py
            break
            ;;
        "${run_options[2]}")
            echo "[INFO] Now terminating..."
            exit 1
            break
            ;;
        *) echo "[INFO] invalid option $REPLY - try again!";continue;;
    esac
done

$SHELL