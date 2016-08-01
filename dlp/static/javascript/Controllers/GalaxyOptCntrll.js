/**
 * Created by xavi on 12/06/16.
 */
angular.module('DLPApp').controller('GalaxyOptCntrll',['$scope', '$http', 'RefreshWeather', 'Tour', 'Demo',
    function($scope, $http, RefreshWeather, Tour, Demo){
    $scope.refresh_weather = function(city){
        RefreshWeather.refresh(city, Date.now())
    };
    $scope.play_tour = function(city){
        Tour.play(city, Date.now())
    };
    $scope.stop_tour = function(city){
        Tour.stop(city, Date.now())
    };
    $scope.run_demo = function(){
        Demo.demo()
    }
}]);
