# Verify that data is being scraped, stored, and exported properly

from soupScrape import ElectionData
import unittest
import json

class ElectionDataTest(unittest.TestCase):

    def setUp(self):
        url='http://www.archives.gov/federal-register/electoral-college/2012/popular-vote.html'
        outfile='2012_us_pres_election_data_test.csv'
        outfileJ='2012_us_pres_election_data_test.json'
        self.data = ElectionData(url,outfile,outfileJ)

    def testLoad(self):
        self.data.load()
        assert self.data!=None
        assert self.data.output!=None
        assert self.data.outfile!=None
        assert self.data.outfileJ!=None

    def testStates(self):
        self.data.load()
        names = self.data.states()
        assert len(names)==51
        assert names[0]=='AL'
        assert names[1]=='AK'

    def testVotesByParty(self):
        self.data.load()
        partyVotes = self.data.total_votes_by_party()
        assert len(partyVotes)==6

    def testPercents(self):
        self.data.load()
        self.data.total_votes_by_party()
        percents = self.data.votes_by_percent()
        assert len(percents)==5

    def testCSV(self):
        self.data.load()
        csv= open(self.data.outfile, 'r')
        lines=csv.readlines()
        assert len(lines)>10

    def testJSON(self):
        self.data.load()
        jsonContents= open(self.data.outfileJ, 'r')
        jsonData=json.load(jsonContents)
        assert len(jsonData[0])==7
        


# if this file is run directly, run the tests
if __name__ == "__main__":
    unittest.main()