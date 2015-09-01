#!/usr/bin/env python
#encoding=utf8
"""
get lastest smth job information
author: chenaway@qq.com
"""

import requests as r
import re
g = r.get
fa = re.findall


def remove_top(html):
    ''' remove top items in first page '''
    return re.sub('<tr class="top">.*?</tr>', '', html)


def html_clean(html):
    ''' clean html tags and escaped chars '''
    ret = re.sub('<br />', '\n', html)
    ret = re.sub('&nbsp;', ' ', ret)
    ret = re.sub('<[^<]*>', '', ret)
    return ret


def local_page(page):
    ''' get local page '''
    with open('%s.html' % page) as f:
        return f.read()


def get_index_page(page):
    ''' get list of topics '''

    # get html
    url = 'http://www.newsmth.net/nForum/board/Career_Upgrade?ajax&p=%s' % page
    html = g(url).content.decode('gbk').encode('utf8')
    open('%s.html' % page, 'w+').write(html)

    # remove top items
    if page == 1:
        html = remove_top(html)
    return html


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
    page = 1
    html = get_index_page(page)
    links = get_index_title(html)
    for tid, title in links:
        print '-'*30
        print tid, title
        html = get_detail_page(tid)
        print get_detail(html)


if __name__ == '__main__':
    main()
