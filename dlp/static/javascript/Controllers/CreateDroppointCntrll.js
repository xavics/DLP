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
        $scope.errors = {
            'name': {'field': 'NAME', 'text': 'REQUIRED', 'show': false},
            'lat': {'field': 'LATITUDE', 'text': 'REQUIRED', 'show': false},
            'alt': {'field': 'ALTITUDE', 'text': 'REQUIRED', 'show': false},
            'lng': {'field': 'LONGITUDE', 'text': 'REQUIRED', 'show': false},
            'description': {'field': 'DESCRIPTION', 'text': 'REQUIRED', 'show': false},
        };
        var clean_errors = function(){
            angular.forEach($scope.errors, function(item){
                item.show = false;
            });
        };
        $scope.closeAlert = function(key) {
            $scope.errors[key].show = false;
        };
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
                    $scope.center.droppoints.push(result);
                    debugger;
                    UpdateDp.dp();
                    if($scope.is_selecting) {
                        $scope.change_selecting();
                    }
                    $scope.add_marker_droppoint($scope.center.id, result.id, result.lat, result.lng, $scope.center.defined_style);
                    $scope.newDroppoint = new Droppoint();
                },
                function(data){
                    clean_errors();
                    Object.keys(data.data).forEach(function (key) {
                        $scope.errors[key].show = true;
                        $scope.errors[key].text = data.data[key][0];
                    });
                })
        };
    }]);
