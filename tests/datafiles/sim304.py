global robo

# demonstrate syntax error (obseerve the runtime error)

robo.right()
while not robo.frontIsWhite():
    robo.forward(1/0)
