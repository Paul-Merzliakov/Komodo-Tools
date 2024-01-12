#ui 
from maya import cmds
import import_animation_frames as anim
import Parent_constrain_bones_to_joints as cstrain
import mirror_keys as mir
import loop_animation_keys as loop

import os
from maya import OpenMayaUI as omui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

class FirstToolUI(QWidget):

    def __init__(self, parent=None):
        super(FirstToolUI, self).__init__(parent)

        self.setWindowFlags(Qt.Window)

        # Set the object name     
        self.setObjectName('FirstToolUI_uniqueId')

        # Customize some window values
        self.setWindowTitle('Komodo Tools')
        self.setGeometry(50, 50, 500, 500)
        #global variables 
        #import animation global vars
        self.file_path_hind = ''
        self.file_path_fore = ''
        #loop Keys global vars
        self.loop_mode = 0
        self.loop_value = 1
        self.loop_endframe = 6
        #Add widgets to your window
        self.build_ui()
        self.connect_ui()


    def build_ui(self):
        layout = QVBoxLayout()
        #          ~~~DENOISE UI~~~
        
        #  **Denoise widgets**
        # denoise source file widgets
        denoise_f_mot_label = QLabel("Select .mot mocap source files")
        self.denoise_f_hind_mot_path = QLineEdit()
        self.configure_QLineedit(self.denoise_f_hind_mot_path, "Browse hindlimb motfile...")
        self.denoise_f_fore_mot_path = QLineEdit()
        self.configure_QLineedit(self.denoise_f_fore_mot_path, "Browse forelimb motfile...")
        self.denoise_f_hind_mot_btn = QPushButton(text = "open", parent = self)
        self.denoise_f_fore_mot_btn = QPushButton(text = "open", parent = self)
        # denoise smoothed file widgets
        denoise_f_csv_label = QLabel( "set denoised .csv file locations" )
        self.denoise_f_hind_csv_path = QLineEdit()
        self.configure_QLineedit(self.denoise_f_hind_csv_path, "Set hindlimb filename/location")
        self.denoise_f_fore_csv_path = QLineEdit()
        self.configure_QLineedit(self.denoise_f_fore_csv_path, "Set forelimb filename/location")
        self.denoise_f_hind_csv_btn = QPushButton(text = "save as", parent = self)
        self.denoise_f_fore_csv_btn = QPushButton(text = "save as", parent = self)
        #denoise button    
        self.denoise_f_btn = QPushButton(text = "create denoised file", parent = self )
          #  **Denoise Layout**
        denoise_f_grp = QGroupBox("Clean .mot mocapfiles)")
        denoise_f_layout = QVBoxLayout()
        denoise_f_motpath_layout = QGridLayout()
        denoise_f_csvpath_layout = QGridLayout()
        denoise_f_motpath_layout.addWidget(self.denoise_f_hind_mot_path,0,0)
        denoise_f_motpath_layout.addWidget(self.denoise_f_hind_mot_btn, 0,1)
        denoise_f_motpath_layout.addWidget(self.denoise_f_fore_mot_path,1,0)
        denoise_f_motpath_layout.addWidget(self.denoise_f_fore_mot_btn,1,1)

        denoise_f_csvpath_layout.addWidget(self.denoise_f_hind_csv_path,0,0)
        denoise_f_csvpath_layout.addWidget(self.denoise_f_hind_csv_btn,0,1)
        denoise_f_csvpath_layout.addWidget(self.denoise_f_fore_csv_path,1,0)
        denoise_f_csvpath_layout.addWidget(self.denoise_f_fore_csv_btn, 1,1)

        denoise_f_layout.addWidget(denoise_f_mot_label)
        denoise_f_layout.addLayout(denoise_f_motpath_layout)
        denoise_f_layout.addWidget(denoise_f_csv_label)
        denoise_f_layout.addLayout(denoise_f_csvpath_layout)
        denoise_f_layout.addWidget(self.denoise_f_btn)
        denoise_f_grp.setLayout(denoise_f_layout)

    
        

    

        #constrain_button_widget
        self.constrain_btn = QPushButton(text = "Constrain joints to Skeleton Geometry", parent = self)
        #Import animation Widgets
        self.use_denoise_fpath = QCheckBox(text = "Use Denoised file" , parent = self)
        self.import_anim_btn = QPushButton( text = "Import Animation", parent = self)
        self.import_anim_path = QLineEdit()
        self.configure_QLineedit(self.import_anim_path,"Browse hindlimb file...")
        self.sel_anim_path = QPushButton(text = "open", parent = self)
        self.import_anim_path2 = QLineEdit()
        self.configure_QLineedit(self.import_anim_path2, "Browse forelimb file...")
        self.sel_anim_path2 = QPushButton(text = "open", parent = self)
        
        import_anim_grp_box = QGroupBox("Import Animation from CSV")
        import_anim_layout = QVBoxLayout()
        import_anim_path_layout = QGridLayout()
        import_anim_btn_layout = QHBoxLayout()
        import_anim_layout.addWidget(self.use_denoise_fpath)
        import_anim_layout.addLayout(import_anim_path_layout)
        import_anim_layout.addLayout(import_anim_btn_layout)
        import_anim_grp_box.setLayout(import_anim_layout)
        #adding widgets to grid layout (import_amin_layout)
        #import_anim_path_layout.addRow( self.import_anim_path, self.sel_anim_path)
        #import_anim_path_layout.addRow( self.import_anim_path2,self.sel_anim_path2)
        import_anim_path_layout.addWidget( self.import_anim_path, 0,0)
        import_anim_path_layout.addWidget( self.sel_anim_path, 0,1)
        import_anim_path_layout.addWidget( self.import_anim_path2, 1,0)
        import_anim_path_layout.addWidget(self.sel_anim_path2,1,1)
        #import_anim_path_layout.addRow( self.sel_anim_path,self.import_anim_path)
        #import_anim_path_layout.addRow( self.sel_anim_path2, self.import_anim_path2)
        import_anim_btn_layout.addWidget(self.import_anim_btn)
      # mirror widgets
        self.mirror_keys_btn = QPushButton( text = "Mirror Keys", parent = self)
      # loopwidgets
        
        loop_grp_box = QGroupBox("Loop Animation")
        loop_grp_layout = QFormLayout()
        loop_mode_label = QLabel(text = "Looping mode")
        self.loop_mode_list = QListWidget()
        self.loop_mode_list.insertItem(0,"By count")
        self.loop_mode_list.insertItem(1,"By endpoint")
        self.loop_mode_list.setMaximumHeight(70)
        self.loop_mode_list.setCurrentRow(0)
        self.stack1 = QWidget()
        self.stack2 = QWidget()

        only_int = QIntValidator()
        self.loop_endframe_input = QLineEdit()
        loop_endframe_label = QLabel(text = "Animation endframe")
        self.loop_endframe_input.setValidator(only_int)
       
        #self.loop_slider_layout = QHBoxLayout()
        #self.loop_endpoint_layout = QFormLayout()

        self.addloop_stacks(self.stack1)
        self.addloop_stacks(self.stack2)
        self.loop_keys_btn = QPushButton( text = "loop keys", parent = self)

        self.master_stack = QStackedWidget(self)
        self.master_stack.addWidget(self.stack1)
        self.master_stack.addWidget(self.stack2)
        loop_grp_layout.addRow(loop_mode_label,self.loop_mode_list)
        loop_grp_layout.addRow(loop_endframe_label,self.loop_endframe_input)
        loop_grp_layout.addWidget(self.master_stack)
        loop_grp_layout.addRow(self.loop_keys_btn)
        loop_grp_box.setLayout(loop_grp_layout)
        
        
        
      #Appending Widgets to main layout
        layout.addWidget(denoise_f_grp)
        layout.addWidget(self.constrain_btn)
        layout.addWidget(import_anim_grp_box)
        layout.addWidget(self.mirror_keys_btn)
        layout.addWidget(loop_grp_box)
        
        self.setLayout(layout)
    def configure_QLineedit(self,widget: QLineEdit,pholder_text : str) -> None:
        widget.setReadOnly(True)
        widget.setPlaceholderText(pholder_text)
        widget.setMinimumWidth(250)

    def addloop_stacks(self,stack: QWidget):
        
        #first row - input final animation frame
        if stack == self.stack1:
            
            #creating widgets
            self.loop_count_slider = QSlider(Qt.Horizontal, self)
            self.loop_count_slider.setTickInterval(1)
            self.loop_count_slider.setMinimum(1)
            self.loop_count_slider.setMaximum(10)
            self.loop_count_slider.setMinimumWidth(130)
            self.loop_count_num = QLineEdit()
            self.loop_count_num.setReadOnly(True)
            self.loop_count_num.setPlaceholderText("0")
            self.loop_count_slider.setTickPosition(QSlider.TicksAbove)#1 is the enum value to set ticks on both sides
            loop_count_label = QLabel("Number of Times to loop animation")
            #configuring layout
            layout =  QHBoxLayout()
            layout.addWidget(loop_count_label)
            layout.addWidget(self.loop_count_slider)
            layout.addWidget(self.loop_count_num)
            #layout.addRow(loop_count_label,self.loop_count_slider)
            self.stack1.setLayout(layout)
        else:
            layout =  QFormLayout()
            self.loop_endpoint_input = QLineEdit()
            only_int = QIntValidator()
            loop_endpoint_input_txt = QLabel(text = "Looping endpoint")
            self.loop_endpoint_input.setValidator(only_int)
            layout.addRow(loop_endpoint_input_txt,self.loop_endpoint_input)
            self.stack2.setLayout(layout)

    def connect_ui(self):
        self.use_denoise_fpath.stateChanged.connect(self.update_import_anim_file)
        self.constrain_btn.clicked.connect(cstrain.constrain_bones )
        self.sel_anim_path.clicked.connect(lambda: self.get_anim_data(True))
        self.sel_anim_path2.clicked.connect(lambda: self.get_anim_data(False))
        self.import_anim_btn.clicked.connect(lambda: anim.create_animation(self.file_path_hind,self.file_path_fore))
        self.mirror_keys_btn.clicked.connect(mir.mirror)
        self.loop_mode_list.currentRowChanged.connect(self.update_loop_mode )
        self.loop_mode_list.currentRowChanged.connect(self.set_loop_stack_display)
        self.loop_count_slider.valueChanged.connect(lambda: self.set_loop_count_display(str(self.loop_count_slider.value())))
        self.loop_count_slider.valueChanged.connect(lambda: self.update_loop_val(self.loop_count_slider.value()))
        self.loop_endpoint_input.textChanged.connect(lambda: self.update_loop_val(int(self.loop_endpoint_input.text())))
        self.loop_endframe_input.textChanged.connect(lambda: self.update_loop_endframe(self.loop_endframe_input.text()))
        self.loop_keys_btn.clicked.connect(lambda: loop.loop_keys(self.loop_mode,self.loop_value,self.loop_endframe))

    def set_loop_stack_display(self,i):
        self.master_stack.setCurrentIndex(i)
    def update_import_anim_file(self):
        if self.use_denoise_fpath.isChecked():
            self.sel_anim_path.setDisabled(True)
            self.sel_anim_path2.setDisabled(True)
        else:
            self.sel_anim_path.setDisabled(False)
            self.sel_anim_path2.setDisabled(False)


    def set_loop_count_display(self,i):
        self.loop_count_num.setText(i)
    
    #update functions for Global variables
    def update_loop_mode(self, i): 
        self.loop_mode = i
   
    def update_loop_val(self,i):
        self.loop_value = i
    def update_loop_endframe(self,i):
        self.loop_endframe = int(i) 

    def get_anim_data(self,isHind: bool):
        filter = "*.csv"
        cwd = os.getcwd()
        if isHind == True:
            self.file_path_hind = QFileDialog.getOpenFileName(self,"Open File",r"C:\Users\paulm\Documents\maya\2022\scripts\Komodo_dragon_scripts",filter )[0]
            self.import_anim_path.setText(self.file_path_hind)
        else:
            self.file_path_fore = QFileDialog.getOpenFileName(self,"Open File",r"C:\Users\paulm\Documents\maya\2022\scripts\Komodo_dragon_scripts",filter )[0]
            self.import_anim_path2.setText(self.file_path_fore)
        #print(self.file_path_hind)
    def set_anim_data(self,isHind: bool):
        pass


def get_main_window():
    """Get the maya window pointer to parent this tool under."""
    ptr = omui.MQtUtil.mainWindow()
    # for Py3 use int() , for Py2 use long() , more info: https://docs.python.org/3/whatsnew/3.0.html#integers
    maya_window = wrapInstance(int(ptr), QWidget)
    return maya_window

# Get Maya's main window to parent to
maya_window = get_main_window()
tool = FirstToolUI(maya_window)
tool.show()
