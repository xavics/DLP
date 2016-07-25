/**
 * Created by xavi on 12/06/16.
 */
angular.module('DLPApp').controller('CreateLCCntrll',['$scope', 'LogisticCenter', 'DefinedStyle', 'UpdateLc',
    function ($scope, LogisticCenter, DefinedStyle, UpdateLc){
        DefinedStyle.get({},
            function (data) {
                $scope.def_style = [];
                data.results.forEach(function(city) {
                    $scope.def_style.push(city);
                });
            }
        );
        $scope.errors = {
            'name': {'field': 'NAME', 'text': 'REQUIRED', 'show': false},
            'lat': {'field': 'LATITUDE', 'text': 'REQUIRED', 'show': false},
            'alt': {'field': 'ALTITUDE', 'text': 'REQUIRED', 'show': false},
            'lng': {'field': 'LONGITUDE', 'text': 'REQUIRED', 'show': false},
            'address': {'field': 'ADDRESS', 'text': 'REQUIRED', 'show': false},
            'defined_style': {'field': 'STYLE', 'text': 'REQUIRED', 'show': false},
            'description': {'field': 'DESCRIPTION', 'text': 'REQUIRED', 'show': false},
        };
        $scope.newCenter = new LogisticCenter();
        $scope.newCenter.city = $scope.$parent.main_city.id;
        $scope.newCenter.radius = 50;
        $scope.$watch('newCoords.lat', function() {
            $scope.newCenter.lat = $scope.newCoords.lat;
        });
        $scope.$watch('newCoords.lng', function() {
            $scope.newCenter.lng = $scope.newCoords.lng;
        });
        $scope.create_new_center = function(){
            $scope.newCenter.$save().then(
                function(result){
                    $scope.logistic_centers.push(result);
                    $scope.newCenter = new LogisticCenter();
                    UpdateLc.lc()
                },
                function(data){
                    clean_errors();
                    Object.keys(data.data).forEach(function (key) {
                        $scope.errors[key].show = true;
                        $scope.errors[key].text = data.data[key][0];
                    });
                }
            )
        };
        var clean_errors = function(){
            angular.forEach($scope.errors, function(item){
                item.show = false;
            });
        }
        $scope.closeAlert = function(key) {
            $scope.errors[key].show = false;
        };
    }]);
