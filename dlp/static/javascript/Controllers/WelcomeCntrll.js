/**
 * Created by xavi on 7/06/16.
 */
angular.module('DLPApp').controller('WelcomeCntrll',['$scope', '$http', '$state', '$translate', '$timeout', '$modal', '$log', 'CityByPlaceId', 'City', '$interval',
    function($scope, $http, $state, $translate, $timeout, $modal, $log, CityByPlaceId, City, $interval){
        $(document).foundation('orbit', 'reflow');
        $scope.city = {name: '', lat: '', lng: '', place_id: ''};
        $scope.place_id = "";
        $scope.select = true;
        City.get({time: Date.now()},
            function (data) {
                $scope.cities_list = [];
                data.results.forEach(function(city) {
                    $scope.cities_list.push(city);
                });
            }
        );
        $scope.logos = [
            {'name': 'logo1', 'init': 'static/images/logos/logo-liquidgalaxylab-trans.png', 'hover': 'static/images/logos/logo-liquidgalaxylab.png'},
            {'name': 'logo2', 'init': 'static/images/logos/parc-logo-trans.png', 'hover': 'static/images/logos/parc-logo.jpg'},
            {'name': 'logo3', 'init': 'static/images/logos/lleidadrone-logo-trans.png', 'hover': 'static/images/logos/lleidadrone-logo.png'},
            {'name': 'logo4', 'init': 'static/images/logos/CataloniaSmartDrones-logo.png', 'hover': 'static/images/logos/CataloniaSmartDrones-logo-solid.png'},
            {'name': 'logo5', 'init': 'static/images/logos/hemav-academics1.png', 'hover': 'static/images/logos/hemav-academics-solid1.png'},
        ];
        $scope.alert = {show: false, type: 'alert', msg: 'ERROR_MESSAGE_1' };
        var timeout;
        var options = {
            types: ['(cities)']
        };
        var inputForm = document.getElementById('autocomplete_google');
        var autocompleteForm = new google.maps.places.Autocomplete(inputForm, options);
        google.maps.event.addListener(autocompleteForm, 'place_changed', function() {
            var place = autocompleteForm.getPlace();
            $scope.city.name = place.name;
            $scope.city.lat = place.geometry.location.lat();
            $scope.city.lng = place.geometry.location.lng();
            $scope.city.place_id = place.place_id;
            $scope.$apply();
        });

        $scope.saveCity = function(){
            if(!$scope.city.place_id){
                showAlert();
                return timeout = $timeout($scope.closeAlert, 5000);
            }
            CityByPlaceId.get({place_id: $scope.city.place_id, time: Date.now()}, function(data){
                if(data.results.length <= 0){
                    $scope.newCity = new City();
                    $scope.newCity.name = $scope.city.name;
                    $scope.newCity.lat = $scope.city.lat;
                    $scope.newCity.lng = $scope.city.lng;
                    $scope.newCity.place_id = $scope.city.place_id;
                    $scope.newCity.$save()
                        .then(function(result){
                            $state.go('main', {'city': result.place_id})
                    })
                }else{
                    $state.go('main', {'city': $scope.city.place_id})
                }
            });
        };

        $scope.changeTab = function(){
            $scope.select = !$scope.select;
        };

        $scope.accessDLP = function(){
            if($scope.place_id == ""){
                showAlert();
                return timeout = $timeout($scope.closeAlert, 5000);
            }
            $state.go('main', {'city': $scope.place_id})
        };

        $scope.stopTimeout = function() {
            if (angular.isDefined(timeout)) {
                $interval.cancel(timeout);
                timeout = undefined;
            }
        };

        $scope.closeAlert = function() {
            $scope.alert.show = false;
            $scope.stopTimeout();
        };

        var showAlert = function() {
            $scope.alert.show = true;
        };

        $scope.open_modal = function () {

            var modalInstance = $modal.open({
                templateUrl: '/static/templates/new_city_modal.html',
                controller: 'CreateCityModal',
                resolve: {
                    city: function () {
                        return $scope.city;
                    }
                }
            });

            modalInstance.result.then(function (id_city) {
                $scope.new_city_id = id_city;
                if($scope.new_city_id != null){
                    $log.info('Created new city with id: ' + $scope.new_city_id);
                    $state.go('main', {'city': $scope.new_city_id});
                }
            });
        };

    }]);