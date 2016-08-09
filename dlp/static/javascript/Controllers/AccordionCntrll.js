/**
 * Created by xavi on 12/06/16.
 */
angular.module('DLPApp').controller('AccordionCntrll',['$scope', '$http', function($scope, $http, $translate){
    $scope.modes = {};
    $scope.create_mode = function(id){
        $scope.modes[id] = "default";
    };
    $scope.get_mode = function(id){
        return $scope.modes[id];
    };

    $scope.modify_mode_lc = function(id, mode){
        $scope.modes[id] = mode
    };

    //$scope.modify_mode_drones = function(mode){
    //    $scope.modes.mode_drone = mode
    //};
    //$scope.modify_mode_droppoints = function(mode){
    //    $scope.modes.mode_drone = mode
    //};
    //$scope.modify_mode_transports = function(mode){
    //    $scope.modes.mode_drone = mode
    //};
}]);
