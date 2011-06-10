=======================================
 Granulate 
=======================================

The Granulate package

Requirements
============

- python-imaging
- pypdf2table

Installation
============

 easy_install Granulate-0.1-py2.5.egg


Introduction to the GranulateSVG class
======================================

GranulateSVG cares about automated extraction on svg files
You can choose the maximum number of images (grains) in which you want to split your svg file

+---------------------------------------------------------------------------------------------
                            -- How it works --

It waits for an opened StringIO with a valid svg file written in it, and the maximum number
of grains to split.
It builds a svg tree containing all necessary definitions - like styles, defs, etc - 
to each group of grains. It looks for basic shapes, paths, texts and some other svg tags, 
sequentially, getting all properties of it and its parents (recursivily) and write 
this group when the number of elements per file is complete. When the number of grains 
per file arrives they are appended to the list as a StringIO containing the entire actual 
SVG tree. The tree is maintained removing all the written nodes and its parents (recursivily).

It returns a list of StringIOs, each element containing at least one grain.
---------------------------------------------------------------------------------------------+

The proccess of calculating the number of images per file
=========================================================

It counts the number of element nodes that are interesting to it (like shapes, paths, texts) and
try to divide it to the maximum number of grains.
If the remainder is zero, it's ok, there will be the same number of grains in each group of grains.
If not, it gets the remainder and adds it into the first groups of grains, one from the remainder per group.
Example: maximum = 50, number of interesting element nodes = 240
          -->  240/50 = 4 and the remainder = 40

        This way, the last ten groups have 4 elements and the first fourty groups have 5.

