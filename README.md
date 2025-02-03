A board game between an autonomous agent. Implements the minimax and alpha-beta pruning algorithms from the book by Russell and Norvig 'Artificial Intelligence: A Modern Approach'

To play the game, run the gamePlay.py script, the board will be shown in the command line. 

If you want to play against the agent, you will need to submit a responce in the format [pawn position][direction to move][how many steps to move].

The pawn position is written as the the x ----> and y | position on the board (start counting from 1)
                                                      |
                                                      V

The direction is given by the character N, S, E and W (north, south, east, and west)

The number of steps to take is limitted by how many opponent pawns surround each of your pawns. Neighbouring pawns are any opponent pawn directly beside or diagnal to your pawn. Each opponent pawn in the neighbourhood restricts the pawn's movement by 1 starting from 3. For example this X pawn: <br>
O, _ , _ <br>
 _ , X , O <br>
 _ , _ , _  <br>
 has 2 opponent pawns, so it can only make 3 - 1 - 1 = 1 steps in the available directions

You cannot select to play a pawn that is not your own, or move the pawn to a location with another pawn. 

For example, if this is your board, and you are player X:
 _ , X , X , _ , _ , _ , _ <br>
 _ , _ , _ , X , _ , _ , _ <br>
 O , _ , _ , _ , _ , _ , _ <br>
 O , O , _ , _ , _ , _ , O <br>
  _  ,  _  , O  ,  _  ,  _ , _  , O <br>
 _ , _ , _ , _ , X , _ , _  <br>
 _ , _ , _ , _ , X , X , _ <br>

You might want to move the pawn at x = 4, y = 2 to the right (W) 2 steps. Since there the spot is free and you have no opponent pawns resistricting your movement, you are free to move up to 3 steps. Your response here would be:

42W2

And the resulting board would be: <br>
 _ , X , X , _ , _ , _ , _ <br>
 _ , _ , _ , _ , _ , X , _ <br>
 O , _ , _ , _ , _ , _ , _ <br>
 O , O , _ , _ , _ , _ , O <br>
_ , _ , O , _ , _ , _ , O <br>
 _ , _ , _ , _ , X , _ , _ <br>
  _ , _ , _ , _ , X , X , _ <br>
