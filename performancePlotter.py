import matplotlib.pyplot as plt

#consulted https://matplotlib.org/3.1.1/gallery/pie_and_polar_charts/pie_features.html#sphx-glr-gallery-pie-and-polar-charts-pie-features-py
# as example code for plotting.
#plot pie charts for each matchup

#matchup is a 4-tuple (winsP1,winsP2,nameP1,nameP2)
#CONVENTIONS:
# P1 is always Random if Random is playing
# Random is black
# MonteCarlo is red
# AlphaBeta is cyan
# MiniMax is blue

def plotMatchup(matchup):
    """
    saves plot to disk

    PARAMETERS: 
    matchup 
    matchup is a 4-tuple (winsP1,winsP2,draws,nameP1,nameP2)

    RETURNS:
    None

    CONVENTIONS:
    P1 is always Random if Random is playing
    Random is black
    MonteCarlo is red
    AlphaBeta is cyan
    MiniMax is blue
    """
    #TODO: save plot
    winsP1,winsP2,draws,nameP1,nameP2 = matchup
    colorLst = []
    for i in range(2): #loop through names to keep consistent colors
        if matchup[i+3] == "Random":
            colorLst+= ['k']
        elif matchup[i+3] == "MonteCarlo":
            colorLst += ['r']
        elif matchup[i+3] == "AlphaBeta":
            colorLst += ['c']
        elif matchup[i+3] == "MiniMax":
            colorLst += ['b']
    colorLst += ['g']
    figure,ax = plt.subplots()
    ax.pie([winsP1,winsP2,draws],labels=[nameP1,nameP2,"Draw"],colors=colorLst)
    ax.axis('equal')

    filename = "{0}_{1}_{2}".format(nameP1,nameP2,str(winsP1+winsP2))
    plt.show()
    plt.savefig(fname=filename)

    
if __name__ == '__main__':
    plotMatchup([58,37,5,'AlphaBeta',"Random"])
