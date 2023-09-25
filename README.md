# Task Tracker

> A CLI Application to track the time on specific tasks

## Features

- [x] Adding reports
  - time is calculated automatically
  - when clicking `CTRL+C` the time is stopped

- [x] display a report for a specific day


## Installation

    python3 -m venv .env
    source .env/bin/activate
    pip install -r requirements.txt

## Usage

### Adding reports

    python main.py /path/to/a/directory/where/the/data/will/be/saved

### Generate reports for a specific day

    python mian.py /path/to/reports --reporting 15.10.2023