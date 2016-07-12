/**
 * Created by xavi on 12/06/16.
 */
angular.module('DLPApp').controller('CreateLCCntrll',['$scope', 'LogisticCenter', 'City', 'UpdateLc',
    function ($scope, LogisticCenter, City, UpdateLc){
        $scope.cities_list = City.get()
        $scope.newCenter = new LogisticCenter()
        $scope.create_new_center = function(){
            $scope.newCenter.$save()
                .then(function(result){
                    $scope.logistic_centers.push(result)
                    $scope.newCenter = new LogisticCenter()
                    UpdateLc.lc()
                })
        }
    }]);
