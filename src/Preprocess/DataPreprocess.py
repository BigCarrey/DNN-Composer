#data preprocessor extracting pitch and duration information from abc files  

import os
import re
import numpy as np
from Preprocess import abcParser
from Preprocess import globalConstant

class ABCPreprocess:
    """
    Preprocess and extract the pitch and duration information from ABC notation files. 

    Properties
    ----------
    measure
        An array of measure information, as measure objects.
    pitch
        A two dimension array of pitch information, as arrays of 34 dimension arrays representing the pitch of each note.
    pitch_dictionary
        A dictionary whose keys are notes and values are indexes of the pitch of each note .
    duration
        A two dimension array of pitch information, as arrays of 23 dimension arrays representing the duration of each note.
    duration_dictionary
        A dictionary whose keys are duration and values are indexes of the duration of each note .
    dir_path
        The path of the directory.
    data
        The ABC files information.
    """
    
    def __init__(self, dir_path, data=[]):
        """
        Do the initialization work.
        """
        self.measures = [] #measure information
        self.pitch = []    # pitch information
        #transpose the key of every song to C Major
        #key must be unchangable, so use 34 as the never reachable index
        #not nessary assign value by such a clumsy way. while the clumy way also has its advantages...  
        self.pitch_dictionary = {globalConstant.note[0] : 0, globalConstant.note[1] : 1, globalConstant.note[2] : 34, globalConstant.note[3] : 0,
                                globalConstant.note[4] : 2, globalConstant.note[5] : 3, globalConstant.note[6] : 1, globalConstant.note[7] : 2,
                                globalConstant.note[8] : 4, globalConstant.note[9] : 5, globalConstant.note[10] : 3, globalConstant.note[11] : 4,
                                globalConstant.note[12] : 5, globalConstant.note[13] : 6, globalConstant.note[14] : 4, globalConstant.note[15] : 5,
                                globalConstant.note[16] : 7, globalConstant.note[17] : 8, globalConstant.note[18] : 6, globalConstant.note[19] : 7,
                                globalConstant.note[20] : 9, globalConstant.note[21] : 10, globalConstant.note[22] : 8, globalConstant.note[23] : 9,
                                globalConstant.note[24] : 10, globalConstant.note[25] : 11, globalConstant.note[26] : 9, globalConstant.note[27] : 10,
                                globalConstant.note[28] : 12, globalConstant.note[29] : 13, globalConstant.note[30] : 11, globalConstant.note[31] : 12,
                                globalConstant.note[32] : 14, globalConstant.note[33] : 15, globalConstant.note[34] : 13, globalConstant.note[35] : 14,
                                globalConstant.note[36] : 16, globalConstant.note[37] : 17, globalConstant.note[38] : 15, globalConstant.note[39] : 16,
                                globalConstant.note[40] : 17, globalConstant.note[41] : 18, globalConstant.note[42] : 16, globalConstant.note[43] : 17,
                                globalConstant.note[44] : 19, globalConstant.note[45] : 20, globalConstant.note[46] : 18, globalConstant.note[47] : 19,
                                globalConstant.note[48] : 21, globalConstant.note[49] : 22, globalConstant.note[50] : 20, globalConstant.note[51] : 21,
                                globalConstant.note[52] : 22, globalConstant.note[53] : 23, globalConstant.note[54] : 21, globalConstant.note[55] : 22,
                                globalConstant.note[56] : 24, globalConstant.note[57] : 25, globalConstant.note[58] : 23, globalConstant.note[59] : 24,
                                globalConstant.note[60] : 26, globalConstant.note[61] : 27, globalConstant.note[62] : 25, globalConstant.note[63] : 26,
                                globalConstant.note[64] : 28, globalConstant.note[65] : 29, globalConstant.note[66] : 27, globalConstant.note[67] : 28,
                                globalConstant.note[68] : 29, globalConstant.note[69] : 30, globalConstant.note[70] : 28, globalConstant.note[71] : 29,
                                globalConstant.note[72] : 31, globalConstant.note[73] : 32, globalConstant.note[74] : 30, globalConstant.note[75] : 31}

                                
        #list first, then convert it to numpy array. see ListToNumpyArrayTest.py.
        self.duration = []    # duration information
            
        self.duration_dictionary = {globalConstant.index0 : 0, 
                                    globalConstant.index1 : 1,
                                    globalConstant.index2 : 2,
                                    globalConstant.index3 : 3,
                                    globalConstant.index4 : 4,
                                    globalConstant.index5 : 5, 
                                    globalConstant.index6 : 6,
                                    globalConstant.index7 : 7,
                                    globalConstant.index8 : 8,
                                    globalConstant.index9 : 9,
                                    globalConstant.index10 : 10,
                                    globalConstant.index11 : 11,
                                    globalConstant.index12 : 12,
                                    globalConstant.index13 : 13,
                                    globalConstant.index14 : 14,
                                    globalConstant.index15 : 15,
                                    globalConstant.index16 : 16,
                                    globalConstant.index17 : 17,
                                    globalConstant.index18 : 18,
                                    globalConstant.index19 : 19,
                                    globalConstant.index20 : 20,
                                    globalConstant.index21 : 21,
                                    globalConstant.index22 : 22                                 
                                    }
        self.dir_path = dir_path;    #path of directionary
        self.data = data    #ABC files information
            
    def processFolder(self, file_name):
        """
        Concatenate all lines from all files in dir_path and return a list.
        """
 
        files = []
        self.listdir(self.dir_path, files)
        for file in files:         
            if file.split('.')[-1] == 'abc': # Only open abc files
                with open(file, 'r') as f:
                    lines = f.readlines()
                    # Skip header info
                    i = 0
                    init = lines[i][0:2]
                    while init != 'X:':
                        i += 1
                        try:
                            init = lines[i][0:2]
                        except:
                            i -= 1
                            break
                    self.data += lines[i:]
        
        self.data = self.keyNormalization(self.data)
        file_object = open(file_name, 'w')
        file_object.writelines(self.data)
        file_object.close()
        
        self.data = []
        
        #return data
    
    
    def listdir(self, dir_path, files):
        """
        Handle the dataset directionary recursively
        """
        
        for item in os.listdir(dir_path):
            if os.path.isdir(os.path.join(dir_path, item)):
                self.listdir(os.path.join(dir_path, item),files)   
            else:
                files.append(os.path.join(dir_path, item))
        
    
