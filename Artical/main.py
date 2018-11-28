from scrapy.cmdline import execute
import sys
import os

#先获取本文件的绝对路径；然后再获取路径前面的目录（即去掉文件名的路径）
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy","crawl","bole"])







