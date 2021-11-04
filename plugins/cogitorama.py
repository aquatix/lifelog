# -*- coding: utf-8 -*-

class Cogitorama:
    PREFIX = 'cogitorama:'

    cogitoramas = {}

    @staticmethod
    def get_term(term):
        """
        Parse a cogitorama term and return the keyword with its sign

        :param str term:
        :return: Tuple with (term, sign)
        :rtype: tuple
        """
        if not term:
            return None, None
        sign = term[0]
        term = term[1:]
        if sign in ('+', '-'):
            return (term, sign)
        return None, None

    def add_day(self, date, cogitorama):
        self.cogitoramas[date] = cogitorama

    def get_cogitoramas(self):
        """
        Return dictionary with all terms and the amount of times they occur in the logbook

        :return: dictionary with all terms and the amount of times they occur in the logbook
        :rtype: dict
        """
        result = {}
        for day_cogitorama in self.cogitoramas.items():
            for term in day_cogitorama[1].split(' '):
                term, sign = self.get_term(term)
                if not term:
                    continue
                if not term in result:
                    result[term] = 0
                if sign == '+':
                    result[term] += 1
                elif sign == '-':
                    result[term] -= 1
                else:
                    print(f"Error processing cogitorama term \"{term}\"")
        return result

    def print_stats(self):
        """
        Print the list of cogitoramas with the amount of times they were encountered in the logbook
        """
        cogs = self.get_cogitoramas()
        for key in sorted(cogs):
            print('{:3} {}'.format(cogs[key], key))


if __name__ == "__main__":
    # TODO: create tests
    pass
