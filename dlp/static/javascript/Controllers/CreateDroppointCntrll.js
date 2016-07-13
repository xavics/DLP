/**
 * Created by xavi on 15/06/16.
 */
angular.module('DLPApp').controller('CreateDroppointCntrll',['$scope', 'Droppoint', 'UpdateDp',
    function ($scope, Droppoint, UpdateDp){
        $scope.newDroppoint = new Droppoint()
        $scope.newDroppoint.logistic_center = $scope.center.id;
        $scope.newDroppoint.style_url = 1;
        $scope.$watch('newCoords.lat', function() {
            $scope.newDroppoint.lat = $scope.newCoords.lat;
        });
        $scope.$watch('newCoords.lng', function() {
            $scope.newDroppoint.lng = $scope.newCoords.lng;
        });
        $scope.create_new_droppoint = function(){
            $scope.newDroppoint.$save()
                .then(function(result){
                    $scope.center.droppoints.push(result.id)
                    $scope.newDroppoint = new Droppoint()
                    $scope.newDroppoint.logistic_center = $scope.center.id;
                    $scope.newDroppoint.style_url = 1;
                    UpdateDp.dp()
                })
        };
    }]);
