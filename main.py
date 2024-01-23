#ui
import ui
global Komodo_UI
# Get Maya's main window to parent to
maya_window = ui.get_main_window()
try:
    Komodo_UI.close()
except NameError:
    pass
Komodo_UI = ui.KomodoToolsUI(maya_window)
Komodo_UI.show()
