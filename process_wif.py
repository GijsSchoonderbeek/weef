# Script to import WIF and process
# Gijs
# 11-1-2020

import numpy as np
import math
from six.moves.configparser import RawConfigParser
nof_shafts = 10
nof_treadles = nof_shafts

def read_wif(config, filename):
    config.read(filename)
    string = 'Treadles' + str(config.getint('WEAVING', 'Treadles'))
    print(string)

    try:
        if config.getboolean('CONTENTS', 'WEFT COLORS'):
            print('import color table')
            weft_color_map = {}
            for thread_no, value in config.items('WEFT COLORS'):
                weft_color_map[int(thread_no)] = int(value)
    except:
        print('Geen weft colors')
    else:
        print('No Weft Colors')

    if config.getboolean('CONTENTS', 'WARP'):
        print('import THREADING')

    threading = {}
    for thread_no, value in config.items('THREADING'):
        threading[int(thread_no)] = int(value)
    return config


def init_wif(config):
    config.add_section('WIF')
    config.add_section('CONTENTS')
    config.add_section('TEXT')
    config.set('CONTENTS', 'TEXT', 'true')
    config.add_section('WARP COLORS')
    config.set('CONTENTS', 'WARP COLORS', 'true')
    config.add_section('WARP SPACING')
    config.set('CONTENTS', 'WARP SPACING', 'true')
    config.add_section('WARP THICKNESS')
    config.set('CONTENTS', 'WARP THICKNESS', 'true')
    config.add_section('WEFT COLORS')
    config.set('CONTENTS', 'WEFT COLORS', 'true')
    config.add_section('WEFT SPACING')
    config.set('CONTENTS', 'WEFT SPACING', 'true')
    config.add_section('WEFT THICKNESS')
    config.set('CONTENTS', 'WEFT THICKNESS', 'true')
    config.add_section('TREADLING')
    config.set('CONTENTS', 'TREADLING', 'true')
    config.add_section('THREADING')
    config.set('CONTENTS', 'THREADING', 'true')
    config.add_section('WEAVING')
    config.set('CONTENTS', 'WEAVING', 'true')
    config.add_section('WARP')
    config.set('CONTENTS', 'WARP', 'true')
    config.add_section('WEFT')
    config.set('CONTENTS', 'WEFT', 'true')
    config.add_section('COLOR TABLE')
    config.set('CONTENTS', 'COLOR TABLE', 'true')
#    config.add_section('COLOR PALETTE')
#    config.set('CONTENTS', 'COLOR PALETTE', 'true')

    config.set('WIF', 'Date', '27-12-2019')
    config.set('WIF', 'Version', '0.1')
    config.set('WIF', 'Developers', 'Gijs')
    config.set('WIF', 'Source Program', 'MyScript')
    config.set('WEAVING', 'Rising Shed', 'true')
    config.set('WEAVING', 'Treadles', nof_treadles)
    config.set('WEAVING', 'Shafts', nof_shafts)
    config.set('WARP', 'Units', 'centimeters')
    config.set('WARP', 'Color', '1')
    config.set('COLOR TABLE', '1', '999, 0, 0')
    config.set('COLOR TABLE', '2', '0, 0, 999')
    config.set('COLOR TABLE', '3', '0, 999, 0')
    config.set('COLOR TABLE', '4', '500, 500, 0')
    config.set('COLOR TABLE', '5', '0, 500, 500')
    config.set('COLOR TABLE', '6', '500, 500, 0')
    config.set('COLOR TABLE', '7', '500, 500, 500')
    config.set('COLOR TABLE', '8', '999, 250, 250')
#    config.set('COLOR PALETTE', 'Range', '0,999')
#    config.set('COLOR PALETTE', 'Entries', '82')
    return config

