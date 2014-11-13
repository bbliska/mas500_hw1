from soupScrape import ElectionData
url='http://www.archives.gov/federal-register/electoral-college/2012/popular-vote.html'
outfile='2012_us_pres_election_data.csv'
outfileJ='2012_us_pres_election_data.json'
data=ElectionData(url,outfile,outfileJ)
#load module
data.load()
#list states represented in data
data.states()
#recalcate vote totals for each party
data.total_votes_by_party()
#calculate percent of popular vote captured by each party
data.votes_by_percent()