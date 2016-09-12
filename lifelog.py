"""
lifelog.py
Build a HTML representation of your logbook, enriched with data from various sources
"""
import os
import click
import jinja2
import markdown
import yaml
from utilkit import fileutil, datetimeutil


def get_entries_per_day(content):
    """
    Split logbook month content into dict with entries per day
    """
    entries = content.split('## ')
    days = {}
    for entry in entries:
        entry_parts = entry.split('\n')
        if entry_parts[0]:
            date = entry_parts[0].split(' ')[0]
            print date
            entry_parts[0] = '## {}'.format(entry_parts[0])
            days[date] = {'title': entry_parts[0], 'body': '\n'.join(entry_parts[1:])}
    print days
    return days


## Main program
@click.group()
def cli():
    """
    Lifelog logbook parser
    """
    pass


@cli.command()
@click.option('-p', '--path', prompt='Logbook path')
@click.option('-d', '--destination', prompt='Destination path')
def build_logbook(path, destination):
    """
    Parse logbook markdown files, build html. Enrich with external sources, images
    """
    click.secho('Needs implementing', fg='red')

    try:
        f = open(os.path.join(path, 'lifelog.yaml'))
        config = yaml.load(f)
        f.close()
    except IOError as e:
        print e
        sys.exit(1)

    print config
    file_postfix = '.md'
    if config['postfix']:
        file_postfix = '{}{}'.format(config['postfix'], '.md')

    filenames = [config['startdate'], '201609']
    for filename in filenames:
        try_filename = os.path.join(path, '{}{}'.format(filename, file_postfix))
        data = fileutil.get_file_contents(try_filename)
        if not data:
            print(try_filename + ' not found')
        days = get_entries_per_day(data)


if __name__ == '__main__':
    """
    Paragoo is ran standalone
    """
    cli()