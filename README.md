
# Komodo Tools | .Mot file Importer

**Overview**


This tool is the rewriting of a series of scripts I used to complete a project where I rigged and animated the skeleton to run a Ziva muscle sim on a Komodo Dragon's Walk cycle. https://drive.google.com/file/d/1I6_1Ci4JKbbKHskQJsoNe9vzPfTmZOrW/view?usp=sharing 

Features include
  - Constraining bone geometry to an advanced skeleton rig.
  - Denoising  mocap data from a .mot file
  - Importing that smoothed mocap data as animation keyframes, with linear interpolation to ensure the animation is loopable. 
  - Mirroring the keys from right to left. 
  - looping the animation to a certain frame or  loop by  x number of times. 

As of writing this the constrain function and the offsets applied to denoised data are still hardcoded for the specific model/ mot file I used.  But I will be rewriting those in the near future.

**Installation**

  1. For denoising the .mot file you'll have to install SciPy and NumPy. To install these on Maya, first  change your directory to Maya's bin folder:`cd C:\Program Files\Autodesk\Maya<version>\bin` then install it there with `mayapy -m pip install numpy/scipy`

  2. To make full use of these tools you'll need a skeleton Mesh, a corresponding Advanced Skeleton rig, and a mot file with the keys you want to import. (An example scene will be provided in the near future)
   
  3. Append  `C:\Program Files\Autodesk\Maya<version>\scripts\Komodo-Tools`  to  the PYTHONPATH maya.env variable or if that doesn't work append it to pythons sys.path. 

  4. Open and run the Main script from the script editor and the ui will appear. 

