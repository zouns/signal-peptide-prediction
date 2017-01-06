from Bio import SeqIO
from os import listdir
from random import randint

print("test3")

#According to the chosen mode, access the desired folder and call the files reading functions
#In the end, returns a list of dictionaries
#Each dictionary has 4 elements :
#1.sequence : sequence of AA
#2.annotationLine
#3.classificationStatus : 'p' if positive exemple, 'n' if negative
#4.isTraining : 'y' if it is a training exemple, 'n' otherwise.
#Proportion of training examples is chosen with the  variable trainingProportion, between 0 and 1
def accessFolders(mode, trainingProportion):
    data = []
    if (mode == "tm" or mode =="all"):
        data += accessFiles("n", trainingProportion, "data/training_data/negative_examples/tm/")
        data += accessFiles("p", trainingProportion, "data/training_data/positive_examples/tm/") 
    if (mode == "nontm" or mode == "all"):
        data += accessFiles("n", trainingProportion, "data/training_data/negative_examples/non_tm/")
        data += accessFiles("p", trainingProportion, "data/training_data/positive_examples/non_tm/")
    return data

#Access all the files in the specific folder
def accessFiles(classificationStatus,trainingProportion,folder):
    data = []
    for f in listdir(folder):
        data += readFile(classificationStatus,trainingProportion,folder + f)
    return data

#Read all the sequences from a specific file
#A number of sequences is chosen randomly in the file to become training examples, according to wanted proportion
def readFile(classificationStatus,trainingProportion,f):
    data = []
    nElements = 0
    with open(f, 'r') as fhandle:
        for record in SeqIO.parse(fhandle, "fasta"):
            nElements += 1
            data.append({'sequence' : record.seq.split('#')[0],
                         'annotationLine' : record.seq.split('#')[1],
                         'classificationStatus' : classificationStatus,
                         'isTraining' : 'y'})
            fhandle.closed
        for n in pickRandomElements(nElements,trainingProportion):
            data[n]['isTraining'] = 'n'
    return data

#Returns a list of number between 0 and nElements -1, where the wanted proportion of elements has been removed randomly
def pickRandomElements(nElements, proportion):
    l = range(0,nElements)
    numberToPick = proportion * nElements
    numberPicked = 0
    while (numberPicked < numberToPick):
        del l[randint(0,len(l) - 1)]
        numberPicked += 1
    return l

# if len(sys.argv) <= 1 or sys.argv[1] not in ["tm","nontm","all"]:
#     sys.stderr.write("You need to choose a correct mode :\ntm\nnontm\nall\n")
#     sys.exit("Script exited with error")
# else:
#     mode = sys.argv[1]
#     if len(sys.argv) == 2:
#         print ("Default training proportion chosen : 0.7")
#         trainingProportion = 0.7
#     else:    
#         trainingProportion = float(sys.argv[2])
#         if not (trainingProportion <= 1.0 and trainingProportion >= 0):
#             sys.stderr.write("The proportion should be between 0 and 1\n")
#             sys.exit("Script exited with error")

#     data = accessFolders(mode, trainingProportion)
#     #print data
#     print len(data)
