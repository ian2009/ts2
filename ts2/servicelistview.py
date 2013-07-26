#
#   Copyright (C) 2008-2013 by Nicolas Piganeau                                
#   npi@m4x.org                                                           
#                                                                         
#   This program is free software; you can redistribute it and/or modify  
#   it under the terms of the GNU General Public License as published by  
#   the Free Software Foundation; either version 2 of the License, or     
#   (at your option) any later version.                                   
#                                                                         
#   This program is distributed in the hope that it will be useful,       
#   but WITHOUT ANY WARRANTY; without even the implied warranty of        
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         
#   GNU General Public License for more details.                          
#                                                                         
#   You should have received a copy of the GNU General Public License     
#   along with this program; if not, write to the                         
#   Free Software Foundation, Inc.,                                       
#   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             
#

from PyQt4.QtGui import *
from simulation import *
from service import *

class ServiceListView(QTreeView):
    """TODO Document ServiceListView"""    

    def __init__(self, parent, simulation):
        super().__init__(parent)
        self._simulation = simulation
        self.setItemsExpandable(False)
        self.setRootIsDecorated(False)
        self.setHeaderHidden(False)
        self._simulation.simulationLoaded.connect(self.setupServiceList)

    serviceSelected = pyqtSignal(str)

    @pyqtSlot(str)
    def updateServiceSelection(self, serviceCode):
        pass

    @pyqtSlot()
    def setupServiceList(self):
        """Updates the service list view."""
        if self.model() is None:
            self.setModel(self._simulation.serviceListModel)
            self.setSortingEnabled(True)
            for i in range(0,4):
                self.resizeColumnToContents(i)
            self.header().setStretchLastSection(False)
            self.header().setSortIndicatorShown(False)
            self.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.serviceSelected.connect(self._simulation.selectedServiceModel.setServiceCode)
            self._simulation.simulationWindow.trainListView.trainSelected.connect(\
                self.updateServiceSelection)

    @pyqtSlot(QItemSelection, QItemSelection)
    def selectionChanged(self, selected, deselected):
        """This function is called when a line is selected in the service list view.
        It emits the serviceSelected signal for others to connect to."""
        index = selected.indexes()[0]
        if index.isValid():
            self.serviceSelected.emit(index.data())
