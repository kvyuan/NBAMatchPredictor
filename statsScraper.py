# -*- coding: utf-8 -*-
"""
Main File: NBAMatchPredictor.py
This File: StatsScraper.py
Purpose: Retrive data from configured url and pre-process with beautifulsoup

@author: Hao Yuan
"""
import pandas as pd
import bs4 as bs
import urllib3
import certifi
import math

def getSoup(url):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    original = http.request('Get', url)
    soup = bs.BeautifulSoup(original.data, 'lxml')
    return soup

#Retrieve team stats: average offense score, average assistants, average opponet score
def getTeamStats(team):
    teamStats = []
    url = 'https://www.cbssports.com/nba/teams/stats/{}'.format(team)
    soup = getSoup(url)
    table = soup.find('table', class_= "data condensed borderTop title")
    #tr classes are messy on this page, so we collect all tr tags and get desired tr tag by index
    trs = table.find_all('tr')
    tds = trs[-2].find_all('td')
    #avgOffPts
    teamStats.append(float((tds[-1].text)))
    #avgAssis
    teamStats.append(float((tds[-6].text)))
    # home score
    tds = trs[-1].find_all('td')
    # avgDefPts
    teamStats.insert(1,float((tds[-1].text)))
    return teamStats

#Retrieve box score stats: last game score difference
def getGameScoreDiff(date, awayTeam, homeTeam):
    diff = []
    url = 'https://www.cbssports.com/nba/gametracker/boxscore/NBA_{}_{}@{}/'.format(date, awayTeam, homeTeam)
    soup = getSoup(url)
    table = soup.find('table', class_="team-stats")
    tr = table.find('tr')
    tds = tr.find_all('td')
    diff.append(math.fabs(int(tds[1].text) - int(tds[2].text)))
    print(diff)

#Retrive injury stats: 
