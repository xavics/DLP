/**
 * Created by xavi on 10/08/16.
 */
angular.module('DLPApp').controller('LogisticCenterTabCntrll',['$scope', function($scope){
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
}]);

