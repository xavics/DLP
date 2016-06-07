/**
 * Created by xavi on 7/06/16.
 */
var myServices = angular.module('myServices', ['ngResource']);

myServices.factory('LogisticCenter', ['$resource', function($resource) {
    return $resource('/crud/logisticCenter/', {'pk': '@pk'}, {
    });
}]);

myServices.factory('Drone', ['$resource', function($resource) {
    return $resource('/crud/drone/', {'pk': '@pk'}, {
    });
}]);

myServices.factory('Droppoint', ['$resource', function($resource) {
    return $resource('/crud/dropPoint/', {'pk': '@pk'}, {
    });
}]);

myServices.factory('City', ['$resource', function($resource) {
    return $resource('/crud/city/', {'pk': '@pk'}, {
    });
}]);

myServices.factory('Package', ['$resource', function($resource) {
    return $resource('/crud/package/', {'pk': '@pk'}, {
    });
}]);

myServices.factory('Transport', ['$resource', function($resource) {
    return $resource('/crud/transport/', {'pk': '@pk'}, {
    });
}]);
