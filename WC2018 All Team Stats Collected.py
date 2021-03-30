import seaborn as sns
import pandas as pd
from pandas import json_normalize
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl
import matplotlib.mlab as mlab
import matplotlib.lines as mlines
from collections import Counter

###Load World Cup 2018 Data
competition_id = 43
with open(r'C:\Users\cherr\PycharmProjects\soccerm8/Statsbomb/data/matches/'+str(competition_id)+'/3.json') as f:
    matches = json.load(f)
#Create Complete Match List
matchlist = []
for match in matches:
    matchlist.append(match['match_id'])

###########################
########## PASSES #########
###########################
print("Passes")
#Actions
success = []
failed = []
highpass = []
#Gamesplayed = Recorded instance (playername + matchid) of game where player was involved, gamesplayedcheck = unique recording of games involved
gamesplayed = []
gamesplayedcheck = []

#Setting up for "Total Pass Length" collection
teamdf = {'Team':['Denmark','Croatia','Nigeria','Iceland','Poland','Colombia','Costa Rica','Brazil','Mexico','Germany','Peru',
          'Australia','Serbia','Senegal','Panama','Tunisia','Switzerland','France','Russia','Uruguay','Belgium',
          'Japan','Argentina','Egypt','Spain','Saudi Arabia','South Korea','Morocco','Portugal','Iran','England',
          'Sweden']
          }
passlength = pd.DataFrame(teamdf,columns = ['Team','Total Pass Length'])
passlength = passlength.rename(columns={'index':'Team', 0:'Total Pass Length'})
# passlength['Previous Pass Length'] = 0
# passlength['Current Pass Length'] = float(0)
passlength['Total Pass Length'] = float(0)
#Reset progress value visualizer
j = 0

for i in range(len(matchlist)):
    match_id_required = matchlist[i]
    file_name = str(match_id_required) + ".json"
    with open(r"C:\Users\cherr\PycharmProjects\soccerm8/Statsbomb/data/events/" + file_name,encoding='utf-8') as data_file:
        # print (mypath+'events/'+file)
        data = json.load(data_file)
    #event data
    df = json_normalize(data, sep="_").assign(match_id=file_name[:-5])
    passes = df.loc[df['type_name'] == 'Pass'].set_index('id')
    j = j+0.5
    print(j)

    for i, thepass in passes.iterrows():
        success.append(thepass['team_name'])
        if str(thepass['team_name'])+str(thepass['match_id']) not in gamesplayedcheck:
            gamesplayed.append(thepass['team_name'])
            gamesplayedcheck.append(str(thepass['team_name'])+str(thepass['match_id']))
        else:
            pass
        if thepass['pass_height_name'] == 'High Pass':
            highpass.append(thepass['team_name'])
        else:
            pass

        #Goes through passlength dataframe to set up to assign passlength value for this specific pass
        for i, plength in passlength.iterrows():
            if plength['Team'] == thepass['team_name']:
                runningtotal = passlength['Total Pass Length']
            else:
                pass
        #Set up pass name for following code
        teamname = thepass['team_name']
        passlength.loc[passlength['Team']== thepass['team_name'],['Total Pass Length']] = (thepass['pass_length'] + runningtotal)
    j = j+0.5
    print(j)

#Counts tackle and gamecount lists and assigns to player (Counter())
actioncount = Counter(success)
gamecount = Counter(gamesplayed)
highpasscount = Counter(highpass)

#Change Counter value into dataframes, set column labels
successfulaction = pd.DataFrame.from_dict(actioncount, orient='index').reset_index()
successfulaction = successfulaction.rename(columns={'index':'Team', 0:'Total Passes'})
totalgames = pd.DataFrame.from_dict(gamecount, orient='index').reset_index()
totalgames = totalgames.rename(columns={'index':'Team', 0:'Games Played'})
totalhighpass = pd.DataFrame.from_dict(highpasscount, orient='index').reset_index()
totalhighpass = totalhighpass.rename(columns={'index':'Team', 0:'Total High Pass'})

