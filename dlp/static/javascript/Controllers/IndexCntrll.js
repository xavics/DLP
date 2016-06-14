/**
 * Created by xavi on 7/06/16.
 */
angular.module('DLPApp').controller('IndexCntrll',['$scope', '$http', '$state', '$stateParams', '$translate', 'uiGmapGoogleMapApi',
    'uiGmapIsReady', 'City', 'CityByName', 'LogisticCenter', 'Droppoint', 'Drone', 'Package', 'Transport', '$timeout', 'FoundationApi',
    function($scope, $state, $stateParams, $http, $translate, uiGmapGoogleMapApi, uiGmapIsReady, City, CityByName,
             LogisticCenter, Droppoint, Drone, Package, $timeout, FoundationApi){
        var city_str = $stateParams.city;
        $scope.logistic_centers = [];
        $scope.lc = [];
        city_str = (city_str) ? city_str : "Lleida";
        if (isNaN(city_str)) {
            $scope.main_city = CityByName.get({name: city_str},
                function () {
                    $scope.main_city = $scope.main_city.results[0];
                    $scope.main_city.logistic_centers.forEach(get_logistic_centers);
                })
        }
        else{
            $scope.main_city = City.get({id:city_str});
        }
        $scope.changeLanguage = function (key) {
            $translate.use(key);
        };
        $scope.left_menu = false;
        get_logistic_centers = function(item){
            var logistic_center = LogisticCenter.get({id: item},
                function () {
                    $scope.logistic_centers.push(logistic_center);
                    $scope.lc[logistic_center.id] = false;
                });
        };

        $scope.openAccordion = function() {

        };

        $scope.selected_center = null
        $scope.change_center = function(index){
            $scope.selected_center = $scope.logistic_centers[index];
        }
        $scope.close_center = function(){
            $scope.selected_center = null;
        }
        // Do stuff with your $scope.
        // Note: Some of the directives require at least something to be defined originally!
        // e.g. $scope.markers = []

        // uiGmapGoogleMapApi is a promise.
        // The "then" callback function provides the google.maps object.
        uiGmapGoogleMapApi.then(function(maps) {
            $scope.map = { center: { latitude: 45, longitude: -73 }, zoom: 8 };
        });
        uiGmapIsReady.promise()                     // this gets all (ready) map instances - defaults to 1 for the first map
            .then(function(instances) {                 // instances is an array object
                var maps = instances[0].map;            // if only 1 map it's found at index 0 of array
            });

        $scope.openCenterInfo = function (index) {
            FoundationApi.subscribe('LCrepresentation', 'open')
            $scope.lc[index] = !$scope.lc[index];
        };

    }]);