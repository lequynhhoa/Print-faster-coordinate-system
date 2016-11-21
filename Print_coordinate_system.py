# -*- coding: utf-8 -*-
"""
/***************************************************************************
 checkcoordinatesys
                                 A QGIS plugin
 Print coordinate system all layers
                              -------------------
        begin                : 2016-10-06
        git sha              : $Format:%H$
        copyright            : (C) 2016 by GFD
        email                : hoa.lq@gfd.com.vn
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis import *
from qgis.utils import *
from qgis.core import *
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QMenu, QMenuBar
from qgis.core import QgsVectorFileWriter
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from Print_coordinate_system_dialog import checkcoordinatesysDialog
import os.path


class checkcoordinatesys:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'checkcoordinatesys_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Kiem tra he toa do')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'checkcoordinatesys')
        self.toolbar.setObjectName(u'checkcoordinatesys')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('checkcoordinatesys', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = checkcoordinatesysDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/checkcoordinatesys/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Kiem tra he toa do cua cac lop'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Kiem tra he toa do'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # Select the layers open in the legendInterface and add them to an array
        crs = QgsCoordinateReferenceSystem()
        layers = self.iface.legendInterface().layers()
        layer_list = []
        # Declare coordinate system to print out screen
        # VN2000 Noi bo mui 3
        htd_103_nb = "+proj=tmerc +lat_0=0 +lon_0=103 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_104_nb = "+proj=tmerc +lat_0=0 +lon_0=104 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_104_5_nb = "+proj=tmerc +lat_0=0 +lon_0=104.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_104_75_nb = "+proj=tmerc +lat_0=0 +lon_0=104.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_105_nb = "+proj=tmerc +lat_0=0 +lon_0=105 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_105_5_nb = "+proj=tmerc +lat_0=0 +lon_0=105.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_105_75_nb = "+proj=tmerc +lat_0=0 +lon_0=105.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_106_nb = "+proj=tmerc +lat_0=0 +lon_0=106 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_106_25_nb = "+proj=tmerc +lat_0=0 +lon_0=106.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_106_5_nb = "+proj=tmerc +lat_0=0 +lon_0=106.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_107_nb = "+proj=tmerc +lat_0=0 +lon_0=107 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_107_25_nb = "+proj=tmerc +lat_0=0 +lon_0=107.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_107_5_nb = "+proj=tmerc +lat_0=0 +lon_0=107.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_107_75_nb = "+proj=tmerc +lat_0=0 +lon_0=107.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_108_nb = "+proj=tmerc +lat_0=0 +lon_0=108 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_108_25_nb = "+proj=tmerc +lat_0=0 +lon_0=108.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        htd_108_5_nb = "+proj=tmerc +lat_0=0 +lon_0=108.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"

        # VN2000 Hoi nhap mui 3
        htd_103_hn = "+proj=tmerc +lat_0=0 +lon_0=103 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_104_hn = "+proj=tmerc +lat_0=0 +lon_0=104 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_104_5_hn = "+proj=tmerc +lat_0=0 +lon_0=104_5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_104_75_hn = "+proj=tmerc +lat_0=0 +lon_0=104.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_105_hn = "+proj=tmerc +lat_0=0 +lon_0=105 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_105_5_hn = "+proj=tmerc +lat_0=0 +lon_0=105.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_105_75_hn = "+proj=tmerc +lat_0=0 +lon_0=105.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_106_hn = "+proj=tmerc +lat_0=0 +lon_0=106 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_106_25_hn = "+proj=tmerc +lat_0=0 +lon_0=106.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_106_5_hn = "+proj=tmerc +lat_0=0 +lon_0=106.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_hn = "+proj=tmerc +lat_0=0 +lon_0=107 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_25_hn = "+proj=tmerc +lat_0=0 +lon_0=107.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_5_hn = "+proj=tmerc +lat_0=0 +lon_0=107.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_75_hn = "+proj=tmerc +lat_0=0 +lon_0=107.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_108_hn = "+proj=tmerc +lat_0=0 +lon_0=108 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_108_25_hn = "+proj=tmerc +lat_0=0 +lon_0=108.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_108_5_hn = "+proj=tmerc +lat_0=0 +lon_0=108.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"

        # UTM 48,49
        htd_utm_48 = "+proj=utm +zone=48 +datum=WGS84 +units=m +no_defs"
        htd_utm_49 = "+proj=utm +zone=49 +datum=WGS84 +units=m +no_defs"

        # WGS84 Latlong - 4326
        htd_latlong_4326 = "+proj=longlat +datum=WGS84 +no_defs"

        #Loop all layers
        for layer in layers:
            if layer.crs().toProj4() == htd_103_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 103 mui 3 ")
            elif layer.crs().toProj4() == htd_104_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 104 mui 3 ")
            elif layer.crs().toProj4() == htd_104_5_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 104.5 mui 3 ")
            elif layer.crs().toProj4() == htd_104_75_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 104.75 mui 3 ")
            elif layer.crs().toProj4() == htd_105_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 105 mui 3 ")
            elif layer.crs().toProj4() == htd_105_5_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 105.5 mui 3 ")
            elif layer.crs().toProj4() == htd_105_75_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 105.75 mui 3 ")
            elif layer.crs().toProj4() == htd_106_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 106 mui 3 ")
            elif layer.crs().toProj4() == htd_106_25_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 106.25 mui 3 ")
            elif layer.crs().toProj4() == htd_106_5_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 106.5 mui 3 ")
            elif layer.crs().toProj4() == htd_107_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 107 mui 3 ")
            elif layer.crs().toProj4() == htd_107_25_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 107.25 mui 3 ")
            elif layer.crs().toProj4() == htd_107_5_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 107.5 mui 3 ")
            elif layer.crs().toProj4() == htd_107_75_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 107.75 mui 3 ")
            elif layer.crs().toProj4() == htd_108_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 108 mui 3 ")
            elif layer.crs().toProj4() == htd_108_25_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 108.25 mui 3 ")
            elif layer.crs().toProj4() == htd_108_5_nb :
                layer_list.append(layer.name() + " -->" + "VN-2000 Noi bo KTT 108.5 mui 3 ")
        # VN2000 Hoi nhap
            elif layer.crs().toProj4() == htd_103_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 103 mui 3 ")
            elif layer.crs().toProj4() == htd_104_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 104 mui 3 ")
            elif layer.crs().toProj4() == htd_104_5_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 104.5 mui 3 ")
            elif layer.crs().toProj4() == htd_104_75_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 104.75 mui 3 ")
            elif layer.crs().toProj4() == htd_105_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 105 mui 3 ")
            elif layer.crs().toProj4() == htd_105_5_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 105.5 mui 3 ")
            elif layer.crs().toProj4() == htd_105_75_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 105.75 mui 3 ")
            elif layer.crs().toProj4() == htd_106_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 106 mui 3 ")
            elif layer.crs().toProj4() == htd_106_25_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 106.25 mui 3 ")
            elif layer.crs().toProj4() == htd_106_5_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 106.5 mui 3 ")
            elif layer.crs().toProj4() == htd_107_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 107 mui 3 ")
            elif layer.crs().toProj4() == htd_107_25_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 107.25 mui 3 ")
            elif layer.crs().toProj4() == htd_107_5_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 107.5 mui 3 ")
            elif layer.crs().toProj4() == htd_107_75_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 107.75 mui 3 ")
            elif layer.crs().toProj4() == htd_108_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 108 mui 3 ")
            elif layer.crs().toProj4() == htd_108_25_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 108.25 mui 3 ")
            elif layer.crs().toProj4() == htd_108_5_hn :
                layer_list.append(layer.name() + " -->" + "VN-2000 Hoi nhap KTT 108.5 mui 3 ")

        # UTM 48,49, Latlong
            elif layer.crs().toProj4() == htd_utm_48 :
                layer_list.append(layer.name() + " -->" + "UTM Zone 48N - EPSG: 32648")
            elif layer.crs().toProj4() == htd_utm_49 :
                layer_list.append(layer.name() + " -->" + "UTM Zone 49N - EPSG: 32649")
            elif layer.crs().toProj4() == htd_latlong_4326 :
                layer_list.append(layer.name() + " -->" + "WGS 84 Lat/Long - EPSG: 4326")
            else:
                layer_list.append(layer.name() + " -->" +layer.crs().toProj4())
        # Add layer_list array to listWidget, clear layer if removed to layer in tools
        self.dlg.listWidget.clear()
        self.dlg.listWidget.addItems(layer_list)
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
