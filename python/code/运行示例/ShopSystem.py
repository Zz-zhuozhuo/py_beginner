import sys
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFrame, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox,
                            QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import (QPainter, QColor, QBrush, QPen, QFont, QLinearGradient, 
                        QRadialGradient, QGuiApplication)

class TitleBar(QFrame):
    """窗口标题栏，包含标题和控制按钮"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()
        
    def initUI(self):
        self.setFixedHeight(30)
        self.setStyleSheet("background-color: transparent;")
        
        # 布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(5)
        
        # 标题
        self.title_label = QLabel("依力全球连锁超市充值系统")
        self.title_label.setFont(QFont("微软雅黑", 10))
        self.title_label.setStyleSheet("color: rgb(100, 100, 100);")
        layout.addWidget(self.title_label)
        
        # 占位符，将按钮推到右侧
        layout.addStretch()
        
        # 最小化按钮
        self.min_btn = QPushButton("—")
        self.min_btn.setFixedSize(20, 20)
        self.min_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: rgb(100, 100, 100);
                border-radius: 10px;
                font-size: 14px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(200, 200, 200, 50);
            }
        """)
        self.min_btn.clicked.connect(self.parent.showMinimized)
        layout.addWidget(self.min_btn)
        
        # 最大化/还原按钮
        self.max_btn = QPushButton("□")
        self.max_btn.setFixedSize(20, 20)
        self.max_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: rgb(100, 100, 100);
                border-radius: 10px;
                font-size: 10px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(200, 200, 200, 50);
            }
        """)
        self.max_btn.clicked.connect(self.toggle_maximize)
        layout.addWidget(self.max_btn)
        
        # 关闭按钮
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: rgb(100, 100, 100);
                border-radius: 10px;
                font-size: 12px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(255, 99, 71, 100);
                color: white;
            }
        """)
        self.close_btn.clicked.connect(self.parent.close)
        layout.addWidget(self.close_btn)
        
        # 窗口拖动相关变量
        self.dragging = False
        self.drag_start_position = QPoint()
        
    def toggle_maximize(self):
        """切换窗口最大化/还原状态"""
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.max_btn.setText("□")
        else:
            self.parent.showMaximized()
            self.max_btn.setText("▢")
            
    def mousePressEvent(self, event):
        """鼠标按下事件，用于窗口拖动"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_start_position = event.globalPos() - self.parent.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        """鼠标移动事件，用于窗口拖动"""
        if self.dragging and event.buttons() & Qt.LeftButton and not self.parent.isMaximized():
            self.parent.move(event.globalPos() - self.drag_start_position)
            event.accept()
            
    def mouseReleaseEvent(self, event):
        """鼠标释放事件，结束窗口拖动"""
        self.dragging = False

class FrostedGlassFrame(QFrame):
    """毛玻璃效果框架"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                border-radius: 15px;
                background-color: rgba(255, 255, 255, 0.7);
            }
        """)
        
        # 阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)
        
    def paintEvent(self, event):
        """绘制毛玻璃效果"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制半透明背景
        rect = self.rect()
        brush = QBrush(QColor(255, 255, 255, 180))  # 70% 透明度
        painter.fillRect(rect, brush)
        
        # 绘制边框
        pen = QPen(QColor(255, 255, 255, 100), 1)
        painter.setPen(pen)
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 15, 15)

class StyledButton(QPushButton):
    """简化版带样式的按钮，无动画避免崩溃"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.line_visible = False
        
        # 固定按钮大小
        self.setFixedSize(200, 50)
        
        # 设置初始样式（淡粉色）
        self.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 228, 225);
                color: rgb(100, 100, 100);
                font-family: '微软雅黑';
                font-size: 14px;
                font-weight: bold;
                border-radius: 25px;
                border: 1px solid rgba(255, 192, 203, 100);
            }
            QPushButton:hover {
                background-color: rgb(139, 0, 0); /* 深红色背景 */
                color: white;
                border: 2px solid rgba(101, 67, 33, 200);
            }
        """)
        
        # 创建正常状态阴影
        self.normal_shadow = QGraphicsDropShadowEffect(self)
        self.normal_shadow.setBlurRadius(5)
        self.normal_shadow.setColor(QColor(0, 0, 0, 30))
        self.normal_shadow.setOffset(0, 2)
        
        # 创建悬停状态阴影
        self.hover_shadow = QGraphicsDropShadowEffect(self)
        self.hover_shadow.setBlurRadius(10)
        self.hover_shadow.setColor(QColor(139, 0, 0, 80))
        self.hover_shadow.setOffset(0, 3)
        
        # 设置初始阴影
        self.setGraphicsEffect(self.normal_shadow)
        
    def enterEvent(self, event):
        """鼠标进入事件 - 切换到悬停阴影效果"""
        self.setGraphicsEffect(self.hover_shadow)
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        """鼠标离开事件 - 恢复正常阴影效果"""
        self.setGraphicsEffect(self.normal_shadow)
        super().leaveEvent(event)
    
    def paintEvent(self, event):
        """绘制按钮"""
        # 调用父类的paintEvent确保按钮正常绘制
        super().paintEvent(event)

class RechargeSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        """初始化界面"""
        # 窗口设置
        self.setWindowTitle("参玖小店充值系统")
        self.setFixedSize(600, 450)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 创建主部件和布局
        self.central_widget = QFrame(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 添加标题栏（带控制按钮）
        self.title_bar = TitleBar(self)
        self.main_layout.addWidget(self.title_bar)
        
        # 创建内容区域
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("background-color: transparent;")
        self.content_layout = QVBoxLayout(self.content_frame)
        self.main_layout.addWidget(self.content_frame)
        
        # 创建毛玻璃效果的主容器
        self.glass_frame = FrostedGlassFrame(self)
        self.glass_layout = QVBoxLayout(self.glass_frame)
        self.glass_layout.setContentsMargins(50, 30, 50, 30)
        self.glass_layout.setSpacing(20)
        
        # 标题
        self.title_label = QLabel("参玖小店充值系统")
        self.title_label.setFont(QFont("微软雅黑", 18, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: rgb(156, 39, 176);")  # #9C27B0
        self.glass_layout.addWidget(self.title_label)
        
        # 新用户判断
        self.new_user_layout = QHBoxLayout()
        self.new_user_label = QLabel("是否为新用户：")
        self.new_user_label.setFont(QFont("微软雅黑", 12))
        self.new_user_label.setStyleSheet("color: rgb(51, 51, 51);")
        
        self.new_user_input = QLineEdit()
        self.new_user_input.setFont(QFont("微软雅黑", 12))
        self.new_user_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 20px;
                background-color: rgba(255, 255, 255, 0.8);
            }
        """)
        
        # 设置提示文字
        self.new_user_hint = "请输入 是/否/新用户/老用户 或 yes/no"
        self.new_user_input.setText(self.new_user_hint)
        self.new_user_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 20px;
                background-color: rgba(255, 255, 255, 0.8);
                color: gray;
            }
        """)
        
        # 绑定新用户输入框事件
        self.new_user_input.focusInEvent = self.on_new_user_focus_in
        self.new_user_input.focusOutEvent = self.on_new_user_focus_out
        
        self.new_user_layout.addWidget(self.new_user_label)
        self.new_user_layout.addWidget(self.new_user_input)
        self.glass_layout.addLayout(self.new_user_layout)
        
        # 充值金额输入
        self.amount_layout = QHBoxLayout()
        self.amount_label = QLabel("充值金额（元）：")
        self.amount_label.setFont(QFont("微软雅黑", 12))
        self.amount_label.setStyleSheet("color: rgb(51, 51, 51);")
        
        self.amount_input = QLineEdit()
        self.amount_input.setFont(QFont("微软雅黑", 12))
        self.amount_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 20px;
                background-color: rgba(255, 255, 255, 0.8);
            }
        """)
        
        self.amount_layout.addWidget(self.amount_label)
        self.amount_layout.addWidget(self.amount_input)
        self.glass_layout.addLayout(self.amount_layout)
        
        # 充值按钮 - 使用简化版按钮
        self.recharge_btn = StyledButton("确认充值")
        self.recharge_btn.clicked.connect(self.calculate_recharge)
        
        # 按钮容器，用于居中显示
        self.btn_container = QFrame()
        self.btn_container.setStyleSheet("background-color: transparent;")
        self.btn_layout = QHBoxLayout(self.btn_container)
        self.btn_layout.setAlignment(Qt.AlignCenter)
        self.btn_layout.addWidget(self.recharge_btn)
        self.glass_layout.addWidget(self.btn_container)
        
        # 将毛玻璃框架添加到内容布局
        self.content_layout.addWidget(self.glass_frame)
        self.content_layout.setAlignment(Qt.AlignCenter)
        self.content_layout.setContentsMargins(20, 10, 20, 20)
    
    def on_new_user_focus_in(self, event):
        """当新用户输入框获得焦点时"""
        current_text = self.new_user_input.text()
        if current_text == self.new_user_hint:
            self.new_user_input.setText("")
            self.new_user_input.setStyleSheet("""
                QLineEdit {
                    padding: 8px 12px;
                    border: 1px solid #ddd;
                    border-radius: 20px;
                    background-color: rgba(255, 255, 255, 0.8);
                    color: #333333;
                }
            """)
        QLineEdit.focusInEvent(self.new_user_input, event)
        
    def on_new_user_focus_out(self, event):
        """当新用户输入框失去焦点时"""
        current_text = self.new_user_input.text().strip()
        if not current_text:  # 如果输入框为空
            self.new_user_input.setText(self.new_user_hint)
            self.new_user_input.setStyleSheet("""
                QLineEdit {
                    padding: 8px 12px;
                    border: 1px solid #ddd;
                    border-radius: 20px;
                    background-color: rgba(255, 255, 255, 0.8);
                    color: gray;
                }
            """)
        QLineEdit.focusOutEvent(self.new_user_input, event)
    
    def paintEvent(self, event):
        """绘制渐变背景"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 创建渐变背景
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor(200, 230, 201))  # #c8e6c9
        gradient.setColorAt(0.5, QColor(248, 187, 208))  # #f8bbd0
        gradient.setColorAt(1.0, QColor(187, 222, 251))  # #bbdefb
        painter.fillRect(self.rect(), QBrush(gradient))
        
        # 添加装饰性圆形
        circle_gradient1 = QRadialGradient(50, 50, 150)
        circle_gradient1.setColorAt(0, QColor(255, 235, 238, 100))  # #FFEBEE 半透明
        circle_gradient1.setColorAt(1, QColor(255, 235, 238, 0))
        painter.setBrush(QBrush(circle_gradient1))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-50, -50, 200, 200)
        
        circle_gradient2 = QRadialGradient(self.width() - 100, self.height() - 100, 150)
        circle_gradient2.setColorAt(0, QColor(243, 229, 245, 100))  # #F3E5F5 半透明
        circle_gradient2.setColorAt(1, QColor(243, 229, 245, 0))
        painter.setBrush(QBrush(circle_gradient2))
        painter.drawEllipse(self.width() - 200, self.height() - 200, 200, 200)
    
    def calculate_recharge(self):
        """计算充值金额和优惠"""
        try:
            # 获取输入值
            amount_text = self.amount_input.text().strip()
            new_user_text = self.new_user_input.text().strip().lower()
            
            # 检查是否为提示文字，如果是则视为未输入
            if new_user_text == self.new_user_hint:
                new_user_text = ""
            
            if not amount_text:
                QMessageBox.warning(self, "提示", "请输入充值金额")
                return
            
            # 验证金额输入是否合法（仅允许数字和正负号）
            if not re.fullmatch(r'^[+-]?\d+(\.\d+)?$', amount_text):
                QMessageBox.critical(self, "错误", "请输入正确的数额！")
                return
                
            amount = float(amount_text)
            
            if amount <= 0:
                QMessageBox.warning(self, "提示", "充值金额必须大于0")
                return
            
            # 新用户判断逻辑（支持中英文）
            is_new_user = False
            # 新用户关键词（中文+英文）
            new_user_patterns = re.compile(r'新|是|首|第一次|yes|y')
            # 老用户关键词（中文+英文）
            old_user_patterns = re.compile(r'不|否|老|不是|no|n')
            
            # 先检查是否有明确表示老用户的关键词
            if old_user_patterns.search(new_user_text):
                is_new_user = False
            # 再检查是否有明确表示新用户的关键词
            elif new_user_patterns.search(new_user_text):
                is_new_user = True
            # 如果没有明确输入，默认为老用户
            else:
                is_new_user = False
                QMessageBox.information(self, "提示", "未明确输入是否为新用户，将按老用户计算")
            
            # 计算基础赠送金额
            bonus = 0
            if amount >= 10000:
                bonus = 10000
            elif amount >= 5000:
                bonus = amount * 0.2 + 500
            elif amount >= 2000:
                bonus = amount * 0.18
            elif amount >= 1000:
                bonus = amount * 0.15
            
            # 新用户额外优惠（仅当金额小于10000时）
            new_user_bonus = 0
            if is_new_user and amount < 10000:
                total_before = amount + bonus
                new_user_bonus = total_before * 0.1
                bonus += new_user_bonus
            # 当新用户充值10000及以上时，显示提示
            elif is_new_user and amount >= 10000:
                QMessageBox.information(self, "提示", "新用户充值10000元及以上无额外赠送")
            
            # 最终结果
            total = amount + bonus
            
            # 显示结果弹窗
            result_msg = f"充值金额：{amount:.2f}元\n"
            result_msg += f"用户类型：{'新用户' if is_new_user else '老用户'}\n"
            result_msg += f"基础赠送：{bonus - new_user_bonus:.2f}元\n"
            if is_new_user and amount < 10000:
                result_msg += f"新用户额外赠送：{new_user_bonus:.2f}元\n"
            result_msg += f"总计到账：{total:.2f}元"
            
            QMessageBox.information(self, "充值成功", result_msg)
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"发生错误：{str(e)}")

if __name__ == "__main__":
    # 确保中文显示正常
    font = QFont("微软雅黑")
    
    app = QApplication(sys.argv)
    app.setFont(font)
    
    # 高DPI支持
    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QGuiApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    window = RechargeSystem()
    window.show()
    sys.exit(app.exec_())
    