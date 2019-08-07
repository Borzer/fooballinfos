from scrapy.cmdline import execute

execute('scrapy crawl matchs'.split())

# 程序会报None值是因为球员信息有些信息是网页本身没有的 对程序并无影响 属于正常现象
