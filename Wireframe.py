'''
Written by Andy Lepetri
Wireframe skeleton from: Peter Collingridge's work
Arbitrary axial rotation formula from: http://inside.mines.edu/fs_home/gmurray/ArbitraryAxisRotation/

Controls:

Up Arrow     is move forward
Down Arrow   is move backward
Left Arrow   is move left
Right Arrow  is move right
2            is move up
1            is move down
Q            is pitch up
W            is pitch down
S            is roll right
A            is roll left
X            is yaw right
Z            is yaw left
'''

import pygame
import numpy as np
import math

key_to_function = {
    pygame.K_LEFT: (lambda x: x.translateAll('LEFT',10)),
    pygame.K_RIGHT:(lambda x: x.translateAll('RIGHT',10)),
    pygame.K_DOWN: (lambda x: x.translateAll('BACKWARD',10)),
    pygame.K_UP:   (lambda x: x.translateAll('FORWARD',10)),
    pygame.K_1:    (lambda x: x.translateAll('UP',10)),
    pygame.K_2:    (lambda x: x.translateAll('DOWN',10)),
    pygame.K_q:    (lambda x: x.rotateAll('PITCH',  0.1)),
    pygame.K_w:    (lambda x: x.rotateAll('PITCH', -0.1)),
    pygame.K_a:    (lambda x: x.rotateAll('ROLL',  -0.1)),
    pygame.K_s:    (lambda x: x.rotateAll('ROLL', 0.1)),
    pygame.K_z:    (lambda x: x.rotateAll('YAW',  -0.1)),
    pygame.K_x:    (lambda x: x.rotateAll('YAW', 0.1))}