#Combine Data Frames on 'players' column, create Per Game column which is Tackles per games played
combine1 = pd.merge(totalgames,successfulaction,on='Team')
combine2 = pd.merge(combine1, totalhighpass, on = 'Team')
combine = pd.merge(combine2,passlength, on = 'Team')
combine['Passes pG'] = combine['Total Passes'].divide(combine['Games Played'])
combine['High Pass Average'] = combine['Total High Pass'].divide(combine['Total Passes'])
combine['Pass Length Average'] = combine['Total Pass Length'].divide(combine['Total Passes'])
#print(combine)

###########################
########## SHOTS ##########
###########################
print("Shots")
#Actions
success = []
goal = []
openplayshot = []
#Gamesplayed = Recorded instance (playername + matchid) of game where player was involved, gamesplayedcheck = unique recording of games involved
gamesplayed = []
gamesplayedcheck = []
j = 0

for i in range(len(matchlist)):
    match_id_required = matchlist[i]
    file_name = str(match_id_required) + ".json"
    with open(r"C:\Users\cherr\PycharmProjects\soccerm8/Statsbomb/data/events/" + file_name,encoding='utf-8') as data_file:
        # print (mypath+'events/'+file)
        data = json.load(data_file)
    #event data
    df = json_normalize(data, sep="_").assign(match_id=file_name[:-5])
    passes = df.loc[df['type_name'] == 'Pass'].set_index('id')
    shots = df.loc[df['type_name'] == 'Shot'].set_index('id')
    j = j+0.5
    print(j)

    for i, thepass in passes.iterrows():
        if str(thepass['team_name'])+str(thepass['match_id']) not in gamesplayedcheck:
            gamesplayed.append(thepass['team_name'])
            gamesplayedcheck.append(str(thepass['team_name'])+str(thepass['match_id']))
        else:
            pass

    for i, shot in shots.iterrows():
        if shot['minute'] > 120:
            pass
        else:
            success.append(shot['team_name'])

        if shot['shot_type_name'] == 'Open Play':
            openplayshot.append(shot['team_name'])
        else:
            pass
        if shot['shot_outcome_name'] == 'Goal':
            #Remove Penalties scored from shootouts
            if shot['minute'] > 120:
                pass
            else:
                goal.append(shot['team_name'])
    j = j+0.5
    print(j)
#Counts tackle and gamecount lists and assigns to player (Counter())
actioncount = Counter(success)
gamecount = Counter(gamesplayed)
goalcount = Counter(goal)
openplayshotcount = Counter(openplayshot)

#Change Counter value into dataframes, set column labels
successfulaction = pd.DataFrame.from_dict(actioncount, orient='index').reset_index()
successfulaction = successfulaction.rename(columns={'index':'Team', 0:'Total Shots'})
totalgames = pd.DataFrame.from_dict(gamecount, orient='index').reset_index()
totalgames = totalgames.rename(columns={'index':'Team', 0:'Games Played'})
totalgoal = pd.DataFrame.from_dict(goalcount, orient='index').reset_index()
totalgoal = totalgoal.rename(columns={'index':'Team', 0:'Total Goals'})
totalopenplayshot = pd.DataFrame.from_dict(openplayshotcount,orient='index').reset_index()
totalopenplayshot = totalopenplayshot.rename(columns={'index':'Team',0:'Total Open Play Shots'})

#Combine Data Frames on 'players' column, create Per Game column which is Tackles per games played
combineshot1 = pd.merge(totalgames,successfulaction,on='Team')
combineshot2 = pd.merge(combineshot1,totalopenplayshot,on='Team')
combineshot = pd.merge(combineshot2,totalgoal, on='Team')
combineshot['Goals per Shot'] = combineshot['Total Goals'].divide(combineshot['Total Shots'])
combineshot['Shots pG'] = combineshot['Total Shots'].divide(combineshot['Games Played'])
combineshot['Open Play per Shot'] = combineshot['Total Open Play Shots'].divide(combineshot['Total Shots'])

#Combine shot and pass dataframes
combineshotpass = pd.merge(combine,combineshot, on='Team')

# print(combineshotpass)

