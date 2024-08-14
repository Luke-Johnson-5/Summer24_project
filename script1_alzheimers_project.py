import os
import re
import csv

my_dir = os.getcwd()
term = "acclist"  # Identifier of all CensuScope output files
thresh = 10  # Currently unused, remove if unnecessary
fileList = []
list_Census = []
blacklist_path = '/Users/Luke/pythonlocal/blackList-v2.0.csv'  # Use your appropriate file path and un-comment out line

# Read the blacklist file into a set
def read_blacklist(blacklist_path):
    blacklist = set()
    with open(blacklist_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # Ensure row is not empty
                blacklist.add(row[0])
    return blacklist

# Create a list of file paths to each of the CensuScope outputs
def createFileList(my_dir, term):
    for subdir, dirs, files in os.walk(my_dir):
        for file in files:
            if re.search(re.escape(term), file):
                result = os.path.join(subdir, file)
                fileList.append(result)
    return fileList

# Read and filter the CensuScope result file
def readCensusresultFile(file, list_Census, blacklist):
    with open(file, 'r') as read:
        reader = read.readlines()
        for line in reader:
            accession = line.strip()
            if accession in blacklist:
                continue
            if accession not in list_Census:
                list_Census.append(accession)
    return list_Census

def main():
    blacklist = read_blacklist(blacklist_path)
    fileList = createFileList(my_dir, term)
    for i in fileList:
        sample_list = readCensusresultFile(i, list_Census, blacklist)

    # Output the results
    with open('all_Acc_in_gut_samples1.3.txt', 'w') as file:
        for j in sample_list:
            print(j)
            file.write(j + '\n')

if __name__ == '__main__':
    main()
