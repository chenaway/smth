#!/usr/bin/env python
#encoding=utf8
"""
get lastest smth job information, search by keyword
author: chenaway@qq.com
"""

import requests as r
import re
g = r.get
fa = re.findall

# ---------------


def get_html(url):
    return g(url).content.decode('gbk').encode('utf8')


def search(keyword):
    ''' search for keyword'''
    pattern = 'http://www.newsmth.net/nForum/s/article?\
ajax&t1=%s&au=&b=Career_Upgrade'
    url = pattern % keyword
    html = get_html(url)
    return get_index_title(html)

# ---------------


def html_clean(html):
    ''' clean html tags and escaped chars '''
    ret = re.sub('<br />', '\n', html)
    ret = re.sub('&nbsp;', ' ', ret)
    ret = re.sub('<[^<]*>', '', ret)
    return ret


def get_index_title(html):
    # get links and titles
    pattern = u'<a href="/nForum/article/Career_Upgrade/(\d+)">([^<]*)</a>'
    links = fa(pattern, html)
    return links


def get_detail_page(tid):
    ''' get the detail page '''
    url = 'http://www.newsmth.net/nForum/article/Career_Upgrade/%s?ajax' % tid
    html = g(url).content.decode('gbk')
    return html


def get_detail(html):
    ''' get detail of a topic '''
    detail = re.findall(u'站内(.*?)来源', html)[0]
    detail = html_clean(detail)
    return detail.encode('utf8')


def get_detail_with_comment(html):
    ''' get detail of a topic with comment '''
    detail_with_comment = re.findall(u'站内(.*)来源', html)[0]
    detail_with_comment = html_clean(detail_with_comment)
    return detail_with_comment.encode('utf8')


def main():
    links = search('python')
    for tid, title in links:
        print '-'*30
        print tid, title
        html = get_detail_page(tid)
        print get_detail(html)


if __name__ == '__main__':
    main()
