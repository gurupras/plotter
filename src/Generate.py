'''
Created on Sep 7, 2013

@author: Guru
'''

import optparse
import subprocess
import os
import sys

class Wrapper :
    __file          = None
    __output        = None
    __x_axis        = None    
    __y_axis        = None
    __x_conversion  = None
    __y_conversion  = None
    __window_size   = None
    
    def __init__(self, input_file, output=None, x_axis=None, y_axis=None, x_conversion=None, y_conversion=None, window_size=None) :
        self.__file         = input_file
        self.__output       = output
        self.__x_axis       = x_axis
        self.__y_axis       = y_axis
        self.__x_conversion = x_conversion
        self.__y_conversion = y_conversion
        self.__window_size  = window_size

    def build(self) :
        cmdline = []
        
        cmdline.append("python Plotter.py")
        cmdline.append("--file \"" + self.__file + "\"")
        
        if self.__output != None :
            cmdline.append("--output \"" + self.__output + "\"")
        if self.__x_axis != None :
            cmdline.append("--x_axis \"" + self.__x_axis + "\"")
        if self.__y_axis != None :
            cmdline.append("--y_axis \"" + self.__y_axis + "\"")
        if self.__x_conversion != None :
            cmdline.append("--x_conversion \"" + self.__x_conversion + "\"")
        if self.__y_conversion != None :
            cmdline.append("--y_conversion \"" + self.__y_conversion + "\"")
        if self.__window_size != None :
            cmdline.append("--window_size " + self.__window_size)
        
        cmd = ""
        for line in cmdline :
            cmd += line + " "
        return cmd


def setup_parser(parser) :
    parser.add_option("-p", "--path"        , type="string" , action="store", help="Path for input files")
    parser.add_option("-o", "--outdir"      , type="string" , action="store", help="Path for output")
    parser.add_option("-w", "--window_size" , type="string" , action="store", help="Window size for moving average")
    parser.add_option("-t", "--test"        ,                 action="store_true", help="Dry run - prints commands and exits")

def check_options(options) :
   
    assert options.path != None, "Must specify path!"
    
    if options.outdir == None :
        options.outdir = os.path.join(options.path, "plots")
        if not os.path.exists(options.outdir) :
            os.mkdir(options.outdir)
#     assert options.outdir != None, "Must specify output path!"

if __name__ == '__main__':
    parser = optparse.OptionParser()
    setup_parser(parser)
    
    (options, args) = parser.parse_args()
    check_options(options)
    
    timing_obj  = Wrapper(input_file=os.path.join(options.path, "timing_data"), output=os.path.join(options.outdir, "timing"), x_axis="Area", y_axis="Time (seconds)", y_conversion="/ 1e9", window_size=options.window_size)
    memory_obj  = Wrapper(input_file=os.path.join(options.path, "memory_data"), output=os.path.join(options.outdir, "memory"), x_axis="Area", y_axis="Memory (Megabytes)", y_conversion="/ 1e6", window_size=options.window_size)
    max_mem_obj = Wrapper(input_file=os.path.join(options.path, "max_mem_data"), output=os.path.join(options.outdir, "max_mem"), x_axis="Area", y_axis="Max Mem (Megabytes)", y_conversion="/ 1e6", window_size=options.window_size)
    

    print "Commandlines :\n"
    print timing_obj.build() + "\n"
    print memory_obj.build() + "\n"
    print max_mem_obj.build() + "\n"
    if options.test is True :
        sys.exit(0)

    procs = []
    procs.append(subprocess.Popen(timing_obj.build(), shell=True))
    procs.append(subprocess.Popen(memory_obj.build(), shell=True))
    procs.append(subprocess.Popen(max_mem_obj.build(), shell=True))
    
    while 1 :
        for proc in procs :
            flag = 1
            if proc.poll() is None :
                flag = 0
        if flag is 1 :
            break


    
