#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Johnny
# @Date:   2016-08-02 10:22:55
# @Email:  sg19910914@gmail.com
# @Last Modified by:   Johnny
# @Last Modified time: 2016-08-02 14:50:59
# ----------------------------------------
import os
import glob
import xlwings as xw
import win32api


@xw.sub
def get_File_Name_from_Path():
    """ Get all file names of a certain type from a certain path. """

    xw.Range(3, 'A3').table.clear_contents()

    path = xw.Range(3, 'A1').value
    file = []
    for filename in glob.glob(path):
        filename = os.path.basename(filename)
        file.append([filename])
    if file == []:
        # print('No', os.path.basename(path), "file.")
        Warnings = 'Do not have ' + os.path.basename(path) + " file."
        win32api.MessageBox(
            0, Warnings, "Warning!")
    else:
        xw.Range(3, (3, 1)).value = file
