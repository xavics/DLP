/**
 * Created by xavi on 12/06/16.
 */
angular.module('DLPApp').controller('AccordionCntrll',['$scope', '$http', function($scope, $http, $translate){

    $scope.tabs = [
        { title:"LOGISTICCENTER", content:"/static/templates/logistic_center_tab.html" },
        { title:"DRONES", content:"/static/templates/drones_view.html" },
        { title:"DROPPOINTS", content:"/static/templates/droppoints_view.html" },
        { title:"TRANSPORTS", content:"/static/templates/transports_view.html" }
    ];

    $scope.active_tab = function(tab){
        return $scope.tabs[tab].active = true;
    };
}]);
