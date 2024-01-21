
# Komodo Tools | .Mot file Importer
 
**Overview**


This tool is the rewriting of some scripts I used to complete a project where I rigged and animated a Komodo Dragon skeleton for a Ziva muscle sim https://drive.google.com/file/d/1I6_1Ci4JKbbKHskQJsoNe9vzPfTmZOrW/view?usp=sharing 

Features include:                                                                                                     <img src = "https://github.com/Paul-Merzliakov/Komodo-Tools/assets/88568775/219d922e-5699-4c3b-81bc-401c2b20c2d0"  height = "650" align = "right">
  - Constraining bone geometry to an advanced skeleton rig.                                                                              
  - Denoising  motion capture data from a .mot file
  - Importing the denoised mocap data as animation keyframes, with linear interpolation to ensure the animation is loopable.            
  - Mirroring the keys from right to left. 
  - Looping the animation to a certain frame.
  - Looping by  x number of times. 

As of writing this the constrain function and the offsets applied to denoised data are still hardcoded for the specific model and mot file I used. I will be rewriting those shortly.

**Installation**


  1. For denoising the .mot file you'll have to install SciPy and NumPy. To install these on Maya, first change your directory to Maya's bin folder:`cd C:\Program Files\Autodesk\Maya<version>\bin` then install both on there with `mayapy -m pip install <module name>`

  2. To make full use of these tools you'll need a skeleton Mesh, a corresponding Advanced Skeleton rig, and a mot file with the keys you want to import. (An example scene is provided)
   
  3. Place the Komodo-Tools folder in the directory you keep your maya scripts in.
    
  4. Add the path of your Komodo-Tools folder to your PYTHONPATH or MAYA_SCRIPT_PATH environment variables in your maya.env file before startup, **or** if that fails boot up maya and run Python's `sys.path.append(<Komodo-tools path>)` in the script editor (although you'll have to do this everytime you boot up maya).  

  5. Open and run the `main.py` script from the script editor and the ui will appear. 

