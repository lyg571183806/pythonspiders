## 环境部署
1. 安装virtualenv和virtualenvwrapper
```
pip install -i https://pypi.douban.com/simple virutalenv
pip install -i https://pypi.douban.com/simple virutalenvwrapper
```
2. 新建虚拟环境
```
mkvirtualenv --python=/usr/local/bin/python3 scrapyspiders
workon scrapyspiders
```

2. 安装scrapy
```
pip install -i https://pypi.douban.com/simple scrapy
```

3. 创建一个scrapy项目
```
scrapy startproject scrapyspiders
```