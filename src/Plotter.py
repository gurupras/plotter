'''
Created on Sep 6, 2013

@author: Guru
'''

import sys
import optparse
import numpy
import matplotlib.pyplot as plt;
import re
import operator

def setup_parser(parser) :
    parser.add_option("-f", "--file"  , type="string", action="store", help="Input file to parse")
    parser.add_option("-x", "--x_axis", type="string", action="store", help="X-Axis name")
    parser.add_option("-y", "--y_axis", type="string", action="store", help="Y-Axis name")
    parser.add_option("-o", "--output", type="string", action="store", help="File in which resulting plot is to be stored")
    parser.add_option("--x_conversion", type="string", action="store", help="Apply a formula on each value of the X-Axis")
    parser.add_option("--y_conversion", type="string", action="store", help="Apply a formula on each value of the Y-Axis")
    parser.add_option("--window_size" , type="string", action="store", help="Window size to use for moving average")

def check_options(options) :
   
    assert options.file != None, "Must specify input file to parse!"
        
    if options.x_conversion != None :
        assert options.x_axis != None, "Must specify x_axis_raw when specifying x_conversion"
    if options.y_conversion != None :
        assert options.y_axis != None, "Must specify y_axis_raw when specifying y_conversion"


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

def smoothen(plot_points, window_size) :
#     We need to sort before smoothing
    sorted_output_raw = sorted(plot_points.iteritems(), key=operator.itemgetter(0))
    
    x_axis_sum  = 0
    y_axis_sum  = 0
    
    x_axis      = []
    y_axis      = []
    
    for index in range(len(sorted_output_raw)) :
        x_axis_raw = sorted_output_raw[index][0]
        y_axis_raw = sorted_output_raw[index][1]
        
        x_axis_sum  = x_axis_sum + x_axis_raw
        y_axis_sum  = y_axis_sum + y_axis_raw

        if index >= window_size - 1 :
            x_axis.append(int(x_axis_sum / window_size))
            y_axis.append(int(y_axis_sum / window_size))
            
            x_axis_sum = x_axis_sum - sorted_output_raw[index - window_size + 1][0]
            y_axis_sum = y_axis_sum - sorted_output_raw[index - window_size + 1][1]
        
    return x_axis, y_axis
            
if __name__ == '__main__':
    parser = optparse.OptionParser()
    setup_parser(parser)
    
    (options, args) = parser.parse_args()
    
    check_options(options)
    
    input_file = open(options.file, "r")
    
    plot_points = {}
    for line in input_file :
        split = line.split('=', 1)
        if len(split) < 2 :
            print 'Warning: Ignored line :\n' + line + '\n'
            continue
        
        x_val = float(split[0])
        y_val = float(split[1])
        
        if options.x_conversion != None :
            x_val = convert(x_val, options.x_conversion)
        if options.y_conversion != None :
            y_val = convert(y_val, options.y_conversion)

        plot_points.update({x_val: y_val})
    
    x_axis = plot_points.keys()
    y_axis = plot_points.values()
    if options.window_size != None :
        (x_axis, y_axis) = smoothen(plot_points, int(options.window_size))
    
    plt.plot(x_axis, y_axis)
    plt.axis([min(x_axis), max(x_axis) + min(x_axis), min(y_axis), max(y_axis) + min(y_axis)])
    
    if options.x_axis != None :
        plt.xlabel(options.x_axis)
    if options.y_axis != None :
        plt.ylabel(options.y_axis)
    
    plt.grid(True)
    
    if options.output != None :
        plt.savefig(options.output + '.svg')
        plt.savefig(options.output + '.png')
        
    plt.show()
