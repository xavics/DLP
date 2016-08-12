/**
 * Created by xavi on 13/06/16.
 */
angular.module('DLPApp').controller('UpdateLCCntrll',['$scope', 'LogisticCenter', 'City', 'UpdateLc', 'DefinedStyle',
    function ($scope, LogisticCenter, City, UpdateLc, DefinedStyle){
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
        $scope.center_backup = angular.copy($scope.$parent.center);
        $scope.is_selecting = false;
        $scope.$watch('newCoords.lat', function () {
            if ($scope.is_selecting)
                $scope.center.lat = $scope.newCoords.lat;
        });
        $scope.$watch('newCoords.lng', function () {
            if ($scope.is_selecting)
                $scope.center.lng = $scope.newCoords.lng;
        });

        $scope.change_selecting = function(){
            $scope.is_selecting = !$scope.is_selecting;
            if($scope.is_selecting)
                $scope.select_coords.actives.push("dp" + $scope.center.id);
            else
                $scope.deactivate_coords("dp" + $scope.center.id)
        };
        $scope.update_center = function(){
            var update_lc = LogisticCenter.get({id: $scope.center.id}, function(){
                update_lc.name = $scope.center.name;
                update_lc.lat = $scope.center.lat;
                update_lc.alt = $scope.center.alt;
                update_lc.lng = $scope.center.lng;
                update_lc.address = $scope.center.address;
                update_lc.defined_style = $scope.center.defined_style;
                update_lc.description = $scope.center.description;
                update_lc.$update()
                    .then(function(result){
                            $scope.center_backup = angular.copy($scope.center);
                            $scope.$parent.modify_mode_lc($scope.center.id, 'default');
                            if($scope.is_selecting)
                                $scope.change_selecting();
                            var markerId = "lc" + $scope.center.id
                            $scope.edit_marker(markerId, result.lat, result.lng);
                            if($scope.is_selecting)
                                $scope.change_selecting();
                        },
                        function(data){
                            clean_errors();
                            Object.keys(data.data).forEach(function (key) {
                                $scope.errors[key].show = true;
                                $scope.errors[key].text = data.data[key][0];
                            });
                        })
            });
        };
        var clean_errors = function(){
            angular.forEach($scope.errors, function(item){
                item.show = false;
            });
        };
        $scope.closeAlert = function(key) {
            $scope.errors[key].show = false;
        };
        $scope.restore_center = function(){
            $scope.$parent.center.name = angular.copy($scope.center_backup.name);
            $scope.$parent.center.address = angular.copy($scope.center_backup.address);
            $scope.$parent.center.description = angular.copy($scope.center_backup.description);
            $scope.$parent.center.lat = angular.copy($scope.center_backup.lat);
            $scope.$parent.center.lng = angular.copy($scope.center_backup.lng);
            $scope.$parent.center.alt = angular.copy($scope.center_backup.alt);
            $scope.$parent.center.city = angular.copy($scope.center_backup.city);
            $scope.$parent.center.defined_style = angular.copy($scope.center_backup.defined_style);
            $scope.$parent.modify_mode_lc($scope.center.id, 'default');
            if($scope.is_selecting)
                $scope.change_selecting();
            UpdateLc.lc()
        }
    }]);
