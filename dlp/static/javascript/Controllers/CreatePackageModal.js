/**
 * Created by xavi on 6/07/16.
 */
angular.module('DLPApp').controller('CreatePackageModal',['$scope', '$modalInstance', 'droppoint', 'Package',
    function ($scope, $modalInstance, droppoint, Package){
        $scope.newPackage = new Package();
        var pending_style = 1;
        $scope.newPackage.drop_point = droppoint.id;
        $scope.newPackage.style_url = pending_style;
        $scope.save = function () {
            $scope.newPackage.$save()
            .then(function(result){
                    $modalInstance.close(result.id);
                })
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    }]);
