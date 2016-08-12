/**
 * Created by xavi on 12/06/16.
 */
angular.module('DLPApp').controller('AccordionCntrll',['$scope', '$http', 'DefinedStyle', 'FoundationApi', '$location', '$anchorScroll',
    function($scope, $http, DefinedStyle, FoundationApi, $location, $anchorScroll){

    $scope.tabs = [
        { title:"LOGISTICCENTER", content:"/static/templates/logistic_center_tab.html" },
        { title:"DRONES", content:"/static/templates/drones_view.html" },
        { title:"DROPPOINTS", content:"/static/templates/droppoints_view.html" },
        { title:"TRANSPORTS", content:"/static/templates/transports_view.html" }
    ];

    $scope.active_tab = function(tab){
        return $scope.tabs[tab].active = true;
    };

    $scope.add_marker_droppoint = function(id_center, id, lat, lng, defStyle){
            DefinedStyle.get({id: defStyle},
                function (result) {
                    var marker = {
                        id: "lc" + id_center + "dp" + id,
                        coords: {
                            latitude: lat,
                            longitude: lng
                        },
                        options: {
                            icon: result.dp.maps_url
                        },
                        events: {
                            click: function (marker, eventName, args) {
                                openDroppointTab("lc" + id_center + "dp" + id, id_center)
                            }
                        }
                    };
                    $scope.map.markers.push(marker);
                });
        };

        var openDroppointTab = function (id, id_center) {
            FoundationApi.publish('LCrepresentation', 'open');
            $scope.lc[id_center] = true;
            $scope.active_tab(2);
            if ($location.hash() !== id) {
                // set the $location.hash to `newHash` and
                // $anchorScroll will automatically scroll to it
                $location.hash(id);
            } else {
                // call $anchorScroll() explicitly,
                // since $location.hash hasn't changed
                $anchorScroll();
            }
        };
}]);
