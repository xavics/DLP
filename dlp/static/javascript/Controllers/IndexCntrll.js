/**
 * Created by xavi on 7/06/16.
 */
angular.module('DLPApp').controller('IndexCntrll',['$scope', '$http', '$stateParams', '$state', '$translate', 'uiGmapGoogleMapApi',
    'uiGmapIsReady', 'City', 'CityByPlaceId', 'LogisticCenter', '$timeout', 'FoundationApi',
    function($scope, $http, $stateParams, $state, $translate, uiGmapGoogleMapApi, uiGmapIsReady, City, CityByPlaceId,
             LogisticCenter, $timeout, FoundationApi){
        var city_str = $stateParams.city;
        $scope.logistic_centers = [];
        $scope.lc = [];
        $scope.main_city = CityByPlaceId.get({place_id: city_str, time: Date.now()},
        function () {
            $scope.main_city = $scope.main_city.results[0];
            $scope.main_city.logistic_centers.forEach(get_logistic_centers);
            $scope.map = { center: { latitude: $scope.main_city.lat, longitude: $scope.main_city.lng }, zoom: 14,
                options: { maxZoom: 18, minZoom: 11 },
                events: {
                    click: function (map, eventNmae, args) {
                        $scope.$apply(function() {
                            latLng = args[0].latLng
                            $scope.openMarker(latLng.lat(), latLng.lng())
                        });
                    }
                },
                markers: []};
            //prepare_map($scope.main_city.lat, $scope.main_city.lng)
        })
        $scope.changeLanguage = function (key) {
            $translate.use(key);
        };
        $scope.left_menu = false;
        get_logistic_centers = function(item){
            var logistic_center = LogisticCenter.get({id: item},
                function () {
                    $scope.logistic_centers.push(logistic_center);
                    $scope.lc[logistic_center.id] = false;
                    $scope.add_marker_center(logistic_center.id, logistic_center.lat, logistic_center.lng)
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
        //prepare_map = function(lat, lng){
        uiGmapGoogleMapApi.then(function(maps) {
        });
        uiGmapIsReady.promise()                     // this gets all (ready) map instances - defaults to 1 for the first map
            .then(function(instances) {                 // instances is an array object
                var maps = instances[0].map;            // if only 1 map it's found at index 0 of array
            });
        //}
        openCenterInfo = function (index) {
            FoundationApi.publish('LCrepresentation', 'open')
            $scope.lc[index] = !$scope.lc[index];
        };

        openDroppointTab = function (id_tab, id_dp){

        }

        $scope.add_marker_center = function(id, lat, lng){
            var marker = {
                id: "lc" + id,
                coords: {
                    latitude: lat,
                    longitude: lng
                },
                options: {
                    icon: 'static/images/lc48.png'
                },
                events: {
                    click: function (marker, eventName, args) {
                        openCenterInfo(id)
                    }
                }
            };
            $scope.map.markers.push(marker);
        }

        $scope.add_marker_droppoint = function(id_center, id, lat, lng){
            var marker = {
                id: "lc" + id_center + "dp" + id,
                coords: {
                    latitude: lat,
                    longitude: lng
                },
                options: {
                    icon: 'static/images/droppoint32.png'
                },
                events: {
                    click: function (marker, eventName, args) {
                        openCenterInfo(id_center)
                    }
                }
            };
            $scope.map.markers.push(marker);
        }

        $scope.newCoords = {lat: 0.0, lng: 0.0}

        $scope.openMarker = function(lat, lng){
            var marker = {
                id: "latLngMk",
                coords: {
                    latitude: lat,
                    longitude: lng
                },
                options: {
                    icon: 'static/images/latLng32.png'
                },
                events: {
                    click: function (marker, eventName, args) {
                        $scope.$apply(function() {
                            $scope.newCoords.lat = lat;
                            $scope.newCoords.lng = lng;
                        });
                    }
                }
            };
            var result = $scope.map.markers.findIndex(function( obj ) {
                return obj.id == "latLngMk";
            });
            if(result != -1) {
                $scope.map.markers.splice(result, 1, marker);
            }
            else {
                $scope.map.markers.push(marker);
            }
            $scope.newCoords.lat = lat;
            $scope.newCoords.lng = lng;
        }

    }]);