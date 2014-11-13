import urllib2
from bs4 import BeautifulSoup
import csv
import numpy
import json

class ElectionData:
    def __init__(self,url,outfile,outfileJ):
        self.url=url
        self.outfile=outfile
        self.outfileJ=outfileJ
        #array representation of data:
        self.output=[]
        self.votes=[]

    def load(self):
        page=urllib2.urlopen(self.url)
        soup=BeautifulSoup(page)
        table = soup.find('table', border=1)
        rows = table.find_all('tr')
        #add column header data to output arr
        h=table.find_all('th')
        headings=[]
        for i in range(0,7):
            bit=h[i].find(text=True)
            headings.append(strip_non_ascii(bit))
        self.output.append(headings)

        #add data from all table rows to output arr
        for row in rows:
            data = row.find_all("td")
            data.insert(0,row.find('th'))
            if len(data)==7:
                curr=[]
                for i in range(0,7):
                    datum=data[i].find(text=True)
                    curr.append(strip_non_ascii(datum))
                self.output.append(curr)

        #write output arr data to .csv file
        with open (self.outfile,'w') as csvfile:
            writer = csv.writer(csvfile,quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(self.output)
        print 'Data written in .csv format to file '+self.outfile+'.'
        csvfile.close()
        page.close()


        #write output arr data to .json file
        toJSON=[]
        for i in range(1,len(self.output)-1):
            entry={
                self.output[0][0]: self.output[i][0],
                self.output[0][1]: self.output[i][1],
                self.output[0][2]: self.output[i][2],
                self.output[0][3]: self.output[i][3],
                self.output[0][4]: self.output[i][4],
                self.output[0][5]: self.output[i][5],
                self.output[0][6]: self.output[i][6],
            }
            toJSON.append(entry)

        with open(self.outfileJ, 'w') as f:
            json.dump(toJSON, f,indent=2)
        print 'Data written in .json format to file '+self.outfileJ+'.'

    def states(self):
        print "Printing all states represented in data... \n"
        openfile=open(self.outfile, 'r')
        all_names = []
        lines=openfile.readlines()
        for line in lines:
            columns = line.split(',')
            all_names.append(columns[0])
        for i in range (1, len(all_names)-1):
            print all_names[i]
        return all_names[1:(len(all_names)-1)]
        openfile.close()

    def total_votes_by_party(self):
        print "\n Recalculating total votes by party... \n"
        votes=[0]*6
        openfile=open(self.outfile, 'r')
        lines=openfile.readlines()
        openfile.close()
        for line in lines[1:(len(lines)-1)]:
            columns=line.split(',')
            for i in range (1,7):
                if columns[i]!="-":
                    votes[i-1]+=int(columns[i])
        for i in range(0,6):
            print self.output[0][i+1] +": "+str(int(votes[i]))
        self.votes=votes
        print self.votes
        return self.votes

    def votes_by_percent(self):
        print "\n Calculating votes as percentage of electorate...\n"
        votes = self.votes
        percents=[]
        for i in range (0,5):
            p=float(votes[i])/votes[5]
            percents.append(p)
        for i in range(0,5):
            print self.output[0][i+1] +": "+str(percents[i]*100)+"%"
        return percents

def strip_non_ascii(string):
    #returns string without non-ascii characters; excludes '*'
    stripped = (c for c in string if 0 < ord(c) < 127 and ord(c)!=42)
    return ''.join(stripped)
