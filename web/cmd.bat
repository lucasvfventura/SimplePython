@ECHO OFF
set search=%1
cd ../webot
scrapy crawl amazon -a search=%search%
scrapy crawl londondrugs -a search=%search%