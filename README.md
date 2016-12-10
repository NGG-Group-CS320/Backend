# MF-DAT Backend
Backend code and configuration for MF-DAT

Open TODO.md for a list of tasks

## Setup

Be sure you are running a copy of Ubuntu Linux for consistency when developing.
 1. Clone this repository. You can just run `git clone https://github.com/NGG-Group-CS320/Backend.git` in terminal.
 2. Copy the `config.py` file from the shared Google Drive directory into the `Backend/src/` directory.
 3. Run the following commands to install the necessary dependencies.

```
# Install psycopg2 python package so queries can be made to postgres DB
sudo apt-get install python3-psycopg2

# Install numpy python package for data manipulation
sudo apt-get install python3-numpy
```

## Running

Run `python3 src/health_score.py` in the terminal to run the script to compute health scores.
