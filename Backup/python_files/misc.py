
import time
import itertools
import matrix

def remove_previous_lines(n):
    for i in range(n):
        print ("\033[A\033[A")

class progress_bar:

    def __init__(self,name, max_val, width, size_of_extra_info=None):
        self.time = time.time()
        self.name = name
        self.current = 0
        self.percent = 0
        self.max_val = max_val
        self.width   = width
        str_name = str(name)
        length_name = len(name)
        if length_name > width + 2:
            print(name)
        else:
            w = int(width/2 - length_name/2)
            print('-'*w + ' '  + str(name) + ' '+ '-'*w)
        if not size_of_extra_info == None:
                print('\n'*size_of_extra_info)
        else:
            print('')
        self.display()

    def update(self, value):

        ratio = float(value)/self.max_val
        self.percent = 100.0 * ratio
        self.current = int(ratio * self.width)

    def display(self, list_extra_info=None):

        bar = '[' + '='*self.current + ' '* (self.width-self.current) + ']:  '
        bar = bar + "{:.2f} %".format(self.percent)

        if list_extra_info == None:
            remove_previous_lines(1)
            print(bar)
        else:
            remove_previous_lines(1 + len(list_extra_info))
            print(bar)
            for info in list_extra_info:
                print(str(info))
    def finish(self):
        print('*' * (self.width))
        print('Completed:  ' + str(self.name))
        print('Time taken: ' + str(time.time() - self.time))
        print('*' * (self.width))
        print('')

# functions from {0,1,..,k-1} --> {0,1,...,n-1}
def hom(k, n):
    return list(itertools.product(range(n), repeat=k))
