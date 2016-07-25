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

myServices.factory('City', ['$resource', '$cacheFactory', function($resource) {
    return $resource('/api/cities/:id/?time=time', {'id': '@id', 'time': '@time'}, {
    });
}]);

myServices.factory('Package', ['$resource', function($resource) {
    return $resource('/api/packages/:id/', {'id': '@id'}, {
        'update': { method:'PUT' }
    });
}]);

myServices.factory('Transport', ['$resource', function($resource) {
    return $resource('/api/transports/:id/?time=:time', {'id': '@id', 'time': '@time'}, {
        'update': { method:'PUT' }
    });
}]);

myServices.factory('CityByPlaceId', ['$resource', function($resource) {
    return $resource('/api/cities/?place_id=:place_id&time=time', {'place_id': '@place_id', 'time': '@time'}, {
    });
}]);

myServices.factory('TransportByLc', ['$resource', function($resource) {
    return $resource('/api/transports/?logistic_center=:logistic_center&status=:status&time=time',
        {'logistic_center': '@logistic_center', status: '@status', 'time': '@time'}, {
        });
}]);

myServices.factory('DefinedStyle', ['$resource', function($resource) {
    return $resource('/api/definedstyles/:id/', {'id': '@id'}, {
        'update': { method:'PUT' }
    });
}]);


myServices.factory('UpdateDp', ['$http', '$cacheFactory', function($http, $cacheFactory) {
 return{
    dp : function() {
        $cacheFactory.get('$http').remove('/update_droppoints');
        return $http({
            url: '/update_droppoints',
            method: 'GET'
        })
    }
 }
}]);

myServices.factory('UpdateLc', ['$http', '$cacheFactory', function($http, $cacheFactory) {
 return{
    lc : function() {
        $cacheFactory.get('$http').remove('/update_logistic_centers')
        return $http({
            url: '/update_logistic_centers',
            method: 'GET'
        })
    }
 }
}]);

myServices.factory('RefreshWeather', ['$http', '$cacheFactory', function($http, $cacheFactory) {
 return{
    refresh : function(city) {
        $cacheFactory.get('$http').remove('/refreshweather')
        return $http({
            url: '/refreshweather',
            method: 'GET',
            params: {
                city: city
            }
        })
    }
 }
}]);