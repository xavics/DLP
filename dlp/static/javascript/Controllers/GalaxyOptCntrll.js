/**
 * Created by xavi on 12/06/16.
 */
angular.module('DLPApp').controller('GalaxyOptCntrll',['$scope', '$http', 'RefreshWeather', function($scope, $http, RefreshWeather){
    $scope.refresh_weather = function(city){
        RefreshWeather.refresh(city)
    };
}]);
