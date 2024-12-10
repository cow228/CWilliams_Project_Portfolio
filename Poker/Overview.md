# Poker Analytics
## Project Goal
Create a tool that will provide insight into poker strategy and analytics while playing online.  
Determining the best action at any given game state in poker requires a mixture of memorization and quick mental math.
This program aims to reduce the need for these difficult methods and simplify the decision process


## Preflop
Ideal preflop strategy depends on your position at the table, your hand, the size of your chip stack and the action of all the players before you.  This can lead to particularly complicated rules that need to be memorized for the best play.  The image below is a "simplified" range of actions to take when in the small blind. 
<br>
![Example Preflop Ranges](/Poker/images/SB_Strat.png)
### Solution
Based on the players hand and position at the table this information can be looked up quickly through coding.  Step:
1. Store range information in an excel file to be referenced by the program
   1. Based on strategy information here: Poker/Reference/online-6max-gto-charts.pdf
   2. store action information in easily readable excel table here: Poker/Reference/ranges.xlsx
   3. To make information readable store all actions posible for a given cell as one number.  Store action against different situations in decimal places.  information can be extracted by code later using modulo division - the table below would result in a value of 1.01
   4. | Action fold to you | Against BTN Raise | Against SB Limp |
      |--------------------|-------------------|-----------------|
      | Raise | Fold | Raise |
      | 1 | 0 | 1 |
4. Input player hand and position
5. Output actions to take against possible action before you
![Example Preflop Ranges](/Poker/images/Preflop_Output.png)

<br>
Code References: <br>
_Determine Preflop Action_ <br>



## Flop
Determining the ideal action on the flop requires determing which of your hands are in the category "Premium", "Marginal", "Draw", or "Junk" based on the range of hands you could have gotten to the flop with (based on preflop strategy) and the flop itself.  These ranks are not fixed, but each hand is categorized based on all the others.  For example, if you considered one pair premium and that meant that 30% of your possible hands would be premium you would want to reduce this so that only two pair is premium and your total premium hands are 15%.  Then you find the range of hands that give you a percent of draw hands that are proportional to premiums.  Lastly the left over hands should be divided between Marginal and Junk in a 70:30 ratio. 
<br>
This analysis is very difficult to do mentally at the table with a time limit.  
### Solution 
Calculate the percentages automatically based on the range of hands, and the flop:
1. Need to create a list of possible hands.  All the possible hands that you could get to the flop with (e.g. not fold preflop) combined with the actual flop cards
2. Assign a rank to each of the hands in that list - assign based on standard poker hand ranks.  This process takes quite a long time since there are up to 22,100 possible hands and >3500 different ranks (accounting for AKQJT flush is better than AKQJ2 for example)
3. Assign a draw value to each hand - draws are not made hands, but ones that are close e.g. 4 cards to a flush
   1. Start by assigning each type of draw a point value based on it's liklihood (180 for 4 to a flush, 30 for gutshot straight draw)
   2. Add the rank of the draw to that value, Ace Flush is higher than K Flush
   3. Calculate which categories each hand satisfies, it can satisfy more than one (4 to flush, 3 to flush, Open ended straight, Gut Shot straight, 3 to a straight, Over Card )
   4. Add up the rank of the all the draws the hand could be
5. Find cutoff values for appropriate card rank percentages on the flop
   1. Start by finding premium cutoff
      1. Start by assuming that top pair (pair that matches with highest card on the board) is the lowest premium hand, calculate the percent this would include
      2. Calculate the board's "wetness" (measure of how likely other hands are to combine well with the flop)
         1. Redo the rankings from step 2, but do them with all possible hole cards
         2. Calculate the percent of hands that would be premium if assuming top pair is lowest premium
         3. If this percent is greater than 17% consider the board wet
      4. if the board is wet subtract the percent found in step 4.i.a by (wetness% - 12) set this as the % target for next step
      5. find the lowest cutoff that yeilds a percent less than new target
   2. Find the draw cutoff
      3. set draw cutoff target percent to be equal to percent of premiums
      4. find the percent of draws of every draw value in the list, take the one closest to target
   5. Find marginal cutoff
      6. set marginal cutoff target percent equal to 70% of remaining hands after draws and premiums are taken out
      7. find the percent that every marginal rank would have
      8. find the largest change in that percent - this indicates a natural cutoff point
      9. find which side of that cutoff point is closer to the goal and set that as marginal cutoff
   10. leftover hands are junk
11. Plot hands on a readable chart
   12. Each cell is color coded based on which type of hand it is
   13. some cells are split since each cell contains multiple hands.  the proprtion of color is equal to the proportion of hands in that cell in that category
   14. Determine what category the actual hole cards are in

![Example Flop Output](/Poker/images/Flop_output.png)
<br>
Code References: <br>
_Rank Hands_ <br>
_Determine Hand Types_ <br>
_Create Chart_


## Manual Input Slow
### Solution

## Rank Calculation Slow
### Solution

