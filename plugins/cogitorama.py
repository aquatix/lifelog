# -*- coding: utf-8 -*-

class Cogitorama:
    PREFIX = 'cogitorama:'

    cogitoramas = {}


    @staticmethod
    def get_term(term):
        if not term:
            return None, None
        sign = term[0]
        term = term[1:]
        if sign == '+' or sign == '-':
            return (term, sign)
        return None, None

    def add_day(self, date, cogitorama):
        self.cogitoramas[date] = cogitorama


    def get_cogitoramas(self):
        result = {}
        for day in self.cogitoramas:
            for term in self.cogitoramas[day].split(' '):
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
                    print('Error processing cogitorama term "{}"'.format(term))
        return result


if __name__ == "__main__":
    # TODO: create tests
    pass
