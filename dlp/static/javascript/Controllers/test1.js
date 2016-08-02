/**
 * Created by xavi on 7/06/16.
 */
angular.module('DLPApp').controller('test1',['$scope', '$http', '$state', '$translate', '$timeout', '$log', 'CityByPlaceId', 'City', '$interval',
    function($scope, $http, $state, $translate, $timeout, $log, CityByPlaceId, City, $interval){
        $scope.new_city = {name: '', lat: '', lng: '', place_id: ''};
        //$scope.alert = {show: false, type: 'alert', msg: 'ERROR_MESSAGE_1' };
        var timeout;
        var options = {
            types: ['(cities)']
        };
        var inputForm = document.getElementById('autocomplete_google');
        var autocompleteForm = new google.maps.places.Autocomplete(inputForm, options);
        google.maps.event.addListener(autocompleteForm, 'place_changed', function() {
            var place = autocompleteForm.getPlace();
            $scope.new_city.name = place.name;
            $scope.new_city.lat = place.geometry.location.lat();
            $scope.new_city.lng = place.geometry.location.lng();
            $scope.new_city.place_id = place.place_id;
            $scope.$apply();
        });

        $scope.saveCity = function(){
            if(!$scope.new_city.place_id){
                showAlert();
                return timeout = $timeout($scope.closeAlert, 5000);
            }
            CityByPlaceId.get({place_id: $scope.new_city.place_id, time: Date.now()}, function(data){
                if(data.results.length <= 0){
                    $scope.newCity = new City();
                    $scope.newCity.name = $scope.new_city.name;
                    $scope.newCity.lat = $scope.new_city.lat;
                    $scope.newCity.lng = $scope.new_city.lng;
                    $scope.newCity.place_id = $scope.new_city.place_id;
                    $scope.newCity.$save()
                        .then(function(result){
                            $state.go('main', {'city': result.place_id})
                    })
                }else{
                    $state.go('main', {'city': $scope.new_city.place_id})
                }
            });
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

    }]);
