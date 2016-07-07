/**
 * Created by xavi on 6/07/16.
 */
angular.module('DLPApp').controller('CreatePackageModal',['$scope', '$modalInstance', 'droppoint', 'Package',
    function ($scope, $modalInstance, droppoint, Package){
        $scope.newPackage = new Package();
        $scope.newPackage.dropPoint = droppoint.id;
        $scope.newPackage.style_url = 1;
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
