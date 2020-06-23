global robo

# demonstrate syntax error (observe the call of a non-existing robo method)

robo.right()
while not robo.frontIsWhite():
    robo.forward()
robo.idonotexist()
