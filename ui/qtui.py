#!/usr/bin/pyhton3

from PySide.QtCore import *
from PySide.QtGui import *

import sys
import os
import math

model = [
    {
        'source': '~', 
        'patterns': [ ('*.png', 'r') ],
        'targets': ['Input'],
        'script':None
    }
]

class MainFrame(QMainWindow):
    def __init__(self,model):
        super().__init__()
        self.view = ModelView(model)
        self.setCentralWidget(self.view)

def model2graph(model):
    vertices = set()
    edges = {}

    for r in model:
        s = r['source']
        vertices.add(s)
        for t in r['targets']:
            vertices.add(t)
            edges[s,t] = r

    return vertices,edges
    
def randomCoords(w,h):
    import random
    return random.randint(0,w), random.randint(0,h)

class Link(QGraphicsItemGroup):
    def __init__(self,folderStart, folderEnd, rule):
        super().__init__()
        self.arrow = Arrow(arrowHead)
        self.folderS = folderStart
        self.folderE = folderEnd            
        self.setFlag(QGraphicsItem.ItemIsSelectable, True);
        s = repr(rule['patterns'])
        self.textLabel = QGraphicsTextItem(s)

        self.addToGroup(self.textLabel)
        self.addToGroup(self.arrow)
        
        self.updatePos()

    def boundingRect(self):
        return self.arrow.boundingRect() | self.textLabel.boundingRect()

    def updatePos(self):
        a = self.folderS.sceneBoundingRect()
        b = self.folderE.sceneBoundingRect()
        
        ac = a.center()
        bc = b.center()

        line = QLineF(ac,bc)

        self.start = intersectBB(line,a)
        self.stop = intersectBB(line,b)

        self.arrow._calculatePath(self.start,self.stop)   

        line = QLineF(self.start,self.stop)
        line.setLength(line.length()/2.0)
        self.textLabel.setPos(line.p2())
        
        
        
        

class Arrow(QGraphicsPathItem):
    def __init__(self, endShape):
        super().__init__()
      
        self.endShape = endShape
        
        self.setPen(QPen(QColor(0,0,0), 1, Qt.SolidLine,
                    Qt.FlatCap, Qt.MiterJoin))

        self.setBrush(QColor(0,0,0))
        
    def _calculatePath(self,start, end):
        path = QPainterPath()

        path.moveTo(start)
        path.lineTo(end)

        line = QLineF(start,end)
        self.angle = line.angle()    

        transform = QTransform()
        transform.scale(20,20)
        transform.rotate(360-self.angle)

        s = self.endShape * transform   
        s.translate(end)
        path.addPath(s)
                
        self.setPath(path)
        

def intersectBB(line,rect):
    a,b,c,d = rect.bottomLeft(), rect.bottomRight(),\
              rect.topRight(), rect.topLeft()

    rlines = ( QLineF(a,b), QLineF(b,c), QLineF(c,d), QLineF(d,a) )
    inter = filter(lambda a:
                   a[0] == QLineF.IntersectType.BoundedIntersection,      
                   map(lambda l: line.intersect(l), rlines))
    try:
        return list(inter)[0][1]
    except:
        return rect.center()
    




arrowHead = QPainterPath()
arrowHead.lineTo(-0.5,-0.3)
arrowHead.lineTo(-0.5,0.3)
arrowHead.lineTo(0,0)
arrowHead.toFillPolygon()



def createFolderGraphicItem(folder_name, scene, border_margin = 6):
    flags = QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable
    text = QGraphicsSimpleTextItem(folder_name)
    rect = text.boundingRect()
    rect.moveTo(- border_margin, - border_margin)
    rect.setWidth(rect.width() + border_margin*1.3)
    rect.setHeight(rect.height() + border_margin*1.3)

    bpath = QPainterPath()
    bpath.addRoundedRect(rect,5,5)

    border = QGraphicsPathItem(bpath)
    border.setBrush(QBrush(QColor(200,200,200)))
    border.setZValue(-100)

    text.setZValue(100)

    border.setFlags(flags)
    text.setFlags(flags)
    scene.addItem(border)
    scene.addItem(text)
    item =  scene.createItemGroup([text,border])
    item.setFlags(flags)
    return item

class ModelView(QGraphicsView):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.graph = model2graph(self.model)
        
        w,h = self.width(), self.height()
        scene = QGraphicsScene()
        self.setScene(scene)
        self.setInteractive(True)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        scene.changed.connect(self.updateLinks)
        
        self.folders = {}
        self.links = {}

        for v in self.graph[0]:
            item = createFolderGraphicItem(v,scene)
            self.folders[v] = item  
            item.setPos(*randomCoords(w,h))

        for ((s,t),d) in self.graph[1].items():            
            a = self.folders[s]
            b = self.folders[t]
            c = Link(a, b, d)
            scene.addItem(c)

        
    def updateLinks(self, regions):
        for r in regions:
            mode = Qt.IntersectsItemBoundingRect
            items = self.scene().items(r, mode)
       
            isLink = lambda a: isinstance(a,Link)
            links = filter(isLink, items)            
            for l in links:
                print(l)
                l.updatePos()
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mf = MainFrame(model)
    mf.show()

    sys.exit(app.exec_())
