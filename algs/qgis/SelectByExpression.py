# -*- coding: utf-8 -*-

"""
***************************************************************************
    SelectByExpression.py
    ---------------------
    Date                 : July 2014
    Copyright            : (C) 2014 by Michael Douchin
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Michael Douchin'
__date__ = 'July 2014'
__copyright__ = '(C) 2014, Michael Douchin'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import processing
from qgis.core import QgsExpression, QgsVectorLayer
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.core.parameters import ParameterVector
from processing.core.parameters import ParameterSelection
from processing.core.outputs import OutputVector
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.parameters import ParameterString


class SelectByExpression(GeoAlgorithm):

    LAYERNAME = 'LAYERNAME'
    EXPRESSION = 'EXPRESSION'
    RESULT = 'RESULT'
    METHOD = 'METHOD'

    def defineCharacteristics(self):
        self.name, self.i18n_name = self.trAlgorithm('Select by expression')
        self.group, self.i18n_group = self.trAlgorithm('Vector selection tools')
        self.showInModeler = False

        self.methods = [self.tr('creating new selection'),
                        self.tr('adding to current selection'),
                        self.tr('removing from current selection'),
                        self.tr('selecting within current selection')]

        self.addParameter(ParameterVector(self.LAYERNAME,
                                          self.tr('Input Layer'), [ParameterVector.VECTOR_TYPE_ANY]))
        self.addParameter(ParameterString(self.EXPRESSION,
                                          self.tr("Expression")))
        self.addParameter(ParameterSelection(self.METHOD,
                                             self.tr('Modify current selection by'), self.methods, 0))
        self.addOutput(OutputVector(self.RESULT, self.tr('Selected (expression)'), True))

    def processAlgorithm(self, progress):
        filename = self.getParameterValue(self.LAYERNAME)
        layer = processing.getObject(filename)
        oldSelection = set(layer.selectedFeaturesIds())
        method = self.getParameterValue(self.METHOD)

        if method == 0:
            behaviour = QgsVectorLayer.SetSelection
        elif method == 1:
            behaviour = QgsVectorLayer.AddToSelection
        elif method == 2:
            behavior = QgsVectorLayer.RemoveFromSelection
        elif method == 3:
            behaviour = QgsVectorLayer.IntersectSelection

        expression = self.getParameterValue(self.EXPRESSION)
        qExp = QgsExpression(expression)
        if qExp.hasParserError():
            raise GeoAlgorithmExecutionException(qExp.parserErrorString())

        layer.selectByExpression(expression, behaviour)
        self.setOutputValue(self.RESULT, filename)
