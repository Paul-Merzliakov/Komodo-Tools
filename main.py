#ui 
import import_animation_frames as anim
import Parent_constrain_bones_to_joints as cstrain
import mirror_keys as mir
import loop_animation_keys as loop
import process_mot_file_data as denoise

import os
from maya import OpenMayaUI as omui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

class KomodoToolsUI(QWidget):

    def __init__(self, parent=None):
        super(KomodoToolsUI, self).__init__(parent)
        self.setWindowFlags(Qt.Window)
        # Set the object name     
        self.setObjectName('FirstToolUI_uniqueId')
        # Customize some window values
        self.setWindowTitle('Komodo Tools')
        self.setGeometry(50, 50, 800, 800)
        #  ~~ GLOBAL CLASS VARS ~~  
        #-denoise_global vars. 
        self.denoise_hind_metadata = denoise.DenoiseFileData() #contains, file paths, channels, 
        self.denoise_fore_metadata = denoise.DenoiseFileData()
        #-import animation global vars-
        self.file_path_hind_var = ''
        self.file_path_fore_var = ''
        #-loop Keys global vars-
        self.loop_mode = 0
        self.loop_value = 1
        self.loop_endframe = 6
        #Add widgets to your window
        self.build_ui()
        self.connect_ui()


    def build_ui(self):
        layout = QVBoxLayout()
        #     ~~~DENOISE UI~~~
        #  -Denoise widgets-
        # denoise source file widgets
        self.denoise_f_mot_label = QLabel("Select .mot mocap source files")
        self.denoise_f_hind_mot_path = QLineEdit()
        self.configure_QLineEdit_widgets(self.denoise_f_hind_mot_path, "Browse hindlimb motfile...")
        self.denoise_f_fore_mot_path = QLineEdit()
        self.configure_QLineEdit_widgets(self.denoise_f_fore_mot_path, "Browse forelimb motfile...")
        self.denoise_f_hind_mot_btn = QPushButton(text = "open", parent = self)
        self.denoise_f_fore_mot_btn = QPushButton(text = "open", parent = self)
        self.denoise_channels_hind_listw= QListWidget()
        self.denoise_channels_hind_listw.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.denoise_channels_fore_listw = QListWidget()
        self.denoise_channels_fore_listw.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # denoise smoothed file widgets
        self.denoise_f_csv_label = QLabel( "set denoised .csv file locations" )
        self.denoise_f_hind_csv_path = QLineEdit()
        self.configure_QLineEdit_widgets(self.denoise_f_hind_csv_path, "Set hindlimb filename/location")
        self.denoise_f_fore_csv_path = QLineEdit()
        self.configure_QLineEdit_widgets(self.denoise_f_fore_csv_path, "Set forelimb filename/location")
        self.denoise_f_hind_csv_btn = QPushButton(text = "save as", parent = self)
        self.denoise_f_fore_csv_btn = QPushButton(text = "save as", parent = self)
        #denoise button    
        self.denoise_f_btn = QPushButton(text = "create denoised file", parent = self )
          # -Denoise Layout-
        denoise_f_grp = QGroupBox("Clean .mot mocapfiles)")
        denoise_f_layout = QVBoxLayout()
        denoise_f_motpath_layout = QGridLayout()
        denoise_f_csvpath_layout = QGridLayout()
        #denoise_f_hind_channel_list_layout = QVBoxLayout()
        #denoise_f_fore_channel_list_layout = QVBoxLayout()

        #denoise_f_hind_channel_list_layout.addWidget(self.denoise_channels_hind_listw)
        #denoise_f_fore_channel_list_layout.addWidget(self.denoise_channels_fore_listw)

        denoise_f_motpath_layout.addWidget(self.denoise_f_hind_mot_path,0,0)
        denoise_f_motpath_layout.addWidget(self.denoise_f_hind_mot_btn, 0,1)
        denoise_f_motpath_layout.addWidget(self.denoise_channels_hind_listw,1,0)
        denoise_f_motpath_layout.addWidget(self.denoise_f_fore_mot_path,2,0)
        denoise_f_motpath_layout.addWidget(self.denoise_f_fore_mot_btn,2,1)
        denoise_f_motpath_layout.addWidget(self.denoise_channels_fore_listw,3,0)

        denoise_f_csvpath_layout.addWidget(self.denoise_f_hind_csv_path,0,0)
        denoise_f_csvpath_layout.addWidget(self.denoise_f_hind_csv_btn,0,1)
        denoise_f_csvpath_layout.addWidget(self.denoise_f_fore_csv_path,1,0)
        denoise_f_csvpath_layout.addWidget(self.denoise_f_fore_csv_btn, 1,1)

        denoise_f_layout.addWidget(self.denoise_f_mot_label)
        denoise_f_layout.addLayout(denoise_f_motpath_layout)
        denoise_f_layout.addWidget(self.denoise_f_csv_label)
        denoise_f_layout.addLayout(denoise_f_csvpath_layout)
        denoise_f_layout.addWidget(self.denoise_f_btn)
        denoise_f_grp.setLayout(denoise_f_layout)

        #constrain_button_widget
        self.constrain_btn = QPushButton(text = "Constrain joints to Skeleton Geometry", parent = self)
        #Import animation Widgets
        self.use_denoise_fpath = QCheckBox(text = "Use Denoised file" , parent = self)
        self.import_anim_btn = QPushButton( text = "Import Animation", parent = self)
        self.import_anim_hind_path = QLineEdit()
        self.configure_QLineEdit_widgets(self.import_anim_hind_path,"Browse hindlimb file...")
        self.importamin_open_hind_btn = QPushButton(text = "open", parent = self)
        self.import_anim_fore_path = QLineEdit()
        self.configure_QLineEdit_widgets(self.import_anim_fore_path, "Browse forelimb file...")
        self.importanim_open_fore_btn = QPushButton(text = "open", parent = self)
        
        import_anim_grp_box = QGroupBox("Import Animation from CSV")
        import_anim_layout = QVBoxLayout()
        import_anim_path_layout = QGridLayout()
        
        import_anim_layout.addWidget(self.use_denoise_fpath)
        import_anim_layout.addLayout(import_anim_path_layout)
        import_anim_layout.addWidget(self.import_anim_btn)
        import_anim_grp_box.setLayout(import_anim_layout)
        import_anim_path_layout.addWidget( self.import_anim_hind_path, 0,0)
        import_anim_path_layout.addWidget( self.importamin_open_hind_btn, 0,1)
        import_anim_path_layout.addWidget( self.import_anim_fore_path, 1,0)
        import_anim_path_layout.addWidget(self.importanim_open_fore_btn,1,1)
        
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

    def setLayouts(self):
        

    def connect_ui(self):
        self.use_denoise_fpath.stateChanged.connect(self.update_import_anim_ui_status)
        self.constrain_btn.clicked.connect(cstrain.constrain_bones )
        self.import_anim_btn.clicked.connect(self.import_animation_wrapper)
        self.mirror_keys_btn.clicked.connect(mir.mirror)
        self.loop_mode_list.currentRowChanged.connect(self.update_loop_mode )
        self.loop_mode_list.currentRowChanged.connect(self.set_loop_stack_display)
        self.loop_count_slider.valueChanged.connect(lambda: self.set_loop_count_display(str(self.loop_count_slider.value())))
        self.loop_count_slider.valueChanged.connect(lambda: self.update_loop_val(self.loop_count_slider.value()))
        self.loop_endpoint_input.textChanged.connect(lambda: self.update_loop_val(int(self.loop_endpoint_input.text())))
        self.loop_endframe_input.textChanged.connect(lambda: self.update_loop_endframe(self.loop_endframe_input.text()))
        self.loop_keys_btn.clicked.connect(lambda: loop.loop_keys(self.loop_mode,self.loop_value,self.loop_endframe))
        self.denoise_f_hind_csv_btn.clicked.connect(lambda: self.get_denoise_csv_filepath(True))
        self.denoise_f_fore_csv_btn.clicked.connect(lambda: self.get_denoise_csv_filepath(False))
        self.denoise_f_hind_mot_btn.clicked.connect(lambda: self.get_mot_metadata(True))
        self.denoise_f_fore_mot_btn.clicked.connect(lambda: self.get_mot_metadata(False))
        self.importamin_open_hind_btn.clicked.connect(lambda: self.get_csv_filepath(True))
        self.importanim_open_fore_btn.clicked.connect(lambda: self.get_csv_filepath(False))
        self.denoise_f_btn.clicked.connect(lambda: self.denoise_hind_metadata.generate_csv([self.denoise_channels_hind_listw.row(item) for item in self.denoise_channels_hind_listw.selectedItems()]))
        self.denoise_f_btn.clicked.connect(lambda: self.denoise_fore_metadata.generate_csv([self.denoise_channels_fore_listw.row(item) for item in self.denoise_channels_fore_listw.selectedItems()]))
        self.denoise_f_hind_mot_path.textChanged.connect(lambda: self.add_to_denoise_listWidget(self.denoise_hind_metadata.animation_channels,True))
        self.denoise_f_fore_mot_path.textChanged.connect(lambda: self.add_to_denoise_listWidget(self.denoise_fore_metadata.animation_channels,False))




    def configure_QLineEdit_widgets(self,widget: QLineEdit,pholder_text : str) -> None:
        widget.setReadOnly(True)
        widget.setPlaceholderText(pholder_text)
        widget.setMinimumWidth(250)

    def add_to_denoise_listWidget(self, name_list: list,ishind: bool):
        if  ishind == True:
            for each in name_list:
                self.denoise_channels_hind_listw.addItem(each)
        else:
            for each in name_list:
                self.denoise_channels_fore_listw.addItem(each)
        #pre selecting the channels I want from these mot files by default for ease of testing
        self.set_select_denoise_widgets([0,1,2,3,4,5,13,14,15,16,17,18,19],True)
        self.set_select_denoise_widgets([0,1,2,13,14,15,16,17,18,19],False)

    def set_select_denoise_widgets(self,list_of_indexs: list, hind: bool):
        
        if hind == True:
            for i in list_of_indexs:
                self.denoise_channels_hind_listw.setItemSelected(self.denoise_channels_hind_listw.item(i),True)
        else:
            for i in list_of_indexs:
                self.denoise_channels_fore_listw.setItemSelected(self.denoise_channels_fore_listw.item(i), True)

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

    
    
    
    def set_loop_stack_display(self,i):
        self.master_stack.setCurrentIndex(i)

    def update_import_anim_ui_status(self):
        if self.use_denoise_fpath.isChecked():
            self.importamin_open_hind_btn.setDisabled(True)
            self.importanim_open_fore_btn.setDisabled(True)
        else:
            self.importamin_open_hind_btn.setDisabled(False)
            self.importanim_open_fore_btn.setDisabled(False)

    def import_animation_wrapper(self):
        if self.use_denoise_fpath.isChecked() == True:
            anim.create_animation(self.denoise_hind_metadata.csv_fpath,self.denoise_fore_metadata)
        else:
            anim.create_animation(self.file_path_hind_var,self.file_path_fore_var)

    def set_loop_count_display(self,i):
        self.loop_count_num.setText(i)
    
    #update functions for Global variables
    def update_loop_mode(self, i): 
        self.loop_mode = i
   
    def update_loop_val(self,i):
        self.loop_value = i
    def update_loop_endframe(self,i):
        self.loop_endframe = int(i) 

    def get_csv_filepath(self,isHind: bool):
        filter = "*.csv"
        if isHind == True:
            self.denoise_hind_metadata.csv_fpath = QFileDialog.getOpenFileName(self,"Open File",r"C:\Users\paulm\Documents\maya\2022\scripts\Komodo-Tools",filter )[0]
            self.import_anim_hind_path.setText(self.denoise_hind_metadata.csv_fpath)
        else:
            self.denoise_fore_metadata.csv_fpath = QFileDialog.getOpenFileName(self,"Open File",r"C:\Users\paulm\Documents\maya\2022\scripts\Komodo-Tools",filter )[0]
            self.import_anim_fore_path.setText(self.denoise_fore_metadata.csv_fpath)

    def get_mot_metadata(self,isHind: bool):
        filter = "*.mot"
        if isHind == True:
            self.denoise_hind_metadata.mot_fpath = QFileDialog.getOpenFileName(self,"Open File",r"C:\Users\paulm\Documents\maya\2022\scripts\Komodo-Tools",filter )[0]
            self.denoise_hind_metadata.get_anim_channels()
            self.denoise_f_hind_mot_path.setText(self.denoise_hind_metadata.mot_fpath)
        else:
            self.denoise_fore_metadata.mot_fpath = QFileDialog.getOpenFileName(self,"Open File",r"C:\Users\paulm\Documents\maya\2022\scripts\Komodo-Tools",filter )[0]
            self.denoise_fore_metadata.ishind = False
            self.denoise_fore_metadata.get_anim_channels()
            self.denoise_f_fore_mot_path.setText(self.denoise_fore_metadata.mot_fpath)
        #print(self.file_path_hind)


    def get_denoise_csv_filepath(self,isHind: bool):
        f_filter = "*.csv"
        if isHind == True: 
            self.denoise_hind_metadata.csv_fpath = QFileDialog.getSaveFileName(self,"save file as",r"C:\Users\paulm\Documents\maya\2022\scripts\Komodo-Tools",f_filter) [0]
            self.denoise_f_hind_csv_path.setText(self.denoise_hind_metadata.csv_fpath)
        else:
            self.denoise_fore_metadata.csv_fpath = QFileDialog.getSaveFileName(self,"save file as",r"C:\Users\paulm\Documents\maya\2022\scripts\Komodo-Tools",f_filter) [0]
            self.denoise_f_fore_csv_path.setText(self.denoise_fore_metadata.csv_fpath)
    
    


def get_main_window():
    """Get the maya window pointer to parent this tool under."""
    ptr = omui.MQtUtil.mainWindow()
    # for Py3 use int() , for Py2 use long() , more info: https://docs.python.org/3/whatsnew/3.0.html#integers
    maya_window = wrapInstance(int(ptr), QWidget)
    return maya_window

# Get Maya's main window to parent to
maya_window = get_main_window()
tool = KomodoToolsUI(maya_window)
tool.show()
