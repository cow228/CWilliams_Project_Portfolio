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

         

## Flop
### Solution 

## Manual Input Slow
### Solution

