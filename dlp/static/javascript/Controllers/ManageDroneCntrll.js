/**
 * Created by xavi on 14/06/16.
 */
angular.module('DLPApp').controller('ManageDroneCntrll',['$scope', 'Drone',
    function ($scope, Drone){
        $scope.drone = Drone.get({id: $scope.drone_id}, function(result) {
            $scope.drone_backup = angular.copy(result);
        });
        $scope.mode = "default";
        $scope.changeMode = function(mode){
            if(mode == "edit"){
                $scope.mode = "edit"
            }
            else if(mode == "delete"){
                $scope.mode = "delete"
            }else{
                $scope.restore_drone()
                $scope.mode = "default"
            }
        }
        $scope.delete_drone = function(){
            $scope.drone.$remove()
                .then(function(result){
                    var index_deleted = $scope.$parent.center.drones.indexOf($scope.drone_id)
                    $scope.$parent.center.drones.splice(index_deleted, 1)
                })
        }
        $scope.update_drone = function(){
            $scope.drone.$update()
                .then(function(result){
                    $scope.drone_backup = angular.copy(result);
                    $scope.changeMode()
                })
        }
        $scope.restore_drone = function(){
            $scope.drone = angular.copy($scope.drone_backup);
        }
    }]);
