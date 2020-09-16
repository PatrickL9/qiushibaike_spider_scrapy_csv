from scrapy import cmdline

name = 'qiushi_spider'
cmd = 'scrapy crawl {0} -o qiushi_4.csv'.format(name)
cmdline.execute(cmd.split())