class Wireframe:
    def __init__(self):
        self.nodes = np.zeros((0, 4))
        self.edges = []

    def addNodes(self, node_array):
        ones_column = np.ones((len(node_array), 1))
        ones_added = np.hstack((node_array, ones_column))
        self.nodes = np.vstack((self.nodes, ones_added))

    def addEdges(self, edgeList):
        self.edges += edgeList

    def outputEdges(self):
        print("\n --- Edges --- ")
        for i, (node1, node2) in enumerate(self.edges):
            print("   %d: %d -> %d" % (i, node1, node2))

    def outputNodes(self):
        print("\n --- Nodes --- ")
        for i, (x, y, z, _) in enumerate(self.nodes):
            print("   %d: (%d, %d, %d)" % (i, x, y, z))

    def transform(self, matrix):
        """ Apply a transformation defined by a given matrix. """
        self.nodes = np.dot(self.nodes, matrix)


    def rotateAll(self, a, b, c, u, v, w, pheta):
        """ Updates nodes to rotate over a given axis. """
        for i, (x, y, z, _) in enumerate(self.nodes):
            self.nodes[i][0] = ((a*((v**2)+(w**2))-u*(b*v+c*w-u*x-v*y-w*z))*(1-np.cos(pheta))+x*np.cos(pheta)+(-c*v+b*w-w*y+v*z)*np.sin(pheta))
            self.nodes[i][1] = ((b*((u**2)+(w**2))-v*(a*u+c*w-u*x-v*y-w*z))*(1-np.cos(pheta))+y*np.cos(pheta)+(c*u-a*w+w*x-u*z)*np.sin(pheta))
            self.nodes[i][2] = ((c*((u**2)+(v**2))-w*(a*u+b*v-u*x-v*y-w*z))*(1-np.cos(pheta))+z*np.cos(pheta)+(-b*u+a*v-v*x+u*y)*np.sin(pheta))

    def translationMatrix(self, dx=0, dy=0, dz=0):
        """ Return matrix for translation along vector (dx, dy, dz). """

        matrix = np.array([[1,0,0,0],
                           [0,1,0,0],
                           [0,0,1,0],
                           [dx,dy,dz,1]])
        return matrix

    def unitVectorFront(self):
        """ Returns unit vector in front direction. """
        EF = self.nodes[5]-self.nodes[4]
        EG = self.nodes[6]-self.nodes[4]
        orthognal = np.array([(EF[1]*EG[2]-EG[1]*EF[2]), (EG[0]*EF[2]-EF[0]*EG[2]), (EF[0]*EG[1]-EG[0]*EF[1])])
        unit = -orthognal/math.sqrt((orthognal[0]**2)+(orthognal[1]**2)+(orthognal[2]**2))
        return unit

    def unitVectorBack(self):
        """ Returns unit vector in back direction. """
        AC = self.nodes[2]-self.nodes[0]
        AB = self.nodes[1]-self.nodes[0]
        orthognal = np.array([(AC[1]*AB[2]-AB[1]*AC[2]), (AB[0]*AC[2]-AC[0]*AB[2]), (AC[0]*AB[1]-AB[0]*AC[1])])
        unit = -orthognal/math.sqrt((orthognal[0]**2)+(orthognal[1]**2)+(orthognal[2]**2))
        return unit

    def unitVectorLeft(self):
        """ Returns unit vector in left direction. """
        AB = self.nodes[1]-self.nodes[0]
        AE = self.nodes[4]-self.nodes[0]
        orthognal = np.array([(AB[1]*AE[2]-AE[1]*AB[2]), (AE[0]*AB[2]-AB[0]*AE[2]), (AB[0]*AE[1]-AE[0]*AB[1])])
        unit = -orthognal/math.sqrt((orthognal[0]**2)+(orthognal[1]**2)+(orthognal[2]**2))
        return unit

    def unitVectorRight(self):
        """ Returns unit vector in right direction. """
        CG = self.nodes[6]-self.nodes[2]
        CD = self.nodes[3]-self.nodes[2]
        orthognal = np.array([(CG[1]*CD[2]-CD[1]*CG[2]), (CD[0]*CG[2]-CG[0]*CD[2]), (CG[0]*CD[1]-CD[0]*CG[1])])
        unit = -orthognal/math.sqrt((orthognal[0]**2)+(orthognal[1]**2)+(orthognal[2]**2))
        return unit

    def unitVectorTop(self):
        """ Returns unit vector in top direction. """
        BD = self.nodes[3]-self.nodes[1]
        BF = self.nodes[5]-self.nodes[1]
        orthognal = np.array([(BD[1]*BF[2]-BF[1]*BD[2]), (BF[0]*BD[2]-BD[0]*BF[2]), (BD[0]*BF[1]-BF[0]*BD[1])])
        unit = -orthognal/math.sqrt((orthognal[0]**2)+(orthognal[1]**2)+(orthognal[2]**2))
        return unit

    def unitVectorBottom(self):
        """ Returns unit vector in bottom direction. """
        AE = self.nodes[4]-self.nodes[0]
        AC = self.nodes[2]-self.nodes[0]
        orthognal = np.array([(AE[1]*AC[2]-AC[1]*AE[2]), (AC[0]*AE[2]-AE[0]*AC[2]), (AE[0]*AC[1]-AC[0]*AE[1])])
        unit = -orthognal/math.sqrt((orthognal[0]**2)+(orthognal[1]**2)+(orthognal[2]**2))
        return unit

    def unitVectorYawCenter(self):
        """ Returns unit vector and point of yaw center axis. """
        AB = self.nodes[1]-self.nodes[0]
        AG = self.nodes[6]-self.nodes[0]
        point = (AG/2)+self.nodes[0]
        axis = AB
        unit = axis/math.sqrt((axis[0]**2)+(axis[1]**2)+(axis[2]**2))
        return point, unit

    def unitVectorPitchCenter(self):
        """ Returns unit vector and point of pitch center axis. """
        AF = self.nodes[5]-self.nodes[0]
        AC = self.nodes[2]-self.nodes[0]
        point = (AF/2)+self.nodes[0]
        axis = AC
        unit = axis/(math.sqrt(((axis[0])**2)+((axis[1])**2)+((axis[2])**2)))
        return point, unit

    def unitVectorRollCenter(self):
        """ Returns unit vector and point of roll center axis. """
        AD = self.nodes[3]-self.nodes[0]
        AE = self.nodes[4]-self.nodes[0]
        point = (AD/2)+self.nodes[0]
        axis = AE
        unit = axis/(math.sqrt(((axis[0])**2)+((axis[1])**2)+((axis[2])**2)))
        return point, unit

