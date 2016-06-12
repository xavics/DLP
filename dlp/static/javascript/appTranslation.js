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
        'DROP_POINTS': 'Drop points',
        'EDIT': 'Edit',
        'CANCEL': 'Cancel',
        'CREATE NEW': 'Create new',
        'SAVE': 'Save',
        'NAME': 'Name',
        'CITY': 'City',
        'DELETE': 'Delete'
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
        'DROP_POINTS': 'Puntos de entrega',
        'EDIT': 'Editar',
        'CANCEL': 'Cancelar',
        'CREATE NEW': 'Crear nuevo',
        'SAVE': 'Guardar',
        'NAME': 'Nombre',
        'CITY': 'Ciudad',
        'DELETE': 'Eliminar'
    });

    $translateProvider.preferredLanguage('en');
}]);