###########################
########## DEFENSE ########
###########################
print("Defense")
#Actions
successDEF = []
#Gamesplayed = Recorded instance (playername + matchid) of game where player was involved, gamesplayedcheck = unique recording of games involved
gamesplayed = []
gamesplayedcheck = []
j = 0

for i in range(len(matchlist)):
    match_id_required = matchlist[i]
    file_name = str(match_id_required) + ".json"
    with open(r"C:\Users\cherr\PycharmProjects\soccerm8/Statsbomb/data/events/" + file_name,encoding='utf-8') as data_file:
        # print (mypath+'events/'+file)
        data = json.load(data_file)
    #event data
    df = json_normalize(data, sep="_").assign(match_id=file_name[:-5])
    passes = df.loc[df['type_name'] == 'Pass'].set_index('id')
    duel = df.loc[df['type_name'] == 'Duel'].set_index('id')
    block = df.loc[df['type_name'] == 'Block'].set_index('id')
    clearance = df.loc[df['type_name'] == 'Clearance'].set_index('id')
    intercept = df.loc[df['type_name'] == 'Interception'].set_index('id')
    ballrecovery = df.loc[df['type_name'] == 'Ball Recovery'].set_index('id')
    j = j+0.5
    print(j)
    for i, thepass in passes.iterrows():
        if str(thepass['team_name'])+str(thepass['match_id']) not in gamesplayedcheck:
            gamesplayed.append(thepass['team_name'])
            gamesplayedcheck.append(str(thepass['team_name'])+str(thepass['match_id']))
        else:
            pass
    #Clearances
    for i,clr in clearance.iterrows():
        successDEF.append((clr['team_name']))
    #Ball Recovery
    for i, br in ballrecovery.iterrows():
        if br['ball_recovery_recovery_failure'] == True:
            pass
        else:
            successDEF.append((br['team_name']))
            # if br['position_name'] == "Goalkeeper":
            #     pass
            # else:
            #     success.append((br['player_name']))
    #Intercepts
    for i, intcpt in intercept.iterrows():
        successDEF.append((intcpt['team_name']))
        # if intcpt['interception_outcome_name'] == "Won" or intcpt['interception_outcome_name'] == "Success In Play" or intcpt['interception_outcome_name'] == "Success Out" or intcpt['interception_outcome_name'] == "Lost Out":
        #     success.append((intcpt['player_name']))
        # else:
        #     pass
    # Blocks
    for i, blk in block.iterrows():
        successDEF.append((blk['team_name']))
    #Tackles
    for i, tckl in duel.iterrows():
        if tckl['duel_type_name'] == "Tackle":
            successDEF.append((tckl['team_name']))
            # if tckl['duel_outcome_name'] == "Won" or tckl['duel_outcome_name'] == "Success In Play" or tckl['duel_outcome_name'] == "Success Out" or tckl['duel_outcome_name'] == "Lost Out":
            #     success.append((tckl['player_name']))
            # else:
            #     pass
        else:
            successDEF.append((tckl['team_name']))
    j = j+0.5
    print(j)
#Counts tackle and gamecount lists and assigns to player (Counter())
actioncount = Counter(successDEF)
gamecount = Counter(gamesplayed)

#Change Counter value into dataframes, set column labels
successfulaction = pd.DataFrame.from_dict(actioncount, orient='index').reset_index()
successfulaction = successfulaction.rename(columns={'index':'Team', 0:'Total Defensive Actions'})
totalgames = pd.DataFrame.from_dict(gamecount, orient='index').reset_index()
totalgames = totalgames.rename(columns={'index':'Team', 0:'Games Played'})

#Combine Data Frames on 'players' column, create Per Game column which is Tackles per games played
combineDEF = pd.merge(totalgames,successfulaction,on='Team')
combineDEF['DEF Act per Game'] = combineDEF['Total Defensive Actions'].divide(combineshot['Games Played'])

#Combine shot and pass dataframes
combinetotal = pd.merge(combineshotpass,combineDEF)
print(combinetotal)
combinetotal.to_excel('Unnormalized_WC2018Data.xlsx')


