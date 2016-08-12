/**
 * Created by xavi on 15/06/16.
 */
angular.module('DLPApp').controller('ManageDroppointCntrll',['$scope', 'Droppoint', '$modal', '$log', 'UpdateDp', 'DefinedStyle', 'FoundationApi', '$location', '$anchorScroll',
    function ($scope, Droppoint, $modal, $log, UpdateDp){
        $scope.add_marker_droppoint($scope.$parent.center.id, $scope.droppoint.id, $scope.droppoint.lat, $scope.droppoint.lng, $scope.$parent.center.defined_style);
        $scope.mode = "default";

        $scope.changeMode = function(mode){
            if(mode == "edit"){
                $scope.mode = "edit"
            }
            else if(mode == "delete"){
                $scope.mode = "delete"
            }else{
                $scope.mode = "default"
            }
        };

        $scope.delete_droppoint = function(){
            var delete_droppoint = Droppoint.get({id: $scope.droppoint.id}, function() {
                delete_droppoint.$remove()
                    .then(function(result){
                        var index_deleted = $scope.$parent.center.droppoints.indexOf($scope.droppoint);
                        $scope.$parent.center.droppoints.splice(index_deleted, 1);
                        UpdateDp.dp();
                        var markerId = "lc" + $scope.center.id + "dp" + $scope.droppoint.id;
                        $scope.delete_marker(markerId);
                    })
            })
        };

        $scope.open_modal = function () {

            var modalInstance = $modal.open({
                templateUrl: '/static/templates/create_package_modal.html',
                controller: 'CreatePackageModal',
                resolve: {
                    droppoint: function () {
                        return $scope.droppoint;
                    }
                }
            });

            modalInstance.result.then(function (id_package) {
                $scope.new_package_id = id_package
            }, function () {
                $log.info('Created new package with id: ' + $scope.new_package_id);
            });
        };
    }]);
