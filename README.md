
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


  1. For denoising the .mot file you'll have to install SciPy and NumPy. To install these on Maya, first change your directory to Maya's bin folder:`cd C:\Program Files\Autodesk\Maya<version>\bin` then install it there with `mayapy -m pip install numpy/scipy`

  2. To make full use of these tools you'll need a skeleton Mesh, a corresponding Advanced Skeleton rig, and a mot file with the keys you want to import. (An example scene will be provided in the near future)
   
  3. Append  `C:\Program Files\Autodesk\Maya<version>\scripts\Komodo-Tools`  to  the PYTHONPATH maya.env variable or if that doesn't work append it to pythons sys.path. 

  4. Open and run the Main script from the script editor and the ui will appear. 

