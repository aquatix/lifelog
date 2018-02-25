"""
lifelog.py
Build a HTML representation of your logbook, enriched with data from various sources
"""
import os
import sys

import click
import yaml

# Export plugins
from plugins import paragoo, pelican, sleepasandroid
from plugins.cogitorama import Cogitorama

try:
    if os.environ['BETTER_EXCEPTIONS']:
        import better_exceptions
except KeyError:
    pass


def string_to_date(datestring):
    from datetime import date
    datestring = str(datestring).replace('-', '')
    if len(datestring) == 6:
        datestring = datestring + '01'
    return date(int(datestring[0:4]), int(datestring[4:6]), int(datestring[6:8]))


def get_dates_in_range(startdate, enddate):
    """ Return list of dates in iso8601 format: yyyymmdd """
    """ returns: list of Date objects """
    from datetime import date, timedelta as td

    result = []
    d1 = string_to_date(startdate)
    d2 = string_to_date(enddate)

    delta = d2 - d1

    for i in range(delta.days + 1):
        result.append(d1 + td(days=i))

    return result


def get_months_in_range(startdate, enddate):
    """ Return list of months in iso8601 format: yyyymm """
    from datetime import date, timedelta as td

    result = []
    startmonth = [int(str(startdate)[0:4]), int(str(startdate)[4:6])]
    endmonth = [int(str(enddate)[0:4]), int(str(enddate)[4:6])]

    this_year = startmonth[0]
    this_month = startmonth[1]

    while this_year < endmonth[0] or (this_year == endmonth[0] and this_month <= endmonth[1]):
        result.append('{}{num:02d}'.format(this_year, num=this_month))
        this_month += 1
        if this_month == 13:
            this_month = 1
            this_year += 1

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


def process_month(config, textdata, censor=False, cogitorama=None):
    days = get_entries_per_day(textdata)
    # Extra text to highlight, when starting a line:
    highlights = config['highlight']
    # If in non-private mode, filter lines starting with:
    filters = config['filter']

    newdays = {}
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
            if cogitorama and line[0:len(cogitorama.PREFIX)].lower() == cogitorama.PREFIX:
                print(line)
                cogitorama.add_day(day, line[len(cogitorama.PREFIX):])
        newdays[day] = '\n'.join(newdaylines)

    # TODO: process time tags, 'med', 'priv' tags and such
    # TODO: parse activity data, sleep data and such
    return newdays


def process_archive(config, path, destination, plugins, censor=False):
    print(config)
    file_postfix = '.md'
    if config['postfix']:
        file_postfix = '{}{}'.format(config['postfix'], '.md')

    try:
        if plugins['sleepasandroid']:
            sleepdataitems = sleepasandroid.read(plugins['sleepasandroid'])
    except KeyError:
        pass

    cogitorama = Cogitorama()

    dates = get_dates_in_range('{}01'.format(config['startdate']), '20160920')
    filenames = [config['startdate'], '201609']
    filenames = get_months_in_range(config['startdate'], '201802')
    print(filenames)
    #sys.exit()
    for filename in filenames:
        try_filename = os.path.join(path, '{}{}'.format(filename, file_postfix))
        try:
            print('processing ' + try_filename)
            with open(try_filename, encoding='latin-1') as pf:
                textdata = pf.read()
        except IOError:
            # File not found, return None
            print(try_filename + ' not found')
            continue
        # activitydata = parse_google_fit_checkout()
        this_month = process_month(config, textdata, censor=censor, cogitorama=cogitorama)
        destination_path = os.path.join(destination, str(filename) + '.md')
        #print('{}/{}.md'.format(destination, filename))
        print(destination_path)

        # Continue for now, as this_month is a dict with days
        continue
        try:
            with open(destination_path, 'w') as df:
                df.write(this_month)
        except IOError:
            print(destination_path + ' not writable')

    print(cogitorama.print_stats())


## Main program
@click.group()
def cli():
    """
    Lifelog logbook parser
    """
    pass


@cli.command()
@click.option('-p', '--path', prompt='Logbook path', type=click.Path(exists=True))
@click.option('-d', '--destination', prompt='Destination path', type=click.Path(exists=True))
@click.option('-s', '--sleepdata', default=None, type=click.Path(exists=True))
@click.option('--censor/--normal', default=False)
@click.option('--sitetype', type=click.Choice(['paragoo', 'pelican']), default='pelican')
def build_logbook(path, destination, sleepdata, censor, sitetype):
    """
    Parse logbook markdown files, build html. Enrich with external sources, images
    """
    click.secho('Needs implementing', fg='red')
    click.echo(sitetype)

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
    if sitetype == 'paragoo':
        paragoo.createproject(destination)
    elif sitetype == 'pelican':
        pelican.createproject(destination)


if __name__ == '__main__':
    """
    Lifelog is being run standalone
    """
    cli()
