# python-template
A template repository for Python 3 projects.

This template provides a logger, as well as set-up and start scripts.

## Usage
1. Follow [this guide](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template#creating-a-repository-from-a-template) to create a repository from this template.
2. Clone your repository, and `cd` to it
3. If your repository requires external dependencies:
    - Run `python -m venv venv` to create a `venv` folder for local dependencies
    - Use `venv/scripts/activate` to start using the virtual environment
    - Use `pip` to install the desired dependencies
    - Use `pip freeze > requirements.txt` to export the list of depencencies
4. (Bash-only) Instruct users to use `setup.sh` to set up their virtual environment in your `README.md`
5. Instruct users to use `start.bat`/`start.sh` to run the program in your `README.md`
6. Test run `main.py` using `start.bat`/`start.sh`
7. Refer to the example in `main.py` to see how to import, instantiate, and use the logger
    - Log files are saved to `/logs` and rotated at midnight.
    - Log files are automatically excluded from git