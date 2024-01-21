#ui 
import import_animation_frames as anim
import Parent_constrain_bones_to_joints as cstrain
import mirror_keys as mir
import loop_animation_keys as loop
import process_mot_file_data as denoise

import os
import sys
from maya import OpenMayaUI as omui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
global Komodo_UI

class KomodoToolsUI(QWidget):

    def __init__(self, parent=None):
        super(KomodoToolsUI, self).__init__(parent)
        self.setWindowFlags(Qt.Window)     
        self.setObjectName('KomodoTools_uniqueId')
        self.setWindowTitle('Komodo Tools')
        self.setGeometry(50, 50, 800, 800)
        

        #  ~~ GLOBAL CLASS VARS ~~  
        self.folder_directory = [x for x in sys.path if x.count("Komodo-Tools") > 0 ][0]
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
        
        self.build_widgets()
        self.set_layouts()
        self.connect_ui()



    def build_widgets(self):

        # ~~ DENOISE WIDGETS ~~
        self.denoise_mot_label = QLabel("Select .mot mocap source files")
        self.denoise_hind_mot_path = QLineEdit()
        self.configure_QLineEdit_widgets(self.denoise_hind_mot_path, "Browse hindlimb motfile...")
        self.denoise_fore_mot_path = QLineEdit()
        self.configure_QLineEdit_widgets(self.denoise_fore_mot_path, "Browse forelimb motfile...")
        self.denoise_hind_mot_btn = QPushButton(text = "open", parent = self)
        self.denoise_fore_mot_btn = QPushButton(text = "open", parent = self)
        self.denoise_channels_hind_listw= QListWidget()
        self.denoise_channels_hind_listw.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.denoise_channels_fore_listw = QListWidget()
        self.denoise_channels_fore_listw.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.denoise_csv_label = QLabel( "set denoised .csv file locations" )
        self.denoise_hind_csv_path = QLineEdit()
        self.configure_QLineEdit_widgets(self.denoise_hind_csv_path, "Set hindlimb filename/location")
        self.denoise_fore_csv_path = QLineEdit()
        self.configure_QLineEdit_widgets(self.denoise_fore_csv_path, "Set forelimb filename/location")
        self.denoise_hind_csv_btn = QPushButton(text = "save as", parent = self)
        self.denoise_fore_csv_btn = QPushButton(text = "save as", parent = self)
        self.denoise_main_btn = QPushButton(text = "create denoised file", parent = self )

        # ~~ CONSTRAIN WIDGETS ~~
        self.constrain_btn = QPushButton(text = "Constrain joints to Skeleton Geometry", parent = self)

        # ~~ IMPORT ANIMATINO WIDGETS ~~
        self.use_denoise_fpath = QCheckBox(text = "Use Denoised file" , parent = self)
        self.import_anim_btn = QPushButton( text = "Import Animation", parent = self)
        self.import_anim_hind_path = QLineEdit()
        self.configure_QLineEdit_widgets(self.import_anim_hind_path,"Browse hindlimb file...")
        self.importamin_open_hind_btn = QPushButton(text = "open", parent = self)
        self.import_anim_fore_path = QLineEdit()
        self.configure_QLineEdit_widgets(self.import_anim_fore_path, "Browse forelimb file...")
        self.importanim_open_fore_btn = QPushButton(text = "open", parent = self)
    
       # ~~ MIRROR WIDGETS ~~
        self.mirror_keys_btn = QPushButton( text = "Mirror Keys", parent = self)

       # ~~ LOOP WIDGETS ~~ 
        self.loop_mode_label = QLabel(text = "Looping mode")
        self.loop_mode_list = QListWidget()
        self.loop_mode_list.insertItem(0,"By count")
        self.loop_mode_list.insertItem(1,"By endpoint")
        self.loop_mode_list.setMaximumHeight(70)
        self.loop_mode_list.setCurrentRow(0)
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        only_int = QIntValidator()
        self.loop_endframe_input = QLineEdit()
        self.loop_endframe_label = QLabel(text = "Animation endframe")
        self.loop_endframe_input.setValidator(only_int)
        self.addloop_stacks(self.stack1)
        self.addloop_stacks(self.stack2)
        self.loop_keys_btn = QPushButton( text = "loop keys", parent = self)
        self.master_stack = QStackedWidget(self)
        self.master_stack.addWidget(self.stack1)
        self.master_stack.addWidget(self.stack2)
      

    def set_layouts(self):

        # ~~ DENOISE LAYOUT ~~
        denoise_f_layout = QVBoxLayout()
        denoise_f_motpath_layout = QGridLayout()
        denoise_f_csvpath_layout = QGridLayout()
        denoise_f_motpath_layout.addWidget(self.denoise_hind_mot_path,0,0)
        denoise_f_motpath_layout.addWidget(self.denoise_hind_mot_btn, 0,1)
        denoise_f_motpath_layout.addWidget(self.denoise_channels_hind_listw,1,0)
        denoise_f_motpath_layout.addWidget(self.denoise_fore_mot_path,2,0)
        denoise_f_motpath_layout.addWidget(self.denoise_fore_mot_btn,2,1)
        denoise_f_motpath_layout.addWidget(self.denoise_channels_fore_listw,3,0)
        denoise_f_csvpath_layout.addWidget(self.denoise_hind_csv_path,0,0)
        denoise_f_csvpath_layout.addWidget(self.denoise_hind_csv_btn,0,1)
        denoise_f_csvpath_layout.addWidget(self.denoise_fore_csv_path,1,0)
        denoise_f_csvpath_layout.addWidget(self.denoise_fore_csv_btn, 1,1)
        denoise_f_layout.addWidget(self.denoise_mot_label)
        denoise_f_layout.addLayout(denoise_f_motpath_layout)
        denoise_f_layout.addWidget(self.denoise_csv_label)
        denoise_f_layout.addLayout(denoise_f_csvpath_layout)
        denoise_f_layout.addWidget(self.denoise_main_btn)
        denoise_f_grp_box = QGroupBox("Clean .mot mocapfiles)")
        denoise_f_grp_box.setLayout(denoise_f_layout)

        # ~~ IMPORT ANIM LAYOUT ~~ 
        import_anim_layout = QVBoxLayout()
        import_anim_path_layout = QGridLayout()
        import_anim_layout.addWidget(self.use_denoise_fpath)
        import_anim_layout.addLayout(import_anim_path_layout)
        import_anim_layout.addWidget(self.import_anim_btn)
        import_anim_path_layout.addWidget( self.import_anim_hind_path, 0,0)
        import_anim_path_layout.addWidget( self.importamin_open_hind_btn, 0,1)
        import_anim_path_layout.addWidget( self.import_anim_fore_path, 1,0)
        import_anim_path_layout.addWidget(self.importanim_open_fore_btn,1,1)
        import_anim_grp_box = QGroupBox("Import Animation from CSV")
        import_anim_grp_box.setLayout(import_anim_layout)

        # ~~ LOOP LAYOUT ~~
        loop_grp_layout = QFormLayout()
        loop_grp_layout.addRow(self.loop_mode_label,self.loop_mode_list)
        loop_grp_layout.addRow(self.loop_endframe_label,self.loop_endframe_input)
        loop_grp_layout.addWidget(self.master_stack)
        loop_grp_layout.addRow(self.loop_keys_btn)
        loop_grp_box = QGroupBox("Loop Animation")
        loop_grp_box.setLayout(loop_grp_layout)
        
      # ~~ MASTER LAYOUT ~~
        master_layout = QVBoxLayout()
        master_layout.addWidget(denoise_f_grp_box)
        master_layout.addWidget(self.constrain_btn)
        master_layout.addWidget(import_anim_grp_box)
        master_layout.addWidget(self.mirror_keys_btn)
        master_layout.addWidget(loop_grp_box)
        self.setLayout(master_layout)

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
        self.denoise_hind_csv_btn.clicked.connect(lambda: self.get_denoise_csv_filepath(True))
        self.denoise_fore_csv_btn.clicked.connect(lambda: self.get_denoise_csv_filepath(False))
        self.denoise_hind_mot_btn.clicked.connect(lambda: self.get_mot_metadata(True))
        self.denoise_fore_mot_btn.clicked.connect(lambda: self.get_mot_metadata(False))
        self.importamin_open_hind_btn.clicked.connect(lambda: self.get_csv_filepath(True))
        self.importanim_open_fore_btn.clicked.connect(lambda: self.get_csv_filepath(False))
        self.denoise_main_btn.clicked.connect(lambda: self.denoise_hind_metadata.generate_csv([self.denoise_channels_hind_listw.row(item) for item in self.denoise_channels_hind_listw.selectedItems()]))
        self.denoise_main_btn.clicked.connect(lambda: self.denoise_fore_metadata.generate_csv([self.denoise_channels_fore_listw.row(item) for item in self.denoise_channels_fore_listw.selectedItems()]))
        self.denoise_hind_mot_path.textChanged.connect(lambda: self.add_to_denoise_listWidget(self.denoise_hind_metadata,self.denoise_channels_hind_listw))
        self.denoise_fore_mot_path.textChanged.connect(lambda: self.add_to_denoise_listWidget(self.denoise_fore_metadata,self.denoise_channels_fore_listw))

    def configure_QLineEdit_widgets(self,widget: QLineEdit,pholder_text : str) -> None:
        widget.setReadOnly(True)
        widget.setPlaceholderText(pholder_text)
        widget.setMinimumWidth(250)

    def add_to_denoise_listWidget(self, mot_metadata: denoise.DenoiseFileData, list_widget: QListWidget):
        self.delete_existing_denoise_list_items(list_widget)
        mot_channels_list = mot_metadata.animation_channels
        default_sel_channel_indexs = mot_metadata.default_sel_indexes
        for each in mot_channels_list:
            list_widget.addItem(each)
        #default preselection item indexes for the mot files I'm using 
        self.preselect_denoise_listWidg_items(default_sel_channel_indexs,list_widget)

    def delete_existing_denoise_list_items(self,list_widget: QListWidget):   
        list_items = [list_widget.item(x) for x in range(list_widget.count())]
        if not list_items: return
        for item in list_items:
            list_widget.takeItem(list_widget.row(item))
            
    def preselect_denoise_listWidg_items(self,list_of_indexs: list, list_widget: QListWidget):
            for i in list_of_indexs:
                list_widget.setItemSelected(list_widget.item(i),True)

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
            self.denoise_hind_metadata.csv_fpath = QFileDialog.getOpenFileName(self,"Open File",self.folder_directory,filter )[0]
            self.import_anim_hind_path.setText(self.denoise_hind_metadata.csv_fpath)
        else:
            self.denoise_fore_metadata.csv_fpath = QFileDialog.getOpenFileName(self,"Open File",self.folder_directory,filter )[0]
            self.import_anim_fore_path.setText(self.denoise_fore_metadata.csv_fpath)

    def get_mot_metadata(self,isHind: bool):
        filter = "*.mot"
        if isHind == True:
            self.denoise_hind_metadata.default_sel_indexes = []
            self.denoise_hind_metadata.mot_fpath = QFileDialog.getOpenFileName(self,"Open File",self.folder_directory,filter )[0]
            if os.path.basename(self.denoise_hind_metadata.mot_fpath) == "komodo06_run12_left_hind_IK.mot":
                self.denoise_hind_metadata.default_sel_indexes = [0,1,2,3,4,5,13,14,15,16,17,18,19]
            self.denoise_hind_metadata.get_anim_channels()
            self.denoise_hind_mot_path.setText(self.denoise_hind_metadata.mot_fpath)
        else:
            self.denoise_fore_metadata.default_sel_indexes = []
            self.denoise_fore_metadata.mot_fpath = QFileDialog.getOpenFileName(self,"Open File",self.folder_directory,filter )[0]
            if os.path.basename(self.denoise_fore_metadata.mot_fpath) == "komodo06_run12_left_fore_ik_output rotmat_v2.mot":
                self.denoise_hind_metadata.default_sel_indexes = [0,1,2,13,14,15,16,17,18,19] 
            self.denoise_fore_metadata.is_hind = False
            self.denoise_fore_metadata.get_anim_channels()
            self.denoise_fore_mot_path.setText(self.denoise_fore_metadata.mot_fpath)
        #print(self.file_path_hind)


    def get_denoise_csv_filepath(self,isHind: bool):
        f_filter = "*.csv"
        if isHind == True: 
            self.denoise_hind_metadata.csv_fpath = QFileDialog.getSaveFileName(self,"save file as",self.folder_directory,f_filter) [0]
            self.denoise_hind_csv_path.setText(self.denoise_hind_metadata.csv_fpath)
        else:
            self.denoise_fore_metadata.csv_fpath = QFileDialog.getSaveFileName(self,"save file as",self.folder_directory,f_filter) [0]
            self.denoise_fore_csv_path.setText(self.denoise_fore_metadata.csv_fpath)
    
    


def get_main_window():
    """Get the maya window pointer to parent this tool under."""
    ptr = omui.MQtUtil.mainWindow()
    # for Py3 use int() , for Py2 use long() , more info: https://docs.python.org/3/whatsnew/3.0.html#integers
    maya_window = wrapInstance(int(ptr), QWidget)
    return maya_window

# Get Maya's main window to parent to
maya_window = get_main_window()
try:
    Komodo_UI.close()
except NameError:
    pass
Komodo_UI = KomodoToolsUI(maya_window)
Komodo_UI.show()
