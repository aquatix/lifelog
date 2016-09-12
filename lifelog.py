"""
lifelog.py
Build a HTML representation of your logbook, enriched with data from various sources
"""
import click
import jinja2
import yaml


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


if __name__ == '__main__':
    """
    Paragoo is ran standalone
    """
    cli()
