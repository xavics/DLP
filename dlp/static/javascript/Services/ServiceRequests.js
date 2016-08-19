/**
 * Created by xavi on 29/07/16.
 */
var myRequests = angular.module('myRequests', ['ngResource']);

myRequests.factory('UpdateDp', ['$http', '$cacheFactory', function($http, $cacheFactory) {
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

myRequests.factory('UpdateLc', ['$http', '$cacheFactory', function($http, $cacheFactory) {
    return{
        lc : function() {
            $cacheFactory.get('$http').remove('/update_logistic_centers');
            return $http({
                url: '/update_logistic_centers',
                method: 'GET'
            })
        }
    }
}]);

myRequests.factory('RefreshWeather', ['$http', '$cacheFactory', function($http, $cacheFactory) {
    return{
        refresh: function(city, time) {
            $cacheFactory.get('$http').remove('/refreshweather');
            return $http({
                url: '/refreshweather',
                method: 'GET',
                params: {
                    city: city,
                    time: time
                }
            })
        },
        get_restriction: function(time) {
            $cacheFactory.get('$http').remove('/get_restriction');
            return $http({
                url: '/get_restriction',
                method: 'GET',
                params: {
                    time: time
                }
            })
        },
        toogle_restriction: function(time) {
            $cacheFactory.get('$http').remove('/toogle_restriction');
            return $http({
                url: '/toogle_restriction',
                method: 'GET',
                params: {
                    time: time
                }
            })
        }
    }
}]);

myRequests.factory('Tour', ['$http', '$cacheFactory', function($http, $cacheFactory) {
    return{
        create : function(city, time) {
            $cacheFactory.get('$http').remove('/make_rotation');
            return $http({
                url: '/make_rotation',
                method: 'GET',
                params: {
                    city: city,
                    time: time
                }
            })
        },
        play : function(city, time) {
            $cacheFactory.get('$http').remove('/play_tour');
            return $http({
                url: '/play_tour',
                method: 'GET',
                params: {
                    city: city,
                    time: time
                }
            })
        },
        stop : function(city, time) {
            $cacheFactory.get('$http').remove('/stop_tour');
            return $http({
                url: '/stop_tour',
                method: 'GET',
                params: {
                    city: city,
                    time: time
                }
            })
        }
    }
}]);


myRequests.factory('Demo', ['$http', '$cacheFactory', function($http, $cacheFactory) {
    return{
        demo : function() {
            $cacheFactory.get('$http').remove('/run_demo');
            return $http({
                url: '/run_demo',
                method: 'GET'
            })
        }
    }
}]);


myRequests.factory('Galaxy', ['$http', '$cacheFactory', function($http, $cacheFactory) {
    return{
        fly_to : function(city, time) {
            $cacheFactory.get('$http').remove('/fly_to');
            return $http({
                url: '/fly_to',
                method: 'GET',
                params: {
                    city: city,
                    time: time
                }
            })
        },
        refresh_kmls : function(city, time) {
            $cacheFactory.get('$http').remove('/refresh_kmls');
            return $http({
                url: '/refresh_kmls',
                method: 'GET',
                params: {
                    city: city,
                    time: time
                }
            })
        }
    }
}]);
