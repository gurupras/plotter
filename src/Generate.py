'''
Created on Sep 7, 2013

@author: Guru
'''

import optparse
import subprocess
import os
import sys
import glob
import Plotter


class Wrapper :
    __file          = None
    __output        = None
    __x_axis        = None    
    __y_axis        = None
    __x_conversion  = None
    __y_conversion  = None
    __window_size   = None
    __legend        = None
    
    def __init__(self, input_file, output=None, x_axis=None, y_axis=None, x_conversion=None, y_conversion=None, window_size=None, legend=None) :
        self.__file         = input_file
        self.__output       = output
        self.__x_axis       = x_axis
        self.__y_axis       = y_axis
        self.__x_conversion = x_conversion
        self.__y_conversion = y_conversion
        self.__window_size  = window_size
        self.__legend       = legend

    def add_file(self, input_file_path) :
        if self.__file is None :
            self.__file = input_file_path
        else :
            self.__file = self.__file + "," + input_file_path
            
    def build_str(self) :
        cmdline = []
        
        cmdline.append("python Plotter.py")
        cmdline.append("--file=\"" + self.__file + "\"")
        
        if self.__output != None :
            cmdline.append("--output=\"" + self.__output + "\"")
        if self.__x_axis != None :
            cmdline.append("--x_axis=\"" + self.__x_axis + "\"")
        if self.__y_axis != None :
            cmdline.append("--y_axis=\"" + self.__y_axis + "\"")
        if self.__x_conversion != None :
            cmdline.append("--x_conversion=\"" + self.__x_conversion + "\"")
        if self.__y_conversion != None :
            cmdline.append("--y_conversion=\"" + self.__y_conversion + "\"")
        if self.__window_size != None :
            cmdline.append("--window_size=" + self.__window_size)
        
        cmd = ""
        for line in cmdline :
            cmd += line + " "
        return cmd

    def build_array(self) :
        cmdline = []
        
        cmdline.append("--file=" + self.__file)
        
        if self.__output != None :
            cmdline.append("--output=" + self.__output)
        if self.__x_axis != None :
            cmdline.append("--x_axis=" + self.__x_axis)
        if self.__y_axis != None :
            cmdline.append("--y_axis=" + self.__y_axis)
        if self.__x_conversion != None :
            cmdline.append("--x_conversion=" + self.__x_conversion)
        if self.__y_conversion != None :
            cmdline.append("--y_conversion=" + self.__y_conversion)
        if self.__window_size != None :
            cmdline.append("--window_size=" + self.__window_size)
        if self.__legend != None :
            cmdline.append("--legend=" + self.__legend)
        
        return cmdline


def setup_parser(parser) :
    parser.add_option("-p", "--path"        , type="string" , action="store"     , help="Path for input files")
    parser.add_option("-o", "--outdir"      , type="string" , action="store"     , help="Path for output")
    parser.add_option("-w", "--window_size" , type="string" , action="store"     , help="Window size for moving average")
    parser.add_option("-t", "--test"        ,                 action="store_true", help="Dry run - prints commands and exits")
    parser.add_option("-m", "--multiplot"   ,                 action="store_true", help="Plot multiple files on a single figure")
    parser.add_option(      "--legend"      , type="string" , action="store"     , help="Labels for plots in multiplot mode")

def check_options(options) :
   
    assert options.path != None, "Must specify path!"
    
    if options.outdir == None :
        options.outdir = os.path.join(options.path, "plots")
        if not os.path.exists(options.outdir) :
            os.mkdir(options.outdir)
            
    if options.multiplot :
        assert options.legend != None, "Must specify legend in multiplot mode"
#     assert options.outdir != None, "Must specify output path!"


def multiplot(options) :
    files_path_list = glob.glob(os.path.join(options.path, "timing_data_*"))
    timing_obj  = Wrapper(input_file=None, output=os.path.join(options.outdir, "timing"), x_axis="Area", y_axis="Time (seconds)", 
                          y_conversion="/ 1e9", window_size=options.window_size, legend=options.legend)
    for file_path in sorted(files_path_list) :
        file_path = file_path.strip("\"'")
        timing_obj.add_file(file_path)
    Plotter.multiplot(timing_obj.build_array())
    
    files_path_list = glob.glob(os.path.join(options.path, "memory_data_*"))
    memory_obj  = Wrapper(input_file=None, output=os.path.join(options.outdir, "memory"), x_axis="Area", y_axis="Memory (Megabytes)", 
                          y_conversion="/ 1e6", window_size=options.window_size, legend=options.legend)
    for file_path in sorted(files_path_list) :
        file_path = file_path.strip("\"'")
        memory_obj.add_file(file_path)
    Plotter.multiplot(memory_obj.build_array())
    
    files_path_list = glob.glob(os.path.join(options.path, "max_mem_data_*"))
    max_mem_obj = Wrapper(input_file=None, output=os.path.join(options.outdir, "max_mem"), x_axis="Area", y_axis="Max Mem (Megabytes)", 
                          y_conversion="/ 1e6", window_size=options.window_size, legend=options.legend)    
    for file_path in sorted(files_path_list) :
        file_path = file_path.strip("\"'")
        max_mem_obj.add_file(file_path)
    Plotter.multiplot(max_mem_obj.build_array())
    
    
if __name__ == '__main__':
    parser = optparse.OptionParser()
    setup_parser(parser)
    
    (options, args) = parser.parse_args()
    check_options(options)
    
    if options.multiplot :
        multiplot(options)
        sys.exit(0)
    
    timing_obj  = Wrapper(input_file=os.path.join(options.path, "timing_data"), output=os.path.join(options.outdir, "timing"), 
                          x_axis="Area", y_axis="Time (seconds)", y_conversion="/ 1e6", window_size=options.window_size)
    memory_obj  = Wrapper(input_file=os.path.join(options.path, "memory_data"), output=os.path.join(options.outdir, "memory"), 
                          x_axis="Area", y_axis="Memory (Megabytes)", y_conversion="/ 1e6", window_size=options.window_size)
    max_mem_obj = Wrapper(input_file=os.path.join(options.path, "max_mem_data"), output=os.path.join(options.outdir, "max_mem"), 
                          x_axis="Area", y_axis="Max Mem (Megabytes)", y_conversion="/ 1e6", window_size=options.window_size)
    
    print "Commandlines :\n"
    print timing_obj.build_str() + "\n"
    print memory_obj.build_str() + "\n"
    print max_mem_obj.build_str() + "\n"
    if options.test is True :
        sys.exit(0)

    procs = []
    procs.append(subprocess.Popen(timing_obj.build_str(), shell=True))
    procs.append(subprocess.Popen(memory_obj.build_str(), shell=True))
    procs.append(subprocess.Popen(max_mem_obj.build_str(), shell=True))
    
    while 1 :
        for proc in procs :
            flag = 1
            if proc.poll() is None :
                flag = 0
        if flag is 1 :
            break


    
