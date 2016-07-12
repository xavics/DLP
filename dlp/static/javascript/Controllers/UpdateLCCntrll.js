/**
 * Created by xavi on 13/06/16.
 */
angular.module('DLPApp').controller('UpdateLCCntrll',['$scope', 'LogisticCenter', 'City', 'UpdateLc',
    function ($scope, LogisticCenter, City, UpdateLc){
        $scope.cities_list = City.get();
        $scope.center_backup = angular.copy($scope.$parent.center);
        $scope.update_center = function(){
            $scope.center.$update()
                .then(function(result){
                    $scope.$parent.modify_mode_lc('Default');
                })
        }
        $scope.restore_center = function(){
            $scope.$parent.center.name = angular.copy($scope.center_backup.name);
            $scope.$parent.center.address = angular.copy($scope.center_backup.address);
            $scope.$parent.center.description = angular.copy($scope.center_backup.description);
            $scope.$parent.center.lat = angular.copy($scope.center_backup.lat);
            $scope.$parent.center.lng = angular.copy($scope.center_backup.lng);
            $scope.$parent.center.alt = angular.copy($scope.center_backup.alt);
            $scope.$parent.center.radius = angular.copy($scope.center_backup.radius);
            $scope.$parent.center.city = angular.copy($scope.center_backup.city);
            // $scope.$parent.center.style_url = angular.copy($scope.center_backup.name);
            $scope.$parent.modify_mode_lc('Default');
            UpdateLc.lc()
        }
    }]);
