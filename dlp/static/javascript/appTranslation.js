/**
 * Created by xavi on 12/06/16.
 */
angular.module('DLPApp').config(['$translateProvider', function ($translateProvider) {
    $translateProvider.translations('en', {
        'INFORMATION': 'Information',
        'LOGISTICCENTER': 'Logistic Center',
        'DRONES': 'Drones',
        'DESCRIPTION': 'Description',
        'ADDRESS': 'Address',
        'PICTURE': 'Picture',
        'LATITUDE': 'Latitude',
        'LONGITUDE': 'Longitude',
        'ALTITUDE': 'Altitude',
        'RADIUS': 'Radius',
        'DROPPOINTS': 'Drop points',
        'DROPPOINT': 'Drop point',
        'EDIT': 'Edit',
        'CANCEL': 'Cancel',
        'CREATE NEW': 'Create new',
        'SAVE': 'Save',
        'NAME': 'Name',
        'CITY': 'City',
        'DELETE': 'Delete',
        'TRANSPORTS': 'Deliveries',
        'DRONE': 'Drone',
        'PLATE': 'Plate',
        'ICON': 'Icon',
        'MODEL': 'Model',
        'ISTRANSPORTING': 'Is transporting?',
        'BATTERY': 'Battery life',
        'DELETE_ALERT': 'Are you sure you want to delete this',
        'TRANSPORT': 'Delivery',
        'PACKAGE': 'Package'
    });

    $translateProvider.translations('es', {
        'INFORMATION': 'Información',
        'LOGISTICCENTER': 'Centro Logístico',
        'DRONES': 'Drones',
        'DESCRIPTION': 'Descripción',
        'ADDRESS': 'Direccion',
        'PICTURE': 'Imagen',
        'LATITUDE': 'Latitud',
        'LONGITUDE': 'Longitud',
        'ALTITUDE': 'Altitud',
        'RADIUS': 'Radio de accion',
        'DROPPOINTS': 'Puntos de entrega',
        'DROPPOINT': 'Punto de entrega',
        'EDIT': 'Editar',
        'CANCEL': 'Cancelar',
        'CREATE NEW': 'Crear nuevo',
        'SAVE': 'Guardar',
        'NAME': 'Nombre',
        'CITY': 'Ciudad',
        'DELETE': 'Eliminar',
        'TRANSPORTS': 'Repartos',
        'DRONE': 'Dron',
        'PLATE': 'Matrícula',
        'ICON': 'Icono',
        'MODEL': 'Modelo',
        'ISTRANSPORTING': 'Esta transportando?',
        'BATTERY': 'Estado de la bateria',
        'DELETE_ALERT': 'Esta seguro que desea eliminar este',
        'TRANSPORT': 'Entrega',
        'PACKAGE': 'Paquete'
    });

    $translateProvider.preferredLanguage('en');
}]);