'''
Created on Sep 6, 2013

@author: Guru
'''

import sys
import optparse
import numpy
import matplotlib.pyplot as plt;
import re

def setup_parser(parser) :
    parser.add_option("-f", "--file", type="string" , action="store", help="Input file to parse")
    parser.add_option("-x", "--x_axis", type="string" , action="store", help="X-Axis name")
    parser.add_option("-y", "--y_axis", type="string" , action="store", help="Y-Axis name")
    parser.add_option("-o", "--output", type="string" , action="store", help="File in which resulting plot is to be stored")
    parser.add_option("--x_conversion", type="string" , action="store", help="Apply a formula on each value of the X-Axis")
    parser.add_option("--y_conversion", type="string" , action="store", help="Apply a formula on each value of the Y-Axis")

def check_options(options) :
   
    assert options.file != None, "Must specify input file to parse!"
        
    if options.x_conversion != None :
        assert options.x_axis != None, "Must specify x_axis when specifying x_conversion"
    if options.y_conversion != None :
        assert options.y_axis != None, "Must specify y_axis when specifying y_conversion"


def convert(value, logic) :
    match_obj = re.match("([-/+*])\s*(\d+e?\d+)", logic)
    
    if match_obj.group(1) is "+" :
        return float(float(value) + float(match_obj.group(2)))
    if match_obj.group(1) is "-" :
        return float(float(value) - float(match_obj.group(2)))
    if match_obj.group(1) is "*" :
        return float(float(value) * float(match_obj.group(2)))
    if match_obj.group(1) is "/" :
        return float(float(value) / float(match_obj.group(2)))

if __name__ == '__main__':
    parser = optparse.OptionParser()
    setup_parser(parser)
    
    (options, args) = parser.parse_args()
    
    check_options(options)
    
    input_file = open(options.file, "r")
    
    x_axis = []
    y_axis = []
    for line in input_file :
        split = line.split('=', 1)
        if len(split) < 2 :
            print 'Warning: Ignored line :\n' + line + '\n'
            continue
        
        x_val = split[0]
        y_val = split[1]
        
        if options.x_conversion != None :
            x_val = convert(x_val, options.x_conversion)
        if options.y_conversion != None :
            y_val = convert(y_val, options.y_conversion)
        
        x_axis.append(x_val)
        y_axis.append(y_val)
    
    plt.plot(x_axis, y_axis)
    
    if options.x_axis != None :
        plt.xlabel(options.x_axis)
    if options.y_axis != None :
        plt.ylabel(options.y_axis)
    
    plt.grid(True)
    
    if options.output != None :
        plt.savefig(options.output + '.svg')
        
    plt.show()
