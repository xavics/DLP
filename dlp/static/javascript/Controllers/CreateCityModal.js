/**
 * Created by xavi on 8/07/16.
 */
angular.module('DLPApp').controller('CreateCityModal',['$scope', '$modalInstance', 'city', 'City',
    function ($scope, $modalInstance, city, City){
        $scope.city = city;
        $scope.newCity = new City();
        $scope.newCity.name = city.name;
        $scope.newCity.lat = city.lat;
        $scope.newCity.lng = city.lng;
        $scope.newCity.place_id = city.place_id;
        $scope.save = function () {
            $scope.newCity.$save()
            .then(function(result){
                    $modalInstance.close(result.place_id);
                })
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    }]);