
Fennec v0.1
Author: Ayoub Lharchi
Contact: ayoublharchi@gmail.com
Website: http://www.lharchi.com

==============================================================
==============================================================


Fennec is a free tool to make plugins for Grasshopper using Python. It allows you to write plugins using Python and to generate a *.gha file ready to be distributed. The tool doesn’t require any external editor or extra DLL files to be delivred with the generated gha file.


==============================================================
==============================================================

To use Fennec, you need the following requirements:

1. .NET Framework 4.0 or higher (Which you should already have if you are running Grasshopper)
2. Rhino 5.0 (at least SR12)
3. Grasshopper


==============================================================
==============================================================


How to use:

Fennec is really simple to use:

For every component you have in your plugin:
Select the .py file containing all your component code
Define the icon, name, nickname, description, category and subcategory of the component
Important: Generate an new GUID for your component (or use an existing one if you have it)
Define all the input and output parameters: name, nickname, description, type and the access (This version doesn’t support data-tree access. Planned for the next one)
Add all your components
Generate your gha file (File > Make GHA)


==============================================================
==============================================================

How to prepare your Python file:

The code for every component should be all in one .py file. The defined input and output parameters are handeled the same way as in the GhPython component. When you declare your input parameters, you can use them simply in your Python code. You should always return the defined output parameters.


==============================================================
==============================================================

