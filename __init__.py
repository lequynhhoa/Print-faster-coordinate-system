# -*- coding: utf-8 -*-
"""
/***************************************************************************
 checkcoordinatesys
                                 A QGIS plugin
 Print coordinate system all layers
                             -------------------
        begin                : 2016-10-06
        copyright            : (C) 2016 by GFD
        email                : hoa.lq@gfd.com.vn
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load checkcoordinatesys class from file checkcoordinatesys.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .Print_coordinate_system import checkcoordinatesys
    return checkcoordinatesys(iface)
