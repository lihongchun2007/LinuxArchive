#!/usr/bin/env python3

import os
from glob import glob
import random
import argparse
from binaryornot.check import is_binary
import pypandoc

def code2MarkdownText(codeFileName, chapterLevel=1):
    if not os.path.isfile(codeFileName): 
        return '', ''
    elif is_binary(codeFileName):
        return '', ''

    [head, tail] = os.path.split(codeFileName)
    if tail == '':
        tail = head

    with open(codeFileName, 'r') as codeFile:
        code = codeFile.read()

    head= ''.join(['#'*chapterLevel, ' ', tail])

    ext = os.path.splitext(codeFileName)[1].lower()
    if ext in ['.md', '.markdown']:
        return head, code
    else:
        return head, '\n'.join([head, '```', code, '```'])


def convertFileList(pathName, fileSepNameList, chapterLevel):
    content = []
    toc = []

    dirFileDict = {}
    for fileSepName in fileSepNameList:
        if len(fileSepName) == 1:
            codeFileName = os.path.join(pathName, fileSepName[0])
            head, cont = code2MarkdownText(codeFileName, chapterLevel)
            toc.append(head)
            content.append(cont)
        elif fileSepName[0] in dirFileDict:
            dirFileDict[fileSepName[0]].append(fileSepName[1:])
        else:
            dirFileDict[fileSepName[0]] = [fileSepName[1:]]

    for key in dirFileDict:
        head = ''.join(['#'*chapterLevel, ' ', key])
        toc.append(head)
        content.append(head)

        heads, cont = convertFileList(os.path.join(pathName, key), dirFileDict[key], chapterLevel+1)
        toc.append(heads)
        content.append(cont)

    return '\n'.join(toc), '\n'.join(content)


def __splitPath(fileName):
    if fileName == '':
        return []
    elif fileName == '/':
        return ['/']

    [head, tail] = os.path.split(fileName)
    return [tail, ] + __splitPath(head)

def splitPath(fileName):
    dirList = __splitPath(fileName)
    dirList.reverse()

    return dirList


def searchFileDirectory(startPathName):
    cwd = os.getcwd()
    os.chdir(startPathName)

    files = glob('**', recursive=True)
    sepPathNames = [splitPath(f) for f in files]
    sepPathNames.sort()
    sepPathNames.sort(key=len)

    os.chdir(cwd)
    
    return sepPathNames

def code2book(codeDirectory, outputFileName):
    tmpPathName = '/tmp/code2book-' + str(int(random.random()*10000))
    sepPathNames = searchFileDirectory(codeDirectory)
    toc, content = convertFileList(codeDirectory, sepPathNames, 1)

    #content = toc + content
    outputFileType = os.path.splitext(outputFileName)[1].lower()
    if outputFileType == '.pdf':
        pypandoc.convert_text(content, to='pdf', format='markdown', outputfile=outputFileName)
    else:
        pypandoc.convert_text(content, to='epub', format='markdown', outputfile=outputFileName)


if __name__ == '__main__':
    argParser = argparse.ArgumentParser(description='Convert souce code into a book')
    argParser.add_argument('codeDirectory', help='directory of source code')
    argParser.add_argument('outputFileName', help='name of output file name with type of epub/pdf')
    args = argParser.parse_args()

    code2book(args.codeDirectory, args.outputFileName)
