import csv

from dateutil.parser import parse


def naturaldatetime_to_datetimestamp(timestamp):
    """Convert '24 Aug 2018 15:02' to datetime object"""
    return parse(timestamp)


def lastfm_stats(filename):
    artists_per_day = {}
    artists_per_month = {}
    current_date = ''
    current_month = ''
    with open(filename) as csvfile:
        statsreader = csv.reader(csvfile, delimiter=',')
        for row in statsreader:
            track_datetime = naturaldatetime_to_datetimestamp(row[3])
            track_date = track_datetime.strftime('%Y%m%d')
            track_month = track_datetime.strftime('%Y%m')

            if current_date != track_date:
                # Add date to the dict
                artists_per_day[track_date] = {}
                current_date = track_date
            if row[0] not in artists_per_day[track_date]:
                # First time we see this artist today
                artists_per_day[track_date][row[0]] = 1
            else:
                artists_per_day[track_date][row[0]] += 1

            if current_month != track_month:
                # Add date to the dict
                artists_per_month[track_month] = {}
                current_month = track_month
            if row[0] not in artists_per_month[track_month]:
                # First time we see this artist today
                artists_per_month[track_month][row[0]] = 1
            else:
                artists_per_month[track_month][row[0]] += 1
    return artists_per_day, artists_per_month


if __name__ == "__main__":
    per_day, per_month = lastfm_stats('lastfm.csv')
    print(per_day)
    print('-----------------------------------------------------')
    print(per_month)
