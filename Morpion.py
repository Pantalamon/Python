#For the game board to print correctly, use the default font (Courier New)


def fconditions(size):
    '''Create strings that will be used as conditions in the winner() fonction'''
        
    condition1 ="game[0][0]"
    condition2 ="game[0]["+str(size-1)+"]"
    condition3="game[0][i]"
    condition4="game[i][0]"
    #Allows to add an "==" condition depending on the size of the board. Indexes also vary accordingly.
    for j in range(size-1):
            condition1 = condition1 + " == game["+str(j+1)+"]["+str(j+1)+"]"
            condition2 = condition2 + " == game["+str(j+1)+"]["+str(size-(j+2))+"]"
            condition3 =  condition3 + " == game["+str(j+1)+"][i]"
            condition4 = condition4 + " == game[i]["+str(j+1)+"]"
    return condition1,condition2,condition3,condition4
        
def winner(game,size,conditions):
        ''' this function will evaluate each turn if someone has won the game based on the list, the conditions given by fcondition() and the size of the board.
        It returns the number of the winner.'''
        a=0
        condition1,condition2,condition3,condition4 = conditions
        if size<7:              
                #eval() allows to take the string as an argument and uses it's content as condition for the if.
                if eval(condition1) and game[0][0]!=0:
                        a=game[0][0]
                elif eval(condition2)and game[0][size-1]!=0:
                        a=game[0][size-1]
                        print("ça marche!")
                for i in range(size-1):
                        if eval(condition3) and game[0][i]!=0:
                                a=game[0][i]
                        elif eval(condition4) and game[i][0]!=0:
                                a=game[i][0]

        return a

'''winner([[1,1,0,1],
         [1,1,0,0],
         [1,1,0,0],
         [1,0,0,0]],4)'''

def table():
    '''table() is called at the beginning of the game. It creates the items that will be manipulated:
    The list that will contain the evolution of the game, the string that is a visual representation of the game board for the player and the size of the game board.
    
    '''
    x=7
    while x>6:
            x=int(input("Hello!\nHow many tiles do you want for the side of your gameboard? 6 tiles max"))
            if x>6:
                    print("6 tiles max!")
        
    visuel=(" ---" * x +"   "+ "\n" + "|   " * x + "|  \n") * x + " ---" * x +" "
    margin=[str(j+1) for j in range(x)]

    fringe = "  "
    for k in margin:
            fringe+=k+"   "
    sizeline=(4*x+4)*2
    #To insert the margin
    for i in range(1,x+1):
        print(i)
        visuel= visuel[:sizeline*i-2] + str(i) + visuel[sizeline*i-1:]
        print(visuel)
    liste=[]
    liste.append([[0 for i in range(x)] for i in range(x)])
    liste=liste[0]
    return (visuel,liste,x,fringe)

def jeu(table):
        print('''\nTo play, please enter the number of the column first, then a space and finally the number of the line
        Example: If you want to set your pawn on the fourth column of the second line, type: 4 2''')
        print("Player 1 you play with the X and Player 2 with the O!")

        tab,game,size,contour=table
        conditions=fconditions(size)
        a=1
        count=0
        print(contour)
        print(tab)
        while count < size*size:

                        #print(game)
                        chaine=input("player {} ,it's your turn\n".format(a))
                        try:
                            tup=chaine.split(" ")
                            col=int(tup[0])-1
                            lig=int(tup[1])-1
                            sizeligne=4*size+4
                            position=sizeligne+2+sizeligne*lig*2+(4*col)
                            #Every turn, the visual game board will be updated based on the list in the background
                            #The Pawn of the player is inserted in the fitting position
                            if game[lig][col]==0:
                                if a==1:
                                    game[lig][col]=1
                                    tab = tab[:position] + "X" + tab[position + 1:]
                                    a=2
                                else:
                                        game[lig][col]=2
                                        tab = tab[:position] + "O" + tab[position + 1:]
                                        a=1
                            else:
                                print("This square is already taken!")
                                continue
                        except:
                            print("Invalid!Enter with the format : column line")
                            continue
                        count+=1
                        print(contour)
                        print(tab)
                        b=winner(game,size,conditions)
                        print(b)
                        if b==1:
                                print("Player 1 has won!GG")
                                print(count , " moves have been made!")
                                break
                        elif b==2:
                                print("Player 2 has won!GG")
                                print(count , " have been made!")
                                break
                        elif b==0 and count >= size**2:
                                print("It's a draw!")
                                print(count , " have been made!")
                                break
                                
        print("thank you for playing")                    
                        
jeu(table())