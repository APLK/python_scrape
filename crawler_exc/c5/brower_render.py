# encoding:utf-8
'''
@author:lk

@time:2018/5/4 

@desc:

'''
import sys

import time

try:
    from PySide.QtGui import QApplication
    from PySide.QtCore import QUrl, QEventLoop, QTimer
    from PySide.QtWebKit import QWebView
except ImportError:
    from PyQt4.QtGui import QApplication
    from PyQt4.QtCore import QUrl, QEventLoop, QTimer
    from PyQt4.QtWebKit import QWebView


class BrowserRender(QWebView):
    def __init__(self,show=True):
        self.app = QApplication(sys.argv)
        QWebView.__init__(self)
        if show:
            self.show()#显示浏览器


    def download(self,url,timeout=60):
        loop = QEventLoop()
        timer = QTimer()
        timer.setSingleShot(True)#让定时器只执行一次
        timer.timeout.connect(loop.quit)
        self.loadFinished.connect(loop.quit)
        self.load(QUrl(url))
        timer.start(timeout*1000)

        loop.exec_()

        if timer.isActive():
            timer.stop()
            return self.html()
        else:
            print('请求超时:'+url)

    def html(self):
        return self.page().mainFrame().toHtml()

    def find(self, pattern):
        return self.page().mainFrame().findAllElements(pattern)

    def attr(self,pattern,name,value):
        '''
        设置value属性值
        :param pattern:
        :param name:
        :param value:
        :return:
        '''
        for e in self.find(pattern):
            e.setAttribute(name,value)

    def text(self,pattern,value):
        for e in self.find(pattern):
            e.setPlainText(value)

    def click(self,pattern):
        for e in self.find(pattern):
            e.evaluateJavaScript('this.click()')

    def wait_load(self,pattern,timeout=60):
        deadline = time.time() + timeout
        while time.time()<deadline:
            self.app.processEvents()
            matches = self.find(pattern)
            if matches:
                return matches
        print('等待超时')


br = BrowserRender()
br.download('http://example.webscraping.com/places/default/search')
br.attr('#search_term','value','.')
br.text('#page_size option','1000')
br.click('#search')
elements = br.wait_load('#results a')
if elements:
    countries = [e.toPlainText().strip() for e in elements]
    print(countries)
