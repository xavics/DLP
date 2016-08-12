/**
 * Created by xavi on 14/06/16.
 */
angular.module('DLPApp').controller('CreateDroneCntrll',['$scope', 'Drone',
    function ($scope, Drone){
        $scope.newDrone = new Drone();
        $scope.newDrone.battery_life = 100;
        $scope.newDrone.logistic_center = $scope.center.id;
        $scope.newDrone.style_url = 4;
        $scope.errors = {
            'model': {'field': 'MODEL', 'text': 'REQUIRED', 'show': false},
            'plate': {'field': 'PLATE', 'text': 'REQUIRED', 'show': false}
        };
        var clean_errors = function(){
            angular.forEach($scope.errors, function(item){
                item.show = false;
            });
        };
        $scope.closeAlert = function(key) {
            $scope.errors[key].show = false;
        };
        $scope.create_new_drone = function(){
            $scope.newDrone.$save()
                .then(function(result){
                        $scope.center.drones.push(result.id);
                        $scope.newDrone = new Drone();
                        $scope.newDrone.battery_life = 100;
                        $scope.newDrone.logistic_center = $scope.center.id;
                        $scope.newDrone.style_url = 4;
                    },
                    function(data) {
                        clean_errors();
                        Object.keys(data.data).forEach(function (key) {
                            $scope.errors[key].show = true;
                            $scope.errors[key].text = data.data[key][0];
                        });
                    }
                );
        }
    }]);
