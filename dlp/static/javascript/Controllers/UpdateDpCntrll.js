/**
 * Created by xavi on 10/08/16.
 */
angular.module('DLPApp').controller('UpdateDpCntrll',['$scope', 'Droppoint', '$modal', '$log', 'UpdateDp',
    function ($scope, Droppoint, $modal, $log, UpdateDp){
        $scope.droppoint_backup = angular.copy($scope.droppoint);
        $scope.is_selecting = false;
        $scope.$watch('newCoords.lat', function () {
            if ($scope.is_selecting)
                $scope.droppoint.lat = $scope.newCoords.lat;
        });
        $scope.$watch('newCoords.lng', function () {
            if ($scope.is_selecting)
                $scope.droppoint.lng = $scope.newCoords.lng;
        });

        $scope.change_selecting = function(){
            $scope.is_selecting = !$scope.is_selecting;
            if($scope.is_selecting)
                $scope.select_coords.actives.push("lc" + $scope.droppoint.id);
            else
                $scope.deactivate_coords("lc" + $scope.droppoint.id)
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
                        $scope.$parent.changeMode();
                        UpdateDp.dp();
                        if($scope.is_selecting)
                            $scope.change_selecting();
                    })
            })
        };
        $scope.restore_droppoint = function(){
            $scope.droppoint.name = $scope.droppoint_backup.name;
            $scope.droppoint.lat = $scope.droppoint_backup.lat;
            $scope.droppoint.lng = $scope.droppoint_backup.lng;
            $scope.droppoint.alt = $scope.droppoint_backup.alt;
            $scope.droppoint.description = $scope.droppoint_backup.description;
        };

        $scope.cancel = function(){
            $scope.restore_droppoint();
            if($scope.is_selecting)
                $scope.change_selecting();
            $scope.$parent.changeMode();
        }
    }]);

