/**
 * Created by xavi on 15/06/16.
 */
angular.module('DLPApp').controller('ManageDroppointCntrll',['$scope', 'Droppoint',
    function ($scope, Droppoint){
        $scope.droppoint = Droppoint.get({id: $scope.droppoint_id}, function(result) {
            $scope.droppoint_backup = angular.copy(result);
            $scope.add_marker_droppoint($scope.$parent.center.id, result.id, result.lat, result.lng)
        });
        $scope.mode = "default";
        $scope.changeMode = function(mode){
            if(mode == "edit"){
                $scope.mode = "edit"
            }
            else if(mode == "delete"){
                $scope.mode = "delete"
            }else{
                $scope.restore_droppoint()
                $scope.mode = "default"
            }
        }
        $scope.delete_droppoint = function(){
            $scope.droppoint.$remove()
                .then(function(result){
                    var index_deleted = $scope.$parent.center.droppoints.indexOf($scope.droppoint_id)
                    $scope.$parent.center.droppoints.splice(index_deleted, 1)
                })
        }
        $scope.update_droppoint = function(){
            $scope.droppoint.$update()
                .then(function(result){
                    $scope.droppoint_backup = angular.copy(result);
                    $scope.changeMode()
                })
        }
        $scope.restore_droppoint = function(){
            $scope.droppoint = angular.copy($scope.droppoint_backup);
        }
    }]);
