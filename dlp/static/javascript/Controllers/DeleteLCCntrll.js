/**
 * Created by xavi on 5/08/16.
 */
/**
 * Created by xavi on 13/06/16.
 */
angular.module('DLPApp').controller('DeleteLCCntrll',['$scope', 'LogisticCenter', 'UpdateLc',
    function ($scope, LogisticCenter, UpdateLc){
        $scope.delete = function() {
            LogisticCenter.get({id: $scope.center.id}, function (result) {
                result.$remove()
                    .then(function (result) {
                        var index_deleted = $scope.$parent.logistic_centers.indexOf($scope.center);
                        $scope.$parent.logistic_centers.splice(index_deleted, 1);
                        var markerId = "lc" + result.id;
                        $scope.delete_marker(markerId);
                        UpdateLc.lc();
                    })
            });
        };
        $scope.cancel = function(){
            $scope.$parent.modify_mode_lc($scope.center.id, 'default');
        }
    }]);