def write_wif(config, filename, threads, treadles, nof_warp_color = 1, nof_weft_color = 2):

    for index in range(len(threads)):
        config.set('THREADING', str(index + 1), str(threads[index]))
        config.set('WARP COLORS', str(index + 1), str(1+(index % nof_warp_color)))
        config.set('WARP SPACING', str(index + 1), str(0.212))
        config.set('WARP THICKNESS', str(index + 1), str(0.212))
    for index in range(len(treadles)):
        config.set('TREADLING', str(index + 1), str(treadles[index]))
        config.set('WEFT COLORS', str(index + 1), str(3 + (index % nof_weft_color)))
        config.set('WEFT SPACING', str(index + 1), str(0.212))
        config.set('WEFT THICKNESS', str(index + 1), str(0.212))

    config.set('TEXT', 'Title', filename)
    config.set('WARP', 'Threads', len(threads))
    config.set('WEFT', 'Threads', len(treadles))

    tieup(config)
    with open(filename, 'w') as f:
        config.write(f)
    return config


def design_line(nof_threads=100, shafts=nof_shafts):
    threads = []
    for draad in range(nof_threads):
        ampl = nof_threads * (1 + np.sin((1 * np.pi / nof_threads) * draad))/2.5
        threads.append(math.floor(ampl % shafts) + 1)
    return threads

def read_threads(config):
    threads = []
    r_threads = {}
    for thread_no, value in config.items('THREADING'):
        r_threads[int(thread_no)] = int(value)
    for cnt in range(len(r_threads)):
        threads.append(r_threads[cnt+1])
    return threads

def tieup(config):
    config.add_section('TIEUP')
    config.set('CONTENTS', 'TIEUP', 'true')
    if nof_shafts == 10:
        line = [3, 8, 9, 10]
    else:
        line = [2,4,7,8]
    for cnt in range(nof_shafts):
        config.set('TIEUP', str(nof_shafts-cnt), str(line))
        for cnt_2 in range(len(line)):
            shaft = line[cnt_2] + 1
            if shaft > nof_shafts:
                shaft = shaft - nof_shafts
            line[cnt_2] = shaft

def extent(i_threads, extent_factor = 3 ):
    r_threads = []
    for cnt in range(len(i_threads)):
        for extent_cnt in range(extent_factor):
            r_threads.append(i_threads[cnt])
    return r_threads

def network(threads, shafts):
    r_threads=[]
    groups = 2
    shaft_per_group = shafts/groups
    for cnt in range(len(threads)):
        input_thread = threads[cnt]
#        r_threads.append(((input_thread + (cnt % shaft_per_group)) % shafts) + 1)
        if input_thread > ((cnt % shaft_per_group) + shaft_per_group):
            thread_loc = (cnt % shaft_per_group) + (2 * shaft_per_group)
        elif input_thread > (cnt % shaft_per_group):
            thread_loc = (cnt % shaft_per_group) + shaft_per_group
        else:
            thread_loc = (cnt % shaft_per_group)
        r_threads.append((thread_loc % shafts) + 1)
    return r_threads


def interleave(threads, shafts, x_offset, y_offset=0):
    r_threads = []
    offset_a = math.floor(x_offset/2)
    offset_b = 0#len(threads)-offset_a
    for cnt in range(len(threads)):
        r_threads.append(threads[(cnt + offset_a) % len(threads)])
#        r_threads.append(threads[cnt]) #(cnt + x_offset) % len(threads)])
        r_threads.append(((threads[(cnt + offset_b) % len(threads)] + y_offset - 1) % shafts) + 1)
    return r_threads


def main():
    filename = 'DesignBase.wif'
    make_new_wif = False
    config = RawConfigParser()
    if make_new_wif:
        init_wif(config)
        threads = design_line(nof_threads=100, shafts=nof_shafts)
        write_wif(config, filename, threads, threads, nof_warp_color=1, nof_weft_color=1)
    else:
        config = read_wif(config, filename)
        filename = 'Design_NW.wif'
        threads = read_threads(config)
        threads = extent(threads, extent_factor=4)
        threads = network(threads, config.getint('WEAVING', 'Shafts'))
        inter_warp = interleave(threads, shafts=nof_shafts, x_offset=75, y_offset=nof_shafts/2)
        inter_weft = interleave(threads, shafts=nof_shafts, x_offset=0, y_offset=0)
        write_wif(config, filename, inter_warp, inter_weft, nof_warp_color=2, nof_weft_color=2)


if __name__ == "__main__":
    main()
