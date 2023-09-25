import datetime
import json
import tempfile
from time import sleep

import click
from rich.console import Console
from rich.markdown import Markdown
import os
from subprocess import call

from rich.table import Table

console = Console()


def print_markdown(data: str) -> None:
    console.print(Markdown(data))


def format_time_elapsed(start: datetime, end: datetime) -> str:
    duration = (end - start).total_seconds()
    seconds = duration % 60
    minutes = (duration - seconds) / 60
    return f'{minutes:.0f}:{seconds:02.0f}'


@click.command()
@click.argument('tasks_dir', type=click.Path(dir_okay=True, file_okay=False))
@click.option('--reporting', type=click.DateTime(formats=['%d.%m.%Y']))
def main(tasks_dir: str, reporting: datetime.datetime):
    print_markdown('# Task Tracker')
    if reporting is not None:
        show_report(reporting, tasks_dir)
    else:
        track_time(tasks_dir)


def track_time(tasks_dir):
    if not os.path.exists(tasks_dir):
        os.mkdir(tasks_dir)
    print_markdown('> Available Projects')
    [print_markdown(f'- {file}') for file in os.listdir(tasks_dir)]
    project_name = input('Project Name: ')
    project_path = os.path.join(tasks_dir, project_name)
    if not os.path.exists(project_path):
        os.mkdir(project_path)
    print_markdown('> Available Tasks')
    [print_markdown(f'- {file}') for file in os.listdir(project_path)]
    task_name = input('Task Name: ')
    task_path = os.path.join(tasks_dir, project_name, f'{task_name}.json')
    start = datetime.datetime.now()
    time_displayed = ''
    try:
        print_markdown(f'> Task: `{task_name}` for Project {project_name} started')
        while True:
            end = datetime.datetime.now()
            time_displayed = format_time_elapsed(start, end)
            print(time_displayed, end='', flush=True)
            sleep(10)
            for i in range(len(time_displayed)):
                print('\b', end='', flush=True)
    except:
        print('\b\b', end='', flush=True)
        pass
    for i in range(len(time_displayed)):
        print('\b', end='', flush=True)
    end = datetime.datetime.now()
    time_displayed = format_time_elapsed(start, end)
    print(time_displayed)
    description = ''
    with tempfile.NamedTemporaryFile(suffix='.md') as temp:
        temp.write(''.encode('utf-8'))
        temp.flush()
        call(['vim', temp.name])
        temp.seek(0)
        description = temp.read().decode('utf-8')
    task_report_data = {
        'date': start.isoformat(),
        'duration': time_displayed[:-3],
        'description': description
    }
    task_reports = []
    if os.path.exists(task_path):
        with open(task_path) as f:
            task_reports = json.loads(f.read().encode('utf-8'))
    task_reports.append(task_report_data)
    with open(task_path, 'w') as f:
        f.write(json.dumps(task_reports))
    print_markdown(f'> Task: `{task_name}` for Project {project_name} saved')


def show_report(reporting, tasks_dir):
    table = Table(title=f'Report for {reporting.date()}', expand=True, show_lines=True)
    table.add_column('Task')
    table.add_column('Description')
    table.add_column('Duration (hours)', justify="right", width=1)
    total_hours = 0
    for project in os.listdir(tasks_dir):
        for task in os.listdir(os.path.join(tasks_dir, project)):
            with open(os.path.join(tasks_dir, project, task)) as f:
                result = filter(
                    lambda reported_task: datetime.datetime.fromisoformat(
                        reported_task['date']).date() == reporting.date(),
                    json.loads(f.read().encode('utf-8'))
                )
                for reported_task in result:
                    hours = int(reported_task['duration']) / 60
                    total_hours += hours
                    table.add_row(task[:-5], reported_task['description'], f'{hours:.2f}')
    table.add_row('', '', f'[bold green]{total_hours:.2f}')
    console.print(table)


if __name__ == '__main__':
    main()
