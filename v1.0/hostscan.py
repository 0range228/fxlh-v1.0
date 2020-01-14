import sys
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon


# class App(QWidget):
#
#     def __init__(self):
#         super().__init__()
#         self.title = 'PyQt5 file system view - pythonspot.com'
#         self.left = 10
#         self.top = 10
#         self.width = 640
#         self.height = 480
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
#         self.model = QFileSystemModel()
#         self.model.setRootPath('http://192.168.134.130:8080/')
#         self.tree = QTreeView()
#         self.tree.setModel(self.model)
#         self.tree.setAnimated(False)
#         self.tree.setIndentation(20)
#         self.tree.setSortingEnabled(True)
#         self.tree.setWindowTitle("Dir View")
#         self.tree.resize(640, 480)
#         windowLayout = QVBoxLayout()
#         windowLayout.addWidget(self.tree)
#         self.setLayout(windowLayout)
#         self.show()
#


# import sys
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
#
# class TreeView(QTreeView):
#     def __init__(self, parent=None):
#         super(TreeView, self).__init__(parent)
#
#         self.__model = QFileSystemModel()
#         self.__model.setRootPath(QDir.rootPath())
#         self.setModel(self.__model)
#
#         self.__current_select_path = None
#         self.doubleClicked.connect(self.__getCurPathEvent)
#
#     #双击信号 获得当前选中的节点的路径
#     def __getCurPathEvent(self):
#         index = self.currentIndex()
#         model = index.model()  # 请注意这里可以获得model的对象
#         self.__current_select_path = model.filePath(index)
#
#     # 设置TreeView的跟文件夹
#     def setPath(self, path):
#         self.setRootIndex(self.__model.index(path))
#
#     # 获得当前选中的节点的路径
#     def getCurPath(self):
#         return self.__current_select_path
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#
#     asset = TreeView()
#     asset.setPath(r"D:/")
#     asset.show()
#
#     sys.exit(app.exec_())

# import sys
# from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout
# from PyQt5.QtGui import QIcon
#
#
# class App(QWidget):
#
#     def __init__(self):
#         super().__init__()
#         self.title = 'PyQt5 file system view - pythonspot.com'
#         self.left = 10
#         self.top = 10
#         self.width = 640
#         self.height = 480
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
#         self.model = QFileSystemModel()
#         self.model.setRootPath('')
#         self.tree = QTreeView()
#         self.tree.setModel(self.model)
#         self.tree.setAnimated(False)
#         self.tree.setIndentation(20)
#         self.tree.setSortingEnabled(True)
#         self.tree.setWindowTitle("Dir View")
#         self.tree.resize(640, 480)
#         windowLayout = QVBoxLayout()
#         windowLayout.addWidget(self.tree)
#         self.setLayout(windowLayout)
#         self.show()
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = App()
#     sys.exit(app.exec_())


# class TreeWidget(QMainWindow):
#     myControls = {}
#     def __init__(self, parent=None):
#         QWidget.__init__(self, parent)
#         self.setWindowTitle('TreeWidget')
#         self.tree = QTreeWidget()
#         self.myControls['tree'] = self.tree
#         self.tree.setColumnCount(5)  # 说明是树形的表，
#         # self.tree.setHeaderLabels(['Key', 'Value'])  # 是表，则有表头
#         # 根节点的父是 QTreeWidget对象
#         root = QTreeWidgetItem(self.tree)
#
#         root.setText(0, 'root')
#         child1 = QTreeWidgetItem(root)  # 指出父结点
#         child1.setText(0, 'child1')
#         child1.setText(1, 'name1')
#         child2 = QTreeWidgetItem(root)
#         child2.setText(0, 'child2')
#         child2.setText(1, 'name2')
#         child3 = QTreeWidgetItem(root)
#         child3.setText(0, 'child3')
#         child4 = QTreeWidgetItem(child3)
#         child4.setText(0, 'child4')
#         child4.setText(1, 'name4')
#         # 以下两句是主窗口的设置
#         self.tree.addTopLevelItem(root)
#         self.setCentralWidget(self.tree)
#
#
#         def on_addAction_triggered(self):
#             currNode = self.tree.currentItem()
#             addChild1 = QTreeWidgetItem()
#             addChild1.setText(0, 'addChild1_key')
#             addChild1.setText(1, 'addChild1_val')
#             currNode.addChild(addChild1)
#
#         def on_editdAction_triggered(self):
#             currNode = self.tree.currentItem()
#             currNode.setText(0, 'editkey')
#             currNode.setText(1, 'editvalue')
#
#         def on_deleteAction_triggered(self):
#             currNode = self.tree.currentItem()
#             parent1 = currNode.parent();
#             parent1.removeChild(currNode)
#
#         def on_findAction_triggered(self):
#             # MatchRegExp 正则查找，MatchRecursive递归遍历，最后是指树表的第几列值
#             # 本例是 查找第0中 所有开头含有”child“文字的节点
#             nodes = self.tree.findItems("^child[\w|\W]*", Qt.MatchRegExp | Qt.MatchRecursive, 0)
#             for node in nodes:
#                 QMessageBox.information(self, '', node.text(0))
#
#         # 带图标是这形式QAction(QIcon("ss.png"), "add", self)
#         #addAction = QAction("增加", self)
#         #addAction.triggered.connect(self.on_addAction_triggered)
#
#         #editAction = QAction("修改", self)
#         #editAction.triggered.connect(self.on_editdAction_triggered)
#
#         #deleteAction = QAction("删除", self)
#         #deleteAction.triggered.connect(self.on_deleteAction_triggered)
#
#         #findAction = QAction("查找", self)
#         #findAction.triggered.connect(self.on_findAction_triggered)
#
#
#         #toolbar = self.addToolBar("aa")
#         #toolbar.addAction(addAction)
#         #toolbar.addAction(editAction)
#         #toolbar.addAction(deleteAction)
#         #toolbar.addAction(findAction)
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     tp = TreeWidget()
#     tp.show()
#     sys.exit(app.exec_())

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Teww(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle("TEww")
        self.tree=QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["key","value"])
        root=QTreeWidgetItem(self.tree)
        root.setText(0,"root")
        child1=QTreeWidgetItem(root)
        child1.setText(0,"child1")
        child1.setText(1,"name")
        child2=QTreeWidgetItem(root)
        child2.setText(0,"child2")
        child2.setText(1,"name")
        child3=QTreeWidgetItem(child2)
        child3.setText(0,"child3")
        child3.setText(1,"name")
        child4=QTreeWidgetItem(child3)
        child4.setText(0,"child4")
        child4.setText(1,"name")
        self.tree.addTopLevelItem(root)
        self.setCentralWidget(self.tree)
        self.root_2()
        self.root_3()

    def root_2(self):
        root2=QTreeWidgetItem(self.tree)
        root2.setText(0,"root2")
        child5=QTreeWidgetItem(root2)
        child5.setText(0,"child5")
        child5.setText(1,"ddd")
        self.tree.addTopLevelItem(root2)
        self.setCentralWidget(self.tree)
    def root_3(self):
        root3=QTreeWidgetItem(self.tree)
        root3.setText(0,"root3")
        child6=QTreeWidgetItem(root3)
        child6.setText(0,"child6")
        child6.setText(1,"child6")
        self.tree.addTopLevelItem(root3)
        self.setCentralWidget(self.tree)
if __name__=="__main__":
    app = QApplication(sys.argv)
    tp = Teww()
    tp.show()
    app.exec_()