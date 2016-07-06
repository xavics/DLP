/**
 * Created by xavi on 12/06/16.
 */
angular.module('DLPApp').controller('AccordionCntrll',['$scope', '$http', function($scope, $http, $translate){
    $scope.modes = {mode_lc: "default", mode_drone: "default",
    mode_droppoints: "default", mode_transports: "default"}
    //$scope.mode_lc = "default";
    $scope.modify_mode_lc = function(mode){
        $scope.modes.mode_lc = mode
    }
    $scope.modify_mode_drones = function(mode){
        $scope.modes.mode_drone = mode
    }
    $scope.modify_mode_droppoints = function(mode){
        $scope.modes.mode_drone = mode
    }
    $scope.modify_mode_transports = function(mode){
        $scope.modes.mode_drone = mode
    }
}]);
