/**
 * Created by xavi on 14/06/16.
 */
angular.module('DLPApp').controller('CreateDroneCntrll',['$scope', 'Drone',
    function ($scope, Drone){
        $scope.newDrone = new Drone()
        $scope.newDrone.battery_life = 100;
        $scope.newDrone.logistic_center = $scope.center.id;
        $scope.newDrone.style_url = 1;
        $scope.create_new_drone = function(){
            $scope.newDrone.$save()
                .then(function(result){
                    $scope.center.drones.push(result.id)
                    $scope.newDrone = new Drone()
                    $scope.newDrone.battery_life = 100;
                    $scope.newDrone.logistic_center = $scope.center.id;
                    $scope.newDrone.style_url = 1;
                })
        }
    }]);
