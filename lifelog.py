"""
lifelog.py
Build a HTML representation of your logbook, enriched with data from various sources
"""
import os
import sys
import click
import yaml
from utilkit import fileutil, datetimeutil
from plugins import sleepasandroid

def string_to_date(datestring):
    from datetime import date
    datestring = datestring.replace('-', '')
    return date(int(datestring[0:4]), int(datestring[4:6]), int(datestring[6:8]))


def get_dates_in_range(startdate, enddate):
    """ Return list of dates in iso8601 format: yyyymmdd """
    from datetime import date, timedelta as td

    result = []
    d1 = string_to_date(startdate)
    d2 = string_to_date(enddate)

    delta = d2 - d1

    for i in range(delta.days + 1):
        result.append(d1 + td(days=i))

    return result


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
            print(date)
            entry_parts[0] = '## {}'.format(entry_parts[0])
            days[date] = {'title': entry_parts[0], 'body': '\n'.join(entry_parts[1:])}
    #print(days)
    return days


def process_day(config, textdata, censor=False):
    days = get_entries_per_day(textdata)
    # Extra text to highlight, when starting a line:
    highlights = config['highlight']
    # If in non-private mode, filter lines starting with:
    filters = config['filter']

    #print(days)
    for day in days:
        daylines = days[day]['body'].split('\n')
        newdaylines = []
        for line in daylines:
            if censor:
                for privfilter in filters:
                    print('"{}"'.format(line[0:(len(privfilter))]))
                    if line[0:len(privfilter)] == privfilter:
                        print('skipping!')
                        print(line)
                        # Skip this line
                        continue
            for highlight in highlights:
                if line[0:len(highlight)] == highlight:
                    # Add emphasizing, so *'s or _'s
                    line = '_{}_{}'.format(line[0:len(highlight)], line[len(highlight):])
            newdaylines.append(line)
        days[day] = '\n'.join(newdaylines)

    # TODO: process time tags, 'med', 'priv' tags and such
    # TODO: parse activity data, sleep data and such
    return days


def process_archive(config, path, destination, plugins, censor=False):
    print(config)
    file_postfix = '.md'
    if config['postfix']:
        file_postfix = '{}{}'.format(config['postfix'], '.md')

    dates = get_dates_in_range('{}01'.format(config['startdate']), '20160920')
    filenames = [config['startdate'], '201609']
    for filename in filenames:
        try_filename = os.path.join(path, '{}{}'.format(filename, file_postfix))
        textdata = fileutil.get_file_contents(try_filename)
        if not textdata:
            print(try_filename + ' not found')
        # activitydata = parse_google_fit_checkout()
        this_day = process_day(config, textdata)
        print('{}/{}.md'.format(destination, filename))


## Main program
@click.group()
def cli():
    """
    Lifelog logbook parser
    """
    pass


@cli.command()
@click.option('-p', '--path', prompt='Logbook path',type=click.Path(exists=True))
@click.option('-d', '--destination', prompt='Destination path', type=click.Path(exists=True))
@click.option('-s', '--sleepdata', default=None, type=click.Path(exists=True))
@click.option('--censor/--normal', default=False)
def build_logbook(path, destination, sleepdata, censor):
    """
    Parse logbook markdown files, build html. Enrich with external sources, images
    """
    click.secho('Needs implementing', fg='red')

    try:
        f = open(os.path.join(path, 'lifelog.yaml'))
        config = yaml.load(f)
        f.close()
    except IOError as e:
        print(e)
        sys.exit(1)

    plugins = {}
    if sleepdata:
        plugins['sleepasandroid'] = sleepdata

    print(plugins)
    process_archive(config, path, destination, plugins, censor)


if __name__ == '__main__':
    """
    Lifelog is being run standalone
    """
    cli()
