"""lifelog.py

Build a HTML representation of your logbook, enriched with data from various sources
"""
import os
import sys
from datetime import date, timedelta

import click
import strictyaml

# Export plugins
from plugins import json_base, paragoo, pelican, sleepasandroid
from plugins.cogitorama import Cogitorama

#  try:
#      if os.environ['BETTER_EXCEPTIONS']:
#          import better_exceptions
#  except KeyError:
#      pass


def string_to_date(datestring):
    datestring = str(datestring).replace('-', '')
    if len(datestring) == 6:
        datestring = datestring + '01'
    return date(int(datestring[0:4]), int(datestring[4:6]), int(datestring[6:8]))


def get_dates_in_range(startdate, enddate):
    """Enumerates all dates from startdate to enddate

    Args:
        startdate: start of the list of dates
        enddate: end of the list of dates, likely today
    Returns:
        a list of Date objects
    """

    result = []
    d1 = string_to_date(startdate)
    d2 = string_to_date(enddate)

    delta = d2 - d1

    for i in range(delta.days + 1):
        result.append(d1 + timedelta(days=i))

    return result


def get_months_in_range(startdate, enddate):
    """Enumerates all months from startdate to enddate

    Args:
        startdate: start of the list of dates
        enddate: end of the list of dates, likely today
    Returns:
        list of months in iso8601 format: yyyymm
    """
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
    """Splits logbook month content into dict with entries per day

    Args:
        content: 'raw' markdown text of a month
    Returns:
        dictionary of days
    """
    entries = content.split('## ')
    days = {}
    for entry in entries:
        entry_parts = entry.split('\n')
        if entry_parts[0]:
            the_date = entry_parts[0].split(' ')[0]
            print(the_date)
            entry_parts[0] = '## {}'.format(entry_parts[0])
            days[the_date] = {'title': entry_parts[0], 'body': '\n'.join(entry_parts[1:])}
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

    posts_destination_dir = os.path.join(destination, 'content/posts')
    #os.makedirs(posts_destination_dir, exists_ok=True)
    if not os.path.isdir(posts_destination_dir):
        os.makedirs(posts_destination_dir)

    try:
        if plugins['sleepasandroid']:
            sleepdataitems = sleepasandroid.read(plugins['sleepasandroid'])
    except KeyError:
        pass

    cogitorama = Cogitorama()

    current_month = date.today().strftime('%Y%m')
    #dates = get_dates_in_range('{}01'.format(config['startdate']), '20160920')
    filenames = get_months_in_range(config['startdate'], current_month)
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
        destination_path = os.path.join(posts_destination_dir, str(filename) + '.md')
        #print('{}/{}.md'.format(destination, filename))
        print(destination_path)

        this_month_content = ''
        # TODO: add pelican post item header
        for the_date in this_month:
            this_month_content += '## {}\n{}'.format(the_date, this_month[the_date])

        # Continue for now, as this_month is a dict with days
        #continue
        try:
            with open(destination_path, 'w') as df:
                df.write(this_month_content)
        except IOError:
            print(destination_path + ' not writable')

    print(cogitorama.print_stats())


## Main program
@click.group()
def cli():
    # Lifelog logbook parser
    pass


@cli.command()
@click.option('-p', '--path', prompt='Logbook path', type=click.Path(exists=True))
@click.option('-d', '--destination', prompt='Destination path', type=click.Path(exists=True))
@click.option('-s', '--sleepdata', default=None, type=click.Path(exists=True))
@click.option('--censor/--normal', default=False)
@click.option('--sitetype', type=click.Choice(['json', 'paragoo', 'pelican']), default='json')
def build_logbook(path, destination, sleepdata, censor, sitetype):
    """Parses logbook markdown files, builds pelican or paragoo files. Enriches with external sources, images

    Args:
        path: path to the source of the logbook
        destination: destination path for generated output
        sleepdata: path to sleepdata files
        censor: Boolean to censor private notes or not
        sitetype: paragoo or pelican output
    Returns:
        nothing
    """
    click.secho('Needs implementing', fg='red')
    click.echo(sitetype)

    try:
        f = open(os.path.join(path, 'lifelog.yaml'))
        config = strictyaml.load(f.read()).data
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
    elif sitetype == 'json':
        json_base.createproject(destination)


if __name__ == '__main__':
    # Lifelog is being run standalone
    cli()