class ProjectionViewer:
    """ Displays 3D objects on a Pygame screen """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Wireframe Display')
        self.background = (10,10,50)

        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = True
        self.nodeColour = (255,255,255)
        self.edgeColour = (200,200,200)
        self.nodeRadius = 4

    def addWireframe(self, name, wireframe):
        """ Add a named wireframe object. """

        self.wireframes[name] = wireframe

    def run(self):
        """ Create a pygame screen until it is closed. """

        running = True
        pygame.key.set_repeat(50,50)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_to_function:
                        key_to_function[event.key](self)

            self.display()
            pygame.display.flip()

    def display(self):
        """ Draw the wireframes on the screen. """

        self.screen.fill(self.background)

        for wireframe in self.wireframes.values():
            if self.displayEdges:
                pygame.draw.aaline(self.screen, (0,255,0), (int(400+(wireframe.nodes[0][0]-400)*(1-wireframe.nodes[0][2]/1000)), int(300+(wireframe.nodes[0][1]-300)*(1-wireframe.nodes[0][2]/1000))), (int(400+(wireframe.nodes[1][0]-400)*(1-wireframe.nodes[1][2]/1000)), int(300+(wireframe.nodes[1][1]-300)*(1-wireframe.nodes[1][2]/1000))), 1)
                pygame.draw.aaline(self.screen, (0,255,0), (int(400+(wireframe.nodes[1][0]-400)*(1-wireframe.nodes[1][2]/1000)), int(300+(wireframe.nodes[1][1]-300)*(1-wireframe.nodes[1][2]/1000))), (int(400+(wireframe.nodes[3][0]-400)*(1-wireframe.nodes[3][2]/1000)), int(300+(wireframe.nodes[3][1]-300)*(1-wireframe.nodes[3][2]/1000))), 1)
                pygame.draw.aaline(self.screen, (0,255,0), (int(400+(wireframe.nodes[3][0]-400)*(1-wireframe.nodes[3][2]/1000)), int(300+(wireframe.nodes[3][1]-300)*(1-wireframe.nodes[3][2]/1000))), (int(400+(wireframe.nodes[2][0]-400)*(1-wireframe.nodes[2][2]/1000)), int(300+(wireframe.nodes[2][1]-300)*(1-wireframe.nodes[2][2]/1000))), 1)
                pygame.draw.aaline(self.screen, (0,255,0), (int(400+(wireframe.nodes[2][0]-400)*(1-wireframe.nodes[2][2]/1000)), int(300+(wireframe.nodes[2][1]-300)*(1-wireframe.nodes[2][2]/1000))), (int(400+(wireframe.nodes[0][0]-400)*(1-wireframe.nodes[0][2]/1000)), int(300+(wireframe.nodes[0][1]-300)*(1-wireframe.nodes[0][2]/1000))), 1)
                pygame.draw.aaline(self.screen, (0,0,255), (int(400+(wireframe.nodes[4][0]-400)*(1-wireframe.nodes[4][2]/1000)), int(300+(wireframe.nodes[4][1]-300)*(1-wireframe.nodes[4][2]/1000))), (int(400+(wireframe.nodes[5][0]-400)*(1-wireframe.nodes[5][2]/1000)), int(300+(wireframe.nodes[5][1]-300)*(1-wireframe.nodes[5][2]/1000))), 1)
                pygame.draw.aaline(self.screen, (0,0,255), (int(400+(wireframe.nodes[5][0]-400)*(1-wireframe.nodes[5][2]/1000)), int(300+(wireframe.nodes[5][1]-300)*(1-wireframe.nodes[5][2]/1000))), (int(400+(wireframe.nodes[7][0]-400)*(1-wireframe.nodes[7][2]/1000)), int(300+(wireframe.nodes[7][1]-300)*(1-wireframe.nodes[7][2]/1000))), 1)
                pygame.draw.aaline(self.screen, (0,0,255), (int(400+(wireframe.nodes[7][0]-400)*(1-wireframe.nodes[7][2]/1000)), int(300+(wireframe.nodes[7][1]-300)*(1-wireframe.nodes[7][2]/1000))), (int(400+(wireframe.nodes[6][0]-400)*(1-wireframe.nodes[6][2]/1000)), int(300+(wireframe.nodes[6][1]-300)*(1-wireframe.nodes[6][2]/1000))), 1)
                pygame.draw.aaline(self.screen, (0,0,255), (int(400+(wireframe.nodes[6][0]-400)*(1-wireframe.nodes[6][2]/1000)), int(300+(wireframe.nodes[6][1]-300)*(1-wireframe.nodes[6][2]/1000))), (int(400+(wireframe.nodes[4][0]-400)*(1-wireframe.nodes[4][2]/1000)), int(300+(wireframe.nodes[4][1]-300)*(1-wireframe.nodes[4][2]/1000))), 1)
                pygame.draw.aaline(self.screen, self.edgeColour, (int(400+(wireframe.nodes[0][0]-400)*(1-wireframe.nodes[0][2]/1000)), int(300+(wireframe.nodes[0][1]-300)*(1-wireframe.nodes[0][2]/1000))), (int(400+(wireframe.nodes[4][0]-400)*(1-wireframe.nodes[4][2]/1000)), int(300+(wireframe.nodes[4][1]-300)*(1-wireframe.nodes[4][2]/1000))), 1)
                pygame.draw.aaline(self.screen, self.edgeColour, (int(400+(wireframe.nodes[2][0]-400)*(1-wireframe.nodes[2][2]/1000)), int(300+(wireframe.nodes[2][1]-300)*(1-wireframe.nodes[2][2]/1000))), (int(400+(wireframe.nodes[6][0]-400)*(1-wireframe.nodes[6][2]/1000)), int(300+(wireframe.nodes[6][1]-300)*(1-wireframe.nodes[6][2]/1000))), 1)
                pygame.draw.aaline(self.screen, self.edgeColour, (int(400+(wireframe.nodes[1][0]-400)*(1-wireframe.nodes[1][2]/1000)), int(300+(wireframe.nodes[1][1]-300)*(1-wireframe.nodes[1][2]/1000))), (int(400+(wireframe.nodes[5][0]-400)*(1-wireframe.nodes[5][2]/1000)), int(300+(wireframe.nodes[5][1]-300)*(1-wireframe.nodes[5][2]/1000))), 1)
                pygame.draw.aaline(self.screen, self.edgeColour, (int(400+(wireframe.nodes[3][0]-400)*(1-wireframe.nodes[3][2]/1000)), int(300+(wireframe.nodes[3][1]-300)*(1-wireframe.nodes[3][2]/1000))), (int(400+(wireframe.nodes[7][0]-400)*(1-wireframe.nodes[7][2]/1000)), int(300+(wireframe.nodes[7][1]-300)*(1-wireframe.nodes[7][2]/1000))), 1)

            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, self.nodeColour, (int(400+(node[0]-400)*(1-node[2]/1000)), int(300+(node[1]-300)*(1-node[2]/1000))), self.nodeRadius, 0)


    def translateAll(self, direction, increment):
        """ Translate all wireframes along a given axis by d units. """

        for wireframe in self.wireframes.values():
            if direction == 'FORWARD':
                vector = wireframe.unitVectorFront()*increment
            if direction == 'BACKWARD':
                vector = wireframe.unitVectorBack()*increment
            if direction == 'UP':
                vector = wireframe.unitVectorTop()*increment
            if direction == 'DOWN':
                vector = wireframe.unitVectorBottom()*increment
            if direction == 'RIGHT':
                vector = wireframe.unitVectorRight()*increment
            if direction == 'LEFT':
                vector = wireframe.unitVectorLeft()*increment
            matrix = wireframe.translationMatrix(*vector)
            wireframe.transform(matrix)

    def rotateAll(self, spin, theta):
        """ Rotate all wireframe about their center, along a given axis by a given angle. """

        for wireframe in self.wireframes.values():
            if spin == 'YAW':
                point, axis = wireframe.unitVectorYawCenter()
            if spin == 'PITCH':
                point, axis = wireframe.unitVectorPitchCenter()
            if spin == 'ROLL':
                point, axis = wireframe.unitVectorRollCenter()
            wireframe.rotateAll(point[0],point[1],point[2],axis[0],axis[1],axis[2],theta)

