/**
 * Created by xavi on 7/06/16.
 */
angular.module('DLPApp').controller('WelcomeCntrll',['$scope', '$http', '$state', '$translate', '$timeout', '$log', 'CityByPlaceId', 'City', '$interval',
    function($scope, $http, $state, $translate, $timeout, $log, CityByPlaceId, City, $interval){
        $scope.city = {name: '', lat: '', lng: '', place_id: ''};
        $scope.place_id = "";
        $scope.select = true;
        City.get({},
            function (data) {
                $scope.cities_list = [];
                data.results.forEach(function(city) {
                    $scope.cities_list.push(city);
                });
            }
        );
        $scope.logos = [
            {'name': 'logo1', 'init': 'static/images/logos/logo-liquidgalaxylab-trans.png', 'href': 'http://www.liquidgalaxylab.com/'},
            {'name': 'logo2', 'init': 'static/images/logos/parc-logo-trans.png', 'href': 'http://www.parcteclleida.es/'},
            {'name': 'logo3', 'init': 'static/images/logos/lleidadrone-logo-trans.png', 'href': 'http://www.lleidadrone.com/'},
            {'name': 'logo4', 'init': 'static/images/logos/CataloniaSmartDrones-logo.png', 'href': '#/'},
            {'name': 'logo5', 'init': 'static/images/logos/hemav-academics1.png', 'href': 'http://hemav.com/academics/'},
        ];
        $scope.alert = {show: false, type: 'alert', msg: 'ERROR_MESSAGE_1' };
        var timeout;
        $scope.changeTab = function(){
            $scope.select = !$scope.select;
        };

        $scope.accessDLP = function(){
            if($scope.city.place_id == ""){
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

        //$scope.open_modal = function () {
        //
        //    var modalInstance = $modal.open({
        //        templateUrl: '/static/templates/new_city_modal.html',
        //        controller: 'CreateCityModal',
        //        resolve: {
        //            city: function () {
        //                return $scope.city;
        //            }
        //        }
        //    });
        //
        //    modalInstance.result.then(function (id_city) {
        //        $scope.new_city_id = id_city;
        //        if($scope.new_city_id != null){
        //            $log.info('Created new city with id: ' + $scope.new_city_id);
        //            $state.go('main', {'city': $scope.new_city_id});
        //        }
        //    });
        //};

    }]);