# 中国象棋 Python | Chinese Chess Python
中国象棋Python版本，本项目主要借鉴了[sunfish](https://github.com/thomasahle/sunfish)
## 特性
- 代码简洁：仅仅使用一百多行代码即实现了中国象棋，并具有简单对战功能。
- 性能高效：经测试水平在初学者之上。

## 缺点
- 现代竞技象棋有许多复杂的规则，例如不得长将，长吃等，参见[2011版象棋规则](www.xqbase.com/protocol/rule2011.pdf)。本程序仅实现了基本规则，未实现禁手。
- 没有引入随机参数，导致在相同局面下程序总是会有相同的输出。
- 进攻欲望较低，与人对战“以守为攻”。

## 注意
- 本程序使用的象棋棋子来自Unicode13中的[棋类符号](https://www.unicode.org/charts/PDF/U1FA00.pdf)，如果你的电脑能正确显示以下几个字符：🩠 🩡 🩢 🩣 🩤 🩦 🩥 🩧 🩨 🩩 🩪 🩫 🩭 🩬，则可以最大程度上利用本程序，否则请修改`sunfish_chinese.py`448行为`pieces = chinese_pieces`。
- 因为字体关系，有些字体中文字符长度不等于两个英文字符长度，所以显示效果因字体而异，可以手动调节`sunfish_chinese.py`中452或454行获得最佳显示效果。
- 测试运行环境为Ubuntu20.04，使用系统terminal，字体为Monospace Regular。

## 运行截图

![xiangqi_unicode](screenshot/xiangqi_unicode.png)

如果设置`pieces = chinese_pieces`

![xaingqi_chinese](screenshot/xiangqi_chinese.png)

# 运行程序
```shell
python sunfish_chinese.py
```

## 棋盘显示
本仓库代码还实现了中文棋盘显示，运行`python chinese_chess_board.py`即可。同样，如果字体不支持Unicode13， 可修改`chinese_chess_board.py`第一行为`def chinese_chess(mode=''):`。效果如下所示：

如果字体支持Unicode13

![chess_board_unicode](screenshot/chess_board_unicode.png)

如果不支持Unicode13

![chess_board_chinese](screenshot/chess_board_chinese.png)