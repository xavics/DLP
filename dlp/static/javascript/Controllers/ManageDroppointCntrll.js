/**
 * Created by xavi on 15/06/16.
 */
angular.module('DLPApp').controller('ManageDroppointCntrll',['$scope', 'Droppoint', '$modal', '$log', 'UpdateDp',
    function ($scope, Droppoint, $modal, $log, UpdateDp){
        //$scope.droppoint = Droppoint.get({id: $scope.droppoint_id}, function(result) {
        //    $scope.droppoint_backup = angular.copy(result);
        //    $scope.add_marker_droppoint($scope.$parent.center.id, result.id, result.lat, result.lng, $scope.$parent.center.defined_style);
        //});
        $scope.droppoint_backup = angular.copy($scope.droppoint);
        $scope.add_marker_droppoint($scope.$parent.center.id, $scope.droppoint.id, $scope.droppoint.lat, $scope.droppoint.lng, $scope.$parent.center.defined_style);
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
        };

        $scope.$watch('newCoords.lat', function() {
            if($scope.newCoords.lat != 0)
                $scope.droppoint.lat = $scope.newCoords.lat;
        });
        $scope.$watch('newCoords.lng', function() {
            if($scope.newCoords.lng != 0)
                $scope.droppoint.lng = $scope.newCoords.lng;
        });

        $scope.delete_droppoint = function(){
            var delete_droppoint = Droppoint.get({id: $scope.droppoint.id}, function() {
                delete_droppoint.$remove()
                    .then(function(result){
                        var index_deleted = $scope.$parent.center.droppoints.indexOf($scope.droppoint);
                        $scope.$parent.center.droppoints.splice(index_deleted, 1);
                        UpdateDp.dp();
                    })
            })
        };

        $scope.update_droppoint = function(){
            var update_droppoint = Droppoint.get({id: $scope.droppoint.id}, function() {
                update_droppoint.name = $scope.droppoint.name;
                update_droppoint.lat = $scope.droppoint.lat;
                update_droppoint.lng = $scope.droppoint.lng;
                update_droppoint.alt = $scope.droppoint.alt;
                update_droppoint.description = $scope.droppoint.description;
                update_droppoint.$update()
                    .then(function (result) {
                        $scope.droppoint_backup = angular.copy(result);
                        $scope.changeMode();
                        UpdateDp.dp();
                    })
            })
        };

        $scope.restore_droppoint = function(){
            $scope.droppoint = angular.copy($scope.droppoint_backup);
        };

        $scope.open_modal = function () {

            var modalInstance = $modal.open({
                templateUrl: '/static/templates/create_package_modal.html',
                controller: 'CreatePackageModal',
                resolve: {
                    droppoint: function () {
                        return $scope.droppoint;
                    }
                }
            });

            modalInstance.result.then(function (id_package) {
                $scope.new_package_id = id_package
            }, function () {
                $log.info('Created new package with id: ' + $scope.new_package_id);
            });
        };
    }]);
