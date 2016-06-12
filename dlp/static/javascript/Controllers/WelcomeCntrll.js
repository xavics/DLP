/**
 * Created by xavi on 7/06/16.
 */
angular.module('DLPApp').controller('WelcomeCntrll',['$scope', '$http', function($scope, $http, $translate){
    $scope.something = "ju!"
    $scope.open_close_left = function(){
        $scope.$parent.left_menu = !$scope.$parent.left_menu
    }
}]);