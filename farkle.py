#!/usr/bin/env python

#External modules
import os
from random import randint
from collections import Counter

#Settings
fewestDiceToRoll = 3 #the risk factor! don't roll fewer than this, lest you farkle

#Let's go!
try:
    while 1: #loop of turns
        rolls = 0
        dice = [0,0,0,0,0,0]
        points = 0
        kept = False

        while 1: #loop of rolls per turn
            #roll dice in the set
            if(rolls==0): os.system('clear')
            else: print('')
            rolls += 1
            for i in range(0,len(dice)):
                dice[i] = randint(1,6)
            print('ROLL #'+str(rolls)+': '+str(dice));

            #analyze results and see if we want to keep any
            kept = False

            #is there a flush?
            if len(Counter(dice)) == 6: #six discrete dice values counted
                points += 1500
                print('   Found a flush! Turn score: '+str(points));
                #Keep all and start over
                continue
                dice = [] #remove all six dice
                kept = True
                #TEST: 132465

            #is there three pair?
            ctPairs = Counter(dice) #get counts per dice value
            for i in list(ctPairs):
                if ctPairs[i] < 2:
                    del ctPairs[i] #drop counts below 2
            if len(ctPairs) == 3: #if there are three such counts
                points += 750
                print('   Found three pair! Turn score: '+str(points));
                dice = []
                kept = True
                #TEST: 154415

            #is there three (or more) of a kind?
            while 1: #loop because this condition could be met twice
                ctTrips = Counter(dice)
                for i in list(ctTrips):
                    if ctTrips[i] < 3:
                        del ctTrips[i] #drop counts below 3
                if len(ctTrips) > 0: #got (at least) one!
                    val = list(ctTrips)[0]
                    ct = ctTrips[val]
                    scr = val * 100 * pow(2,ct-3) #ex: five 4s: 4*100*pow(2,5-3) = 4*100*4 = 1600
                    if(val==1): scr *= 10 #three 1s are 1000
                    points += scr
                    ctWord = 'three'
                    if ct == 4: ctWord = 'four'
                    if ct == 5: ctWord = 'five'
                    if ct == 6: ctWord = 'six'
                    print('   Found '+ctWord+' '+str(val)+'s! Turn score: '+str(points));
                    #remove all of val - needs [:]?
                    dice = [x for x in dice if x != val]
                    kept = True
                else:
                    break
            #TEST: 331345 #three 3s
            #TEST: 414454 #four 4s
            #TEST: 565555 #five 5s
            #TEST: 331311 #three 3s and three 1s - should loop twice

            #Now for counters, if there are any
            onlyCtrs = [x for x in dice if x==1 or x==5]
            if len(onlyCtrs) > 0:
                #If all remaining dice are counters, take them all
                if len(onlyCtrs) == len(dice):
                    for val in onlyCtrs:
                        if(val==1): points += 100
                        else: points += 50
                    print('   All the rest are counters! Turn score: '+str(points));
                    dice = []
                    kept = True

                #Or, if we haven't kept anything yet, and keeping one counter would allow enough to roll again, do that, and take 1 before 5
                elif kept == False and len(dice) > fewestDiceToRoll:
                    if 1 in dice:
                        points += 100
                        print('   Taking a 1 counter. Turn score: '+str(points));
                        for x in dice:
                            if x == 1:
                                dice.remove(x)
                                break #only remove one
                        kept = True
                    elif 5 in dice:
                        points += 50
                        print('   Taking a 5 counter. Turn score: '+str(points));
                        for x in dice:
                            if x == 5:
                                dice.remove(x)
                                break #only remove one
                        kept = True

                #If we have or have not kept anything, but don't have enough to roll again, take them all
                elif (kept == False and len(dice) <= fewestDiceToRoll or kept == True and len(dice) < fewestDiceToRoll):
                    for val in onlyCtrs:
                        if(val==1): points += 100
                        else: points += 50
                    print('   Taking all the counters. Turn score: '+str(points));
                    dice = [x for x in dice if x!=1 and x!=5]
                    kept = True
            #end if we have counters

            #if we still haven't kept anything, we farkled
            if kept == False:
                #did you farkle at the start?
                if(rolls==1 and len(dice)==6):
                    points += 250
                    print('   Farkle at the start of turn! Turn score: '+str(points))
                else:
                    points = 0
                    print('   Farkled!')
                break #end the turn

            #if we did keep something, decide whether to continue
            if len(dice) == 0: #restore all six dice for next roll
                print("   Roll 'em all again!")
                dice = [0,0,0,0,0,0]
            elif len(dice) < fewestDiceToRoll:
                print("   That leaves "+str(len(dice))+" di"+('' if len(dice)==1 else 'c')+"e, so ending turn here.")
                break; #end the turn

        #end loop of rolls
        print('')
        print('Final turn score: '+str(points))
        print('')
        raw_input("Press return to do another turn, or Ctrl+C to quit:")
    #end loop of turns

except KeyboardInterrupt:
    print("\r\nBye!")
#end try/except/finally