def createCube(centerX, centerY, centerZ, sideLength):
    """ Creates the coordinates for a cube. """
    coordinates = np.zeros((8,3))
    coordinates[0] = [centerX-(sideLength/2), centerY-(sideLength/2), centerZ-(sideLength/2)]
    coordinates[1] = [centerX-(sideLength/2), centerY-(sideLength/2), centerZ+(sideLength/2)]
    coordinates[2] = [centerX-(sideLength/2), centerY+(sideLength/2), centerZ-(sideLength/2)]
    coordinates[3] = [centerX-(sideLength/2), centerY+(sideLength/2), centerZ+(sideLength/2)]
    coordinates[4] = [centerX+(sideLength/2), centerY-(sideLength/2), centerZ-(sideLength/2)]
    coordinates[5] = [centerX+(sideLength/2), centerY-(sideLength/2), centerZ+(sideLength/2)]
    coordinates[6] = [centerX+(sideLength/2), centerY+(sideLength/2), centerZ-(sideLength/2)]
    coordinates[7] = [centerX+(sideLength/2), centerY+(sideLength/2), centerZ+(sideLength/2)]
    return coordinates


if __name__ == "__main__":
    resolutionX = 1000
    resolutionY = 800

    cube = Wireframe()
    cube_nodes = createCube(resolutionX/2,resolutionY/2,0,100)

    cube.addNodes(cube_nodes)

    cube.addEdges([(n,n+4) for n in range(0,4)])
    cube.addEdges([(n,n+1) for n in range(0,8,2)])
    cube.addEdges([(n,n+2) for n in (0,1,4,5)])

    cube.outputNodes()
    cube.outputEdges()

    pv = ProjectionViewer(resolutionX, resolutionY)

    pv.addWireframe('cube', cube)
    pv.run()
