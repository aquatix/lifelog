
def listenbrainz_stats(filename):
    """Artists statistics.

    :param str filename: input CSV with LastFM stats
    :return: artists per day and per month
    :rtype: list, list
    """
    raise NotImplementedError('ListenBrainz is not implemented yet')


def read_file(jsonl_file):

    with open('really_big_file.jsonl', mode='r') as infile:
        for line in infile:
            json_line = loads(line)
            # now do the thing
