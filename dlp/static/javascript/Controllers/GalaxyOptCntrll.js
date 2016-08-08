/**
 * Created by xavi on 12/06/16.
 */
angular.module('DLPApp').controller('GalaxyOptCntrll',['$scope', '$http', 'RefreshWeather', 'Tour', 'Demo', 'City',
    function($scope, $http, RefreshWeather, Tour, Demo, City){
        //window.alert($scope.main_city);
        //$scope.actual_city = City.get({id: $scope.main_city.id}, function(result){
        //    window.alert(result)
        //});
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
        };
        $scope.update_city = function(){
            $scope.main_city.$update()
        }
    }]);
