/**
 * Created by xavi on 7/06/16.
 */
angular.module('DLPApp').controller('IndexCntrll',['$anchorScroll', '$location', '$scope', '$http', '$stateParams', '$state', '$translate', 'uiGmapGoogleMapApi',
    'uiGmapIsReady', 'City', 'CityByPlaceId', 'LogisticCenter', '$timeout', 'FoundationApi', 'DefinedStyle', 'Tour', '$interval', 'RefreshWeather', 'Galaxy',
    function($anchorScroll, $location, $scope, $http, $stateParams, $state, $translate, uiGmapGoogleMapApi, uiGmapIsReady, City, CityByPlaceId,
             LogisticCenter, $timeout, FoundationApi, DefinedStyle, Tour, $interval, RefreshWeather, Galaxy) {
        var city_str = $stateParams.city;
        $scope.lc = [];
        var cities_list = [];
        var stop;
        $scope.newCoords = {lat: 0.0, lng: 0.0};
        $scope.select_coords = {actives: []};
        $scope.deactivate_coords = function(id){
            var active = $scope.select_coords.actives.findIndex(function( obj ) {
                return obj == id;
            });
            if(active != -1) {
                $scope.select_coords.actives.splice(active, 1);
            }
            if($scope.select_coords.actives.length < 1){
                var result = $scope.map.markers.findIndex(function( obj ) {
                    return obj.id == "latLngMk";
                });
                if(result != -1) {
                    $scope.map.markers.splice(result, 1);
                }
                $scope.newCoords = {lat: 0.0, lng: 0.0};
            }
        };

        City.get({},
            function (data) {
                data.results.forEach(function(city) {
                    cities_list.push(city);
                });
            }
        );

        $scope.reload_city = function (place_id) {
            CityByPlaceId.get({
                    place_id: place_id,
                    time: Date.now()
                },
                function (result) {
                    $scope.main_city = City.get({id: result.results[0].id}, function() {
                            Tour.create($scope.main_city.id, Date.now());
                            Galaxy.fly_to($scope.main_city.id, Date.now());
                            RefreshWeather.refresh($scope.main_city.id, Date.now());
                            stop = $interval(function(){callAtInterval($scope.main_city.id)}, 900000, false);
                            $scope.logistic_centers = [];
                            $scope.main_city.logistic_centers.forEach(get_logistic_centers);
                            $scope.map = {
                                center: {
                                    latitude: $scope.main_city.lat,
                                    longitude: $scope.main_city.lng
                                }, zoom: 14,
                                options: {maxZoom: 18, minZoom: 11},
                                events: {
                                    click: function (map, eventName, args) {
                                        $scope.$apply(function () {
                                            if($scope.select_coords.actives.length > 0) {
                                                latLng = args[0].latLng.toUrlValue().split(",");
                                                $scope.openMarker(parseFloat(latLng[0]), parseFloat(latLng[1]))
                                            }
                                        });
                                    }
                                },
                                markers: []
                            };
                        }
                    );
                    //prepare_map($scope.main_city.lat, $scope.main_city.lng)
                })
        };

        $scope.reload_city(city_str);

        $scope.$watchCollection('[map.center.latitude, map.center.longitude]',
            function handleFooChange(newValues) {
                if(parseFloat(newValues[0]) == newValues[0] && parseFloat(newValues[1]) == newValues[1]){
                    if(!samePlace(newValues[0], newValues[1]))
                        NearestCity(newValues[0], newValues[1]);
                }

            }
        );

        var samePlace = function(lat, lng){
            return !!(lat == $scope.main_city.lat && lng == $scope.main_city.lng);
        };

        /**
         * @return {number}
         */
        var Deg2Rad = function( deg ) {
            return deg * Math.PI / 180;
        };


        /**
         * @return {number}
         */
        var PythagorasEquirectangular = function ( lat1, lon1, lat2, lon2 )
        {
            lat1 = Deg2Rad(lat1);
            lat2 = Deg2Rad(lat2);
            lon1 = Deg2Rad(lon1);
            lon2 = Deg2Rad(lon2);
            var R = 6371; // km
            var x = (lon2-lon1) * Math.cos((lat1+lat2)/2);
            var y = (lat2-lat1);
            return Math.sqrt(x*x + y*y) * R;
        };

        var NearestCity = function ( latitude, longitude )
        {
            var mindif=99999;
            var closest;
            //console.log("cities: " + cities_list)
            for (index = 0; index < cities_list.length; ++index) {
                var dif =  PythagorasEquirectangular( latitude, longitude, cities_list[index].lat, cities_list[index].lng );
                //console.log(index + " city: " + cities_list[index].name + " diff: " + dif)
                if ( dif < mindif )
                {
                    closest=index;
                    mindif = dif;
                }
            }

            // echo the nearest city
            if( cities_list[ closest].place_id != $scope.main_city.place_id ){
                $scope.change_city(cities_list[ closest].place_id);
            }
        };

        $scope.left_menu = false;

        var get_logistic_centers = function(logistic_center){
            $scope.logistic_centers.push(logistic_center);
            $scope.lc[logistic_center.id] = false;
            $scope.add_marker_center(logistic_center.id, logistic_center.lat, logistic_center.lng, logistic_center.defined_style)
        };


        $scope.selected_center = null;
        $scope.change_center = function(index){
            $scope.selected_center = $scope.logistic_centers[index];
        };
        $scope.close_center = function(){
            $scope.selected_center = null;
        };
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


        var openCenterInfo = function (index) {
            FoundationApi.publish('LCrepresentation', 'open');
            $scope.lc[index] = true;
        };

        $scope.closeCenterInfo = function () {
            FoundationApi.publish('LCrepresentation', 'close');
        };

        $scope.add_marker_center = function(id, lat, lng, defStyle){
            DefinedStyle.get({id: defStyle},
                function (result) {
                    var marker = {
                        id: "lc" + id,
                        coords: {
                            latitude: lat,
                            longitude: lng
                        },
                        options: {
                            icon: result.lc.maps_url
                        },
                        events: {
                            click: function (marker, eventName, args) {
                                openCenterInfo(id)
                            }
                        }
                    };
                    $scope.map.markers.push(marker);
                });
        };

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
        };

        $scope.edit_marker = function(id, lat, lng){
            var result = $scope.map.markers.findIndex(function( obj ) {
                return obj.id == id;
            });
            if(result != -1) {
                    $scope.map.markers[result].coords.latitude = lat;
                    $scope.map.markers[result].coords.longitude = lng;
            }
        };

        $scope.delete_marker = function(id){
            var result = $scope.map.markers.findIndex(function( obj ) {
                return obj.id == id;
            });
            if(result != -1) {
                $scope.map.markers.splice(result, 1);
            }
        };

        $scope.getLocation = function(val) {
            return $http.get('/api/cities/', {
                params: {
                    search: val
                }
            }).then(function(res){
                var addresses = [];
                angular.forEach(res.data.results, function(item){
                    addresses.push(item);
                });
                return addresses;
            });
        };

        $scope.returnMain = function(){
            $state.transitionTo('welcome', null, { reload: true });
        };

        var callAtInterval = function(city) {
            RefreshWeather.refresh(city, Date.now());
        };

        $scope.stopInterval = function() {
            if (angular.isDefined(stop)) {
                $interval.cancel(stop);
                stop = undefined;
            }
        };

        $scope.$on('$destroy', function() {
            // Make sure that the interval is destroyed too
            $scope.stopInterval();
        });

        $scope.change_city = function(location_id){
            $state.go('main', {'city': location_id})
        }

    }]);