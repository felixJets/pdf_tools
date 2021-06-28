
### This file provides the CSS-Styles for all the GUI-Widgets


StyleSheet_Select = '''
        QPushButton {
            background-color: #009900;
            color: #ffffff;
            font-size: 15px;
            font-weight: bold;
            font-family: Georgia;
        }
        QPushButton::hover {
            background-color: #00dd00;
            color: #ffffff;
        }
        '''


StyleSheet_Clear = '''
        QPushButton {
            background-color: #990000;
            color: #ffffff;
            font-size: 15px;
            font-weight: bold;
            font-family: Georgia;
        }
        QPushButton::hover {
            background-color: #dd0000;
            color: #ffffff;
        }
        '''


StyleSheet_Remove = '''
        QPushButton {
            background-color: #cc7a00;
            color: #ffffff;
            font-size: 15px;
            font-weight: bold;
            font-family: Georgia;
        }
        QPushButton::hover {
            background-color: #ffa31a;
            color: #ffffff;
        }
        '''

StyleSheet_Combine = '''
        QPushButton {
            background-color: #000099;
            color: #ffffff;
            font-size: 15px;
            font-weight: bold;
            font-family: Georgia;
        }
        QPushButton::hover {
            background-color: #0000dd;
            color: #ffffff;
        }
        '''

StyleSheet_Encrypt = '''
        QPushButton {
            background-color: #bbbbbb;
            color: #ffffff;
            font-size: 15px;
            font-weight: bold;
            font-family: Georgia;
        }
        QPushButton::hover {
            background-color: #eeeeee;
            color: #000000;
        }
        '''


StyleSheet_QListWidget = '''
        QListWidget::item { 
            border-bottom: 2px solid black;
            background-color: #eeeeff;
        } 
         QListWidget::item:selected {
            background-color: #ffffff; 
            color: #aaaaaa
        }
        QListWidget::item:hover {
            background-color: #eeeeee; 
        }
        QListWidget {
            background-color: #eeffee
        }
        '''

StyleSheet_Main = '''
        background-color: #9999bb
'''