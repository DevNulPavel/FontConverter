#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.dom.minidom as xmldom
import os.path
import os
import re
import sys
import math




curFolder = os.path.dirname(__file__)
sourcesDir = os.path.join(curFolder, "sources")
resultDir = os.path.join(curFolder, "result")

# создадим сразу папку результатов
try:
    os.mkdir(resultDir)
except:
    pass


sourceFilesList = os.listdir(sourcesDir)

for sourceFileName in sourceFilesList:
    if ".fnt" not in sourceFileName:
        continue

    symbolInformations = {}

    sourceFilePath = os.path.join(sourcesDir, sourceFileName)

    xmlData = xmldom.parse(sourceFilePath).getElementsByTagName("font")
    info = xmlData[0].getElementsByTagName("info")
    common = xmlData[0].getElementsByTagName("common")
    chars = xmlData[0].getElementsByTagName("chars")
    kernings = xmlData[0].getElementsByTagName("kernings")

    atlasWidth = float(common[0].attributes['scaleW'].value)
    atlasHeight = float(common[0].attributes['scaleH'].value)

    charsValues = chars[0].getElementsByTagName("char")
    for charInfo in charsValues:
        id = int(charInfo.attributes['id'].value)
        x = float(charInfo.attributes['x'].value) / atlasWidth
        y = float(charInfo.attributes['y'].value) / atlasHeight
        width = float(charInfo.attributes['width'].value) / atlasWidth
        height = float(charInfo.attributes['height'].value) / atlasHeight
        charWidth = int(math.ceil(int(charInfo.attributes['width'].value) / 2))
        charHeight = int(math.ceil(int(charInfo.attributes['height'].value) / 2))
        xOffset = int(math.ceil(int(charInfo.attributes['xoffset'].value) / 2))
        yOffset = int(math.ceil(int(charInfo.attributes['yoffset'].value) / 2))
        xAdvance = int(math.ceil(int(charInfo.attributes['xadvance'].value) / 2))

        charInfo = {"id": id,
                    "x": x, "y": y,
                    "width": width, "height": height,
                    "charWidth": charWidth, "charHeight": charHeight,
                    "xOffset": xOffset, "yOffset": yOffset,
                    "xAdvance": xAdvance}
        symbolInformations[id] = charInfo


    resultFilePath = os.path.join(resultDir, sourceFileName + ".chars.h")

    with open(resultFilePath, "w") as fileIO:
        for i in range(32, 127):
            if i in symbolInformations.keys():
                symbolInfo = symbolInformations[i]
                line = "{{{0}f, {1}f, {2}f, {3}f, {4}, {5}, {6}, {7}, {8}}},\n".\
                        format(symbolInfo["x"], symbolInfo["y"],
                            symbolInfo["width"], symbolInfo["height"],
                            symbolInfo["charWidth"], symbolInfo["charHeight"],
                            symbolInfo["xOffset"], symbolInfo["yOffset"],
                            symbolInfo["xAdvance"])
            else:
                line = "{{0.0f, 0.0f, 0.0f, 0.0f, 0, 0, 0, 0, 0}}"

            fileIO.write(line)