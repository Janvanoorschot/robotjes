

def execute(robo):
    for i in range(10):
        while not robo.frontIsObstacle():
            robo.forward()
        robo.right()
        robo.right()
        while not robo.frontIsObstacle():
            robo.forward()
