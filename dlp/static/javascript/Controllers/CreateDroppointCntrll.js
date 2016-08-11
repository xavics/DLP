/**
 * Created by xavi on 15/06/16.
 */
angular.module('DLPApp').controller('CreateDroppointCntrll',['$scope', 'Droppoint', 'UpdateDp',
    function ($scope, Droppoint, UpdateDp){
        $scope.newDroppoint = new Droppoint();
        $scope.is_selecting = false;
        $scope.$watch('newCoords.lat', function () {
            if ($scope.is_selecting)
                $scope.newDroppoint.lat = $scope.newCoords.lat;
        });
        $scope.$watch('newCoords.lng', function () {
            if ($scope.is_selecting)
                $scope.newDroppoint.lng = $scope.newCoords.lng;
        });

        $scope.change_selecting = function(){
            $scope.is_selecting = !$scope.is_selecting;
            if($scope.is_selecting)
                $scope.select_coords.actives.push("dpnew");
            else
                $scope.deactivate_coords("dpnew")
        };
        $scope.create_new_droppoint = function(){
            $scope.newDroppoint.logistic_center = $scope.center.id;
            $scope.newDroppoint.$save()
                .then(function(result){
                    $scope.center.droppoints.push(result.id);
                    $scope.newDroppoint = new Droppoint();
                    UpdateDp.dp();
                    if($scope.is_selecting)
                        $scope.change_selecting();
                })
        };
    }]);