#     def keyNormalization(self, file_name):
    def keyNormalization(self, text):
        """
        Transpose the key of every song to C Major
        """
        
        #song is a 2-dimension array carrying the information of every song
        song = [[] for i in range(2317)]
#         text = []
        raw_line = []
        key = ''
        flag =True
        
#         file = open(file_name, 'Ur')
#         text = file.readlines()
#         file.close()
        
        #print(text)
        
        song_count = -1
        for line in text:
#             line = re.sub('\n', '', line)
            if re.search('X:[0-9]+', line) != None:
                song_count = song_count + 1
            song[song_count].append(line)
        
        #operate every song
        for i in range(2317):
            for every_line in song[i]:
                if re.search('K:[A-Z][a-z]*', every_line) != None:
                    #get key value
                    key = re.sub('K:', '', every_line)
                    key = re.sub('\n', '', key)
                    flag =False
                    raw_line.append(every_line)
                    
#                     print(key)
#                     print(len(key))
                    
                    #every_line = every_line.replace('K:', '')
                elif re.search('(([A-J]|[L-Z]):[A-Z]*[a-z]*)', every_line) != None:
                    raw_line.append(every_line)
                    flag =False
                    
                else:
                    flag = True
                          
                    #A
                    if key == 'Am':
                        pass
                    elif key == 'A':
                        if re.search('\^C', every_line) != None:
                            every_line = re.sub('\^C', 'D', every_line)
                        if re.search('\^F', every_line) != None:
                            every_line = re.sub('\^F', 'G', every_line)
                        if re.search('\^G', every_line) != None:
                            every_line = re.sub('\^G', 'A', every_line)
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        every_line = re.sub('G', '^G', every_line)
                        
                        if re.search('\^c', every_line) != None:
                            every_line = re.sub('\^c', 'd', every_line)
                        if re.search('\^f', every_line) != None:
                            every_line = re.sub('\^f', 'g', every_line)
                        if re.search('\^g', every_line) != None:
                            every_line = re.sub('\^g', 'a', every_line)
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('f', '^f', every_line)
                        every_line = re.sub('g', '^g', every_line)
                    elif key == 'Amix':
                        if re.search('\^F', every_line) != None:
                            every_line = re.sub('\^F', 'G', every_line)
                        every_line = re.sub('F', '^F', every_line, re.IGNORECASE)
                        if re.search('\^f', every_line) != None:
                            every_line = re.sub('\^f', 'g', every_line)
                        every_line = re.sub('f', '^f', every_line, re.IGNORECASE)
                    elif key == 'Ador':
                        if re.search('\^C', every_line) != None:
                            every_line = re.sub('\^C', 'D', every_line)
                        if re.search('\^F', every_line) != None:
                            every_line = re.sub('\^F', 'G', every_line)
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        
                        if re.search('\^c', every_line) != None:
                            every_line = re.sub('\^c', 'd', every_line)
                        if re.search('\^f', every_line) != None:
                            every_line = re.sub('\^f', 'g', every_line)
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('f', '^f', every_line)
                    #B
                    elif key == 'B':
                        if re.search('\^C', every_line) != None:
                            every_line = re.sub('\^C', 'D', every_line)
                        if re.search('\^D', every_line) != None:
                            every_line = re.sub('\^D', 'E', every_line)
                        if re.search('\^F', every_line) != None:
                            every_line = re.sub('\^F', 'G', every_line)
                        if re.search('\^G', every_line) != None:
                            every_line = re.sub('\^G', 'A', every_line)
                        if re.search('\^A', every_line) != None:
                            every_line = re.sub('\^A', 'B', every_line)
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('D', '^D', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        every_line = re.sub('G', '^G', every_line)
                        every_line = re.sub('A', '^A', every_line)
                        
                        if re.search('\^c', every_line) != None:
                            every_line = re.sub('\^c', 'd', every_line)
                        if re.search('\^d', every_line) != None:
                            every_line = re.sub('\^d', 'e', every_line)
                        if re.search('\^f', every_line) != None:
                            every_line = re.sub('\^f', 'g', every_line)
                        if re.search('\^g', every_line) != None:
                            every_line = re.sub('\^g', 'a', every_line)
                        if re.search('\^a', every_line) != None:
                            every_line = re.sub('\^a', 'b', every_line)
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('d', '^d', every_line)
                        every_line = re.sub('f', '^f', every_line)
                        every_line = re.sub('g', '^g', every_line)
                        every_line = re.sub('a', '^a', every_line)
                    elif key == 'Bm':
                        if re.search('\^C', every_line) != None:
                            every_line = re.sub('\^C', 'D', every_line)
                        if re.search('\^F', every_line) != None:
                            every_line = re.sub('\^F', 'G', every_line)
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        
                        if re.search('\^c', every_line) != None:
                            every_line = re.sub('\^c', 'd', every_line)
                        if re.search('\^f', every_line) != None:
                            every_line = re.sub('\^f', 'g', every_line)
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('f', '^f', every_line)
                    elif key == 'Bmix':
                        if re.search('\^C', every_line) != None:
                            every_line = re.sub('\^C', 'D', every_line)
                        if re.search('\^D', every_line) != None:
                            every_line = re.sub('\^D', 'E', every_line)
                        if re.search('\^F', every_line) != None:
                            every_line = re.sub('\^F', 'G', every_line)
                        if re.search('\^G', every_line) != None:
                            every_line = re.sub('\^G', 'A', every_line)
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('D', '^D', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        every_line = re.sub('G', '^G', every_line)
                        
                        if re.search('\^c', every_line) != None:
                            every_line = re.sub('\^c', 'd', every_line)
                        if re.search('\^d', every_line) != None:
                            every_line = re.sub('\^d', 'e', every_line)
                        if re.search('\^f', every_line) != None:
                            every_line = re.sub('\^f', 'g', every_line)
                        if re.search('\^g', every_line) != None:
                            every_line = re.sub('\^g', 'a', every_line)
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('d', '^d', every_line)
                        every_line = re.sub('f', '^f', every_line)
                        every_line = re.sub('g', '^g', every_line)
                    elif key == 'Bdor':
                        if re.search('\^C', every_line) != None:
                            every_line = re.sub('\^C', 'D', every_line)
                        if re.search('\^F', every_line) != None:
                            every_line = re.sub('\^F', 'G', every_line)
                        if re.search('\^G', every_line) != None:
                            every_line = re.sub('\^G', 'A', every_line)
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        every_line = re.sub('G', '^G', every_line)
                        
                        if re.search('\^c', every_line) != None:
                            every_line = re.sub('\^c', 'd', every_line)
                        if re.search('\^f', every_line) != None:
                            every_line = re.sub('\^f', 'g', every_line)
                        if re.search('\^g', every_line) != None:
                            every_line = re.sub('\^g', 'a', every_line)
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('f', '^f', every_line)
                        every_line = re.sub('g', '^g', every_line)
                    #C
                    elif key == 'C':
                        pass
                    elif key == 'Cm':
                        if re.search('_E', every_line) != None:
                            every_line = re.sub('_E', 'D', every_line)
                        if re.search('_A', every_line) != None:
                            every_line = re.sub('_A', 'G', every_line)
                        if re.search('_B', every_line) != None:
                            every_line = re.sub('_B', 'A', every_line)
                        every_line = re.sub('E', '_E', every_line)
                        every_line = re.sub('A', '_A', every_line)
                        every_line = re.sub('B', '_B', every_line)
                        
                        if re.search('_e', every_line) != None:
                            every_line = re.sub('_e', 'd', every_line)
                        if re.search('_a', every_line) != None:
                            every_line = re.sub('_a', 'g', every_line)
                        if re.search('_b', every_line) != None:
                            every_line = re.sub('_b', 'a', every_line)
                        every_line = re.sub('e', '_e', every_line)
                        every_line = re.sub('a', '_a', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    elif key == 'Cmix':
                        if re.search('_B', every_line) != None:
                            every_line = re.sub('_B', 'A', every_line)
                        every_line = re.sub('B', '_B', every_line)
                        
                        if re.search('_b', every_line) != None:
                            every_line = re.sub('_b', 'a', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    elif key == 'Cdor':
                        if re.search('_E', every_line) != None:
                            every_line = re.sub('_E', 'D', every_line)
                        if re.search('_B', every_line) != None:
                            every_line = re.sub('_B', 'A', every_line)
                        every_line = re.sub('E', '_E', every_line)
                        every_line = re.sub('B', '_B', every_line)
                        
                        if re.search('_e', every_line) != None:
                            every_line = re.sub('_e', 'd', every_line)
                        if re.search('_b', every_line) != None:
                            every_line = re.sub('_b', 'a', every_line)
                        every_line = re.sub('e', '_e', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    #D
                    elif key == 'D':
                        if re.search('\^C', every_line) != None:
                            every_line = re.sub('\^C', 'D', every_line)
                        if re.search('\^F', every_line) != None:
                            every_line = re.sub('\^F', 'G', every_line)
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        
                        if re.search('\^c', every_line) != None:
                            every_line = re.sub('\^c', 'd', every_line)
                        if re.search('\^f', every_line) != None:
                            every_line = re.sub('\^f', 'g', every_line)
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('f', '^f', every_line)
                    elif key == 'Dm':
                        if re.search('_B', every_line) != None:
                            every_line = re.sub('_B', 'A', every_line)
                        every_line = re.sub('B', '_B', every_line)
                        
                        if re.search('_b', every_line) != None:
                            every_line = re.sub('_b', 'a', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    elif key == 'Dmix':
                        if re.search('\^F', every_line) != None:
                            every_line = re.sub('\^F', 'G', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        
                        if re.search('\^f', every_line) != None:
                            every_line = re.sub('\^f', 'g', every_line)
                        every_line = re.sub('f', '^f', every_line)
                    elif key == 'Ddor':
                        pass
                    #E
                    elif key == 'E':
                        if re.search('\^C', every_line) != None:
                            every_line = re.sub('\^C', 'D', every_line)
                        if re.search('\^D', every_line) != None:
                            every_line = re.sub('\^D', 'E', every_line)
                        if re.search('\^F', every_line) != None:
                            every_line = re.sub('\^F', 'G', every_line)
                        if re.search('\^G', every_line) != None:
                            every_line = re.sub('\^G', 'A', every_line)
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('D', '^D', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        every_line = re.sub('G', '^G', every_line)
                        
                        if re.search('\^c', every_line) != None:
                            every_line = re.sub('\^c', 'd', every_line)
                        if re.search('\^d', every_line) != None:
                            every_line = re.sub('\^d', 'e', every_line)
                        if re.search('\^f', every_line) != None:
                            every_line = re.sub('\^f', 'g', every_line)
                        if re.search('\^g', every_line) != None:
                            every_line = re.sub('\^g', 'a', every_line)
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('d', '^d', every_line)
                        every_line = re.sub('f', '^f', every_line)
                        every_line = re.sub('g', '^g', every_line)
                    elif key == 'Em':
                        if re.search('\^F', every_line) != None:
                            every_line = re.sub('\^F', 'G', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        
                        if re.search('\^f', every_line) != None:
                            every_line = re.sub('\^f', 'g', every_line)
                        every_line = re.sub('f', '^f', every_line)
                    elif key == 'Emix':
                        if re.search('\^C', every_line) != None:
                            every_line = re.sub('\^C', 'D', every_line)
                        if re.search('\^F', every_line) != None:
                            every_line = re.sub('\^F', 'G', every_line)
                        if re.search('\^G', every_line) != None:
                            every_line = re.sub('\^G', 'A', every_line)
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        every_line = re.sub('G', '^G', every_line)
                        
                        if re.search('\^c', every_line) != None:
                            every_line = re.sub('\^c', 'd', every_line)
                        if re.search('\^f', every_line) != None:
                            every_line = re.sub('\^f', 'g', every_line)
                        if re.search('\^g', every_line) != None:
                            every_line = re.sub('\^g', 'a', every_line)
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('f', '^f', every_line)
                        every_line = re.sub('g', '^g', every_line)
                    elif key == 'Edor':
                        if re.search('\^C', every_line) != None:
                            every_line = re.sub('\^C', 'D', every_line)
                        if re.search('\^F', every_line) != None:
                            every_line = re.sub('\^F', 'G', every_line)
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        
                        if re.search('\^c', every_line) != None:
                            every_line = re.sub('\^c', 'd', every_line)
                        if re.search('\^f', every_line) != None:
                            every_line = re.sub('\^f', 'g', every_line)
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('f', '^f', every_line)
                    #F
                    elif key == 'F':
                        if re.search('_B', every_line) != None:
                            every_line = re.sub('_B', 'A', every_line)
                        every_line = re.sub('B', '_B', every_line)
                        
                        if re.search('_b', every_line) != None:
                            every_line = re.sub('_b', 'a', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    elif key == 'Fm':
                        if re.search('_D', every_line) != None:
                            every_line = re.sub('_D', 'C', every_line)
                        if re.search('_E', every_line) != None:
                            every_line = re.sub('_E', 'D', every_line)
                        if re.search('_A', every_line) != None:
                            every_line = re.sub('_A', 'G', every_line)
                        if re.search('_B', every_line) != None:
                            every_line = re.sub('_B', 'A', every_line)
                        every_line = re.sub('D', '_D', every_line)
                        every_line = re.sub('E', '_E', every_line)
                        every_line = re.sub('A', '_A', every_line)
                        every_line = re.sub('B', '_B', every_line)
                        
                        if re.search('_d', every_line) != None:
                            every_line = re.sub('_d', 'c', every_line)
                        if re.search('_e', every_line) != None:
                            every_line = re.sub('_e', 'd', every_line)
                        if re.search('_a', every_line) != None:
                            every_line = re.sub('_a', 'g', every_line)
                        if re.search('_b', every_line) != None:
                            every_line = re.sub('_b', 'a', every_line)
                        every_line = re.sub('d', '_d', every_line)
                        every_line = re.sub('e', '_e', every_line)
                        every_line = re.sub('a', '_a', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    elif key == 'Fmix':
                        if re.search('_E', every_line) != None:
                            every_line = re.sub('_E', 'D', every_line)
                        if re.search('_B', every_line) != None:
                            every_line = re.sub('_B', 'A', every_line)
                        every_line = re.sub('E', '_E', every_line)
                        every_line = re.sub('B', '_B', every_line)
                        
                        if re.search('_e', every_line) != None:
                            every_line = re.sub('_e', 'd', every_line)
                        if re.search('_b', every_line) != None:
                            every_line = re.sub('_b', 'a', every_line)
                        every_line = re.sub('e', '_e', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    elif key == 'Fdor':
                        if re.search('_E', every_line) != None:
                            every_line = re.sub('_E', 'D', every_line)
                        if re.search('_A', every_line) != None:
                            every_line = re.sub('_A', 'G', every_line)
                        if re.search('_B', every_line) != None:
                            every_line = re.sub('_B', 'A', every_line)
                        every_line = re.sub('E', '_E', every_line)
                        every_line = re.sub('A', '_A', every_line)
                        every_line = re.sub('B', '_B', every_line)
                        
                        if re.search('_e', every_line) != None:
                            every_line = re.sub('_e', 'd', every_line)
                        if re.search('_a', every_line) != None:
                            every_line = re.sub('_a', 'g', every_line)
                        if re.search('_b', every_line) != None:
                            every_line = re.sub('_b', 'a', every_line)
                        every_line = re.sub('e', '_e', every_line)
                        every_line = re.sub('a', '_a', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    #G
                    elif key == 'G':
                        if re.search('\^F', every_line) != None:
                            every_line = re.sub('\^F', 'G', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        
                        if re.search('\^f', every_line) != None:
                            every_line = re.sub('\^f', 'g', every_line)
                        every_line = re.sub('f', '^f', every_line)
                    elif key == 'Gm':
                        if re.search('_E', every_line) != None:
                            every_line = re.sub('_E', 'D', every_line)
                        if re.search('_B', every_line) != None:
                            every_line = re.sub('_B', 'A', every_line)
                        every_line = re.sub('E', '_E', every_line)
                        every_line = re.sub('B', '_B', every_line)
                        
                        if re.search('_e', every_line) != None:
                            every_line = re.sub('_e', 'd', every_line)
                        if re.search('_b', every_line) != None:
                            every_line = re.sub('_b', 'a', every_line)
                        every_line = re.sub('e', '_e', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    elif key == 'Gmix':
                        pass
                    elif key == 'Gdor':
                        if re.search('_B', every_line) != None:
                            every_line = re.sub('_B', 'A', every_line)
                        every_line = re.sub('B', '_B', every_line)
                        
                        if re.search('_b', every_line) != None:
                            every_line = re.sub('_b', 'a', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    #key error
                    else:
                        print(every_line)
                        print(key)
                        print("Key Error!!")
                        
                if flag == True:        
                    every_line = re.sub('=\^', '', every_line)
                    every_line = re.sub('=_', '', every_line)
                                               
                    raw_line.append(every_line)
                    
        return raw_line


    def getLines(self,file_name):
        """
        Get line information, return an array of line objects.
        """
        
        tune=abcParser.Tune(file_name)
        #print(tune.line[0].measure)
        return tune.line
    
    
    def getMeasures(self, file_name):
        """
        Get measure information, return an array of measure objects.
        """
        
        lines = self.getLines(file_name)
        measure = []
        for line in lines:
            measure.append(line.measure)
        return measure
    
    def getNotes(self, file_name): 
        """
        Get note information, return an array of string.
        """
        
        measures = self.getMeasures(file_name)
        notes = []
        note = []
        for measure in measures:
            for line_measure in measure:
                #separate the measures by regular expression, then analyze the duration
                #p = re.compile('((\^|_|=)?[a-gA-G]((,*)|(\'*))?([2-9]?//*[2-9]?)?([2-9])?(>*)?(<*)?)')
                p = re.compile('(((\^|_|=)?[a-gA-G]((,*)|(\'*))?([2-9]?//*[2-9]?)?([2-9])?(>*)?(<*)?)|(#ending))')
                
                #p = re.compile('((\^|_|=)?[a-gA-G]([2-9]?//*[2-9]?)?([2-9])?((<*)?|(>*)?)?)')
                note = p.findall(line_measure.__str__())
                for i in range(len(note)):
                    notes.append(note[i][0])
                note =[]
                #print(re.findall('(\^|_|=)?[a-gA-G]([2-9]?//*|[2-9]?)(((<*)?|(>*)?)?)?', line_measure.__str__()))
        return notes
            
#     #get pitch information
#     #without ABCPArser.
#     #lost the repeat information.
#   
#     def getPitch(self, file_name):
#         #根据调性出现频率，转化调性至C大调(或频率最高的调性)
#         pitch_list = [(0) for i in range(33)]
#          
#          
#         #lines that are after transposition
#         lines = self.keyNormalization(file_name)
#         for line in lines:
#             p = re.compile('((\^|_|=)?[a-gA-G]((,*)|(\'*))?)')
#             note = p.findall(line)
#              
#             for i in range(len(note)):
#                 pitch_list[self.pitch_dictionary[note[i][0].__str__()]] = 1
#                 self.pitch.append(pitch_list)
#                 pitch_list = [(0) for i in range(33)]
#                  
#         return self.pitch

    #723 pieces of data lost
    #fixed the lost problem.
    def getPitch(self,file_name):
        """
        Get pitch information, return an array of 34 dimension array. Refer to pitch.dat.
        """
        
        notes = self.getNotes(file_name)
        pitch_list = [(0) for i in range(33)]
        pitch_timesteps = []
          
        for note in notes:
            #p = re.compile('((\^|_|=)?[a-gA-G]((,*)|(\'*))?)')
            p = re.compile('(((\^|_|=)?[a-gA-G]((,*)|(\'*))?)|(#ending))')
            current_notes = p.findall(note)
                
            for i in range(len(current_notes)):
                if current_notes[i][0].__str__() != '#ending':
                    pitch_list[self.pitch_dictionary[current_notes[i][0].__str__()]] = 1
                    pitch_timesteps.append(pitch_list)
                    pitch_list = [(0) for i in range(33)]
                else:
                    self.pitch.append(pitch_timesteps)
                    pitch_timesteps = []
                       
        return self.pitch 
 
 
    def getDuration(self, file_name):
        """
        Get duration information, return an array of 23 dimension array. Refer to Duration.dat.
        """
       
        notes = self.getNotes(file_name)
        duration_list = [(0) for i in range(23)]
        duration_timesteps = []
        
        new_nextNoteDurationPlus = 0.0
        new_nextNoteDurationFlag = False
        count = 0
        
        for note in notes:
            
            note_analysis = abcParser.Note()
            if count == 0:
                text, current_duration, nextNoteDurationPlus, nextNoteDurationFlag = note_analysis.parse(note)
                count = count + 1
            else:
                text, current_duration, nextNoteDurationPlus, nextNoteDurationFlag = note_analysis.parse(note, new_nextNoteDurationPlus, new_nextNoteDurationFlag)
            if text == '#ending':
                #self.duration append a vector of the duration information of a note
                self.duration.append(duration_timesteps)
                duration_timesteps = []
            else:
                
                duration_list[self.duration_dictionary[current_duration]] = 1
                duration_timesteps.append(duration_list)
                duration_list = [(0) for i in range(23)]

            new_nextNoteDurationPlus = nextNoteDurationPlus
            new_nextNoteDurationFlag = nextNoteDurationFlag

        return self.duration
    
    
    
    
    