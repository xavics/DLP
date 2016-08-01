/**
 * Created by xavi on 7/06/16.
 */
angular.module('DLPApp').controller('IndexCntrll',['$anchorScroll', '$location', '$scope', '$http', '$stateParams', '$state', '$translate', 'uiGmapGoogleMapApi',
    'uiGmapIsReady', 'City', 'CityByPlaceId', 'LogisticCenter', '$timeout', 'FoundationApi', 'DefinedStyle', 'Tour',
    function($anchorScroll, $location, $scope, $http, $stateParams, $state, $translate, uiGmapGoogleMapApi, uiGmapIsReady, City, CityByPlaceId,
             LogisticCenter, $timeout, FoundationApi, DefinedStyle, Tour) {
        var city_str = $stateParams.city;
        $scope.lc = [];
        var cities_list = [];
        City.get({time: Date.now()},
            function (data) {
                data.results.forEach(function(city) {
                    cities_list.push(city);
                });
            }
        );

        $scope.reload_city = function (place_id) {
            $scope.main_city = CityByPlaceId.get({
                    place_id: place_id,
                    time: Date.now()
                },
                function () {
                    $scope.main_city = $scope.main_city.results[0];
                    Tour.create($scope.main_city.id, Date.now());
                    $scope.logistic_centers = [];
                    $scope.main_city.logistic_centers.forEach(get_logistic_centers);
                    $scope.map = {
                        center: {
                            latitude: $scope.main_city.lat,
                            longitude: $scope.main_city.lng
                        }, zoom: 14,
                        options: {maxZoom: 18, minZoom: 11},
                        events: {
                            click: function (map, eventNmae, args) {
                                $scope.$apply(function () {
                                    latLng = args[0].latLng;
                                    $scope.openMarker(latLng.lat(), latLng.lng())
                                });
                            }
                        },
                        markers: []
                    };
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
                $scope.reload_city(cities_list[ closest].place_id);
            }
        };

        $scope.changeLanguage = function (key) {
            $translate.use(key);
        };
        $scope.left_menu = false;
        get_logistic_centers = function(item){
            var logistic_center = LogisticCenter.get({id: item},
                function () {
                    $scope.logistic_centers.push(logistic_center);
                    $scope.lc[logistic_center.id] = false;
                    $scope.add_marker_center(logistic_center.id, logistic_center.lat, logistic_center.lng, logistic_center.defined_style)
                });
        };

        $scope.openAccordion = function() {

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
            //$scope.lc[index] = !$scope.lc[index];
            $scope.lc[index] = true;
        };

        var openDroppointTab = function (id_center, id) {
            FoundationApi.publish('LCrepresentation', 'open');
            $scope.lc[id_center] = true;
            var tabName = 'tabDpLc' + id_center;
            console.log(tabName);
            //angular.element(document.querySelector(tabName)).active = true;
            elem = document.getElementById(tabName);
            //document.getElementById(tabName).setAttribute("active", "true");
            //$scope.lc[id] = !$scope.lc[id];
            var newHash = "lc" + id_center + "dp" + id;
            if ($location.hash() !== newHash) {
                // set the $location.hash to `newHash` and
                // $anchorScroll will automatically scroll to it
                $location.hash(newHash);
            } else {
                // call $anchorScroll() explicitly,
                // since $location.hash hasn't changed
                $anchorScroll();
            }
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

        $scope.add_marker_droppoint = function(id_center, id, lat, lng, defStyle){
            DefinedStyle.get({id: defStyle},
                function (result) {
                    var marker = {
                        id: "lc" + id_center + "dp" + id,
                        coords: {
                            latitude: lat,
                            longitude: lng
                        },
                        options: {
                            icon: result.dp.maps_url
                        },
                        events: {
                            click: function (marker, eventName, args) {
                                openDroppointTab(id_center, id)
                            }
                        }
                    };
                    $scope.map.markers.push(marker);
                });
        };

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
        }


    }]);