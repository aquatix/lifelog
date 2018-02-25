# -*- coding: utf-8 -*-

class Cogitorama:
    PREFIX = 'cogitorama:'

    cogitoramas = {}


    @staticmethod
    def get_term(term):
        if not term:
            return None
        #
        sign = '+'
        return (term, sign)

    def add_day(self, date, cogitorama):
        self.cogitoramas[date] = cogitorama


    def get_cogitoramas(self):
        result = {}
        for day in self.cogitoramas:
            for term in self.cogitoramas[day].split(' '):
                print(term)
                if not term:
                    continue
                if not term in result:
                    result[term[1:]] = 0
                if term[0] == '+':
                    result[term[1:]] += 1
                elif term[0] == '-':
                    result[term[1:]] -= 1
                else:
                    print('Error processing cogitorama term "{}"'.format(term))
        return result


if __name__ == "__main__":
    # TODO: create tests
    pass
