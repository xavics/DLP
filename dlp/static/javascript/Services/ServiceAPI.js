/**
 * Created by xavi on 7/06/16.
 */
var myServices = angular.module('myServices', ['ngResource']);

myServices.factory('LogisticCenter', ['$resource', function($resource) {
    return $resource('/api/logisticcenters/:id/', {'id': '@id'}, {
        'update': { method:'PUT' }
    });
}]);

myServices.factory('Drone', ['$resource', function($resource) {
    return $resource('/api/drones/:id/', {'id': '@id'}, {
        'update': { method:'PUT' }
    });
}]);

myServices.factory('Droppoint', ['$resource', function($resource) {
    return $resource('/api/droppoints/:id/', {'id': '@id'}, {
        'update': { method:'PUT' }
    });
}]);

myServices.factory('City', ['$resource', function($resource) {
    return $resource('/api/cities/:id', {'id': '@id'}, {
    });
}]);

myServices.factory('Package', ['$resource', function($resource) {
    return $resource('/api/packages/:id/', {'id': '@id'}, {
        'update': { method:'PUT' }
    });
}]);

myServices.factory('Transport', ['$resource', function($resource) {
    return $resource('/api/transports/:id/', {'id': '@id'}, {
        'update': { method:'PUT' }
    });
}]);

myServices.factory('CityByName', ['$resource', function($resource) {
    return $resource('/api/cities/?name=:name', {'name': '@name'}, {
    });
}]);
