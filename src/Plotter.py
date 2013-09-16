'''
Created on Sep 6, 2013

@author: Guru
'''

import sys
import argparse
import numpy
import matplotlib.pyplot as plt;
import re
import operator

def setup_parser(parser) :
    parser.add_argument('-f', "--file"  , type=str, help="Input file to parse_args")
    parser.add_argument("-x", "--x_axis", type=str, help="X-Axis name")
    parser.add_argument("-y", "--y_axis", type=str, help="Y-Axis name")
    parser.add_argument("-o", "--output", type=str, help="File in which resulting plot is to be stored")
    parser.add_argument("--x_conversion", type=str, help="Apply a formula on each value of the X-Axis")
    parser.add_argument("--y_conversion", type=str, help="Apply a formula on each value of the Y-Axis")
    parser.add_argument("--window_size" , type=str, help="Window size to use for moving average")
    parser.add_argument("--legend"      , type=str, help="Plot legend while using multiplot")

def check_args(args) :
   
    assert args.file != None, "Must specify input file to parse_args!"
        
    if args.x_conversion != None :
        assert args.x_axis != None, "Must specify x_axis_raw when specifying x_conversion"
    if args.y_conversion != None :
        assert args.y_axis != None, "Must specify y_axis_raw when specifying y_conversion"


def convert(value, logic) :
#     logic = logic.strip("\"'")
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


def parse_data(args) :
    plot_points = {}
    input_file = open(args.file, "r")
    for line in input_file :
        split = line.split('=', 1)
        if len(split) < 2 :
            print 'Warning: Ignored line :\n' + line + '\n'
            continue
        
        x_val = float(split[0])
        y_val = float(split[1])
        
        if args.x_conversion != None :
            x_val = convert(x_val, args.x_conversion)
        if args.y_conversion != None :
            y_val = convert(y_val, args.y_conversion)

        plot_points.update({x_val: y_val})
    return plot_points

def plot(plot_points, args, label=None) :
    x_axis = plot_points.keys()
    y_axis = plot_points.values()
    if args.window_size != None :
        (x_axis, y_axis) = smoothen(plot_points, int(args.window_size))
    
    plt.plot(x_axis, y_axis, label=label)
    plt.axis([0, max(x_axis) + min(x_axis), 0, max(y_axis) + min(y_axis)])
    
    if args.x_axis != None :
        plt.xlabel(args.x_axis)
    if args.y_axis != None :
        plt.ylabel(args.y_axis)
    
    plt.grid(True)


def save(args) :
    if args.output != None :
        plt.savefig(args.output + '.svg')
        plt.savefig(args.output + '.png')    


def show() :
    plt.show()


def parse_args(argv=None) :
    if argv is None :
        argv = sys.argv[1:]
    
    parser = argparse.ArgumentParser()
    setup_parser(parser)
    
    args = parser.parse_args(args=argv)
    
    check_args(args)
    return args

def multiplot(argv) :
    args = parse_args(argv)
#     args.file = args.file.strip("\"'")
    file_list = args.file.split(",")
    for input_file in file_list :
        args.file = input_file
        plot_points = parse_data(args)
        index = file_list.index(input_file)
        label = str(index + 1) + " " + args.legend
        plot(plot_points, args, label)
    plt.legend(loc=2)
    save(args)
    plt.clf()
        
if __name__ == '__main__':
    args = parse_args()
    
    plot_points = parse_data(args)

    plot(plot_points, args)
    save(args)
    show()
