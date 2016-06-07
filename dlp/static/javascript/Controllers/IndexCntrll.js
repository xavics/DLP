/**
 * Created by xavi on 7/06/16.
 */
angular.module('DLPApp').controller('IndexCntrll',['$scope', '$http', '$stateParams', '$translate', 'LogisticCenter',
    function($scope, $stateParams, $http, $translate, LogisticCenter){
        var city = $stateParams.city;
        $scope.changeLanguage = function (key) {
            $translate.use(key);
        };

        $scope.models = LogisticCenter.get({city: 1});
        $scope.groups = [
            {
                id: 1,
                logisticCenter: {add: "c/ Noseque", description: "blaBLA", lat: "", lon:"", city:"Lleida"},
                drones: [{model: "AA81", plate: "ABCD"},{model: "AA81", plate: "ABCD"}],
                droppoint: [{name: "dp3", description: "asjdnbiufbd"}, {name: "dp4", description: "asjdnbiufbd"}],
                packages: [{name:"dummy3", droppoint: "dp3"},{name:"dummy3", droppoint: "dp4"}],
                transports: [{plate: "1234"}]
            },
            {
                id: 2,
                logisticCenter: {add: "c/ Noseque", description: "blaBLA", lat: "", lon:"", city:"Lleida"},
                drones: [{model: "AA81", plate: "ABCD"},{model: "AA81", plate: "ABCD"}],
                droppoint: [{name: "dp3", description: "asjdnbiufbd"}, {name: "dp4", description: "asjdnbiufbd"}],
                packages: [{name:"dummy3", droppoint: "dp3"},{name:"dummy3", droppoint: "dp4"}],
                transports: [{plate: "1234"}]
            }
        ];

        $scope.items = ['Item 1', 'Item 2', 'Item 3'];

        $scope.addItem = function() {
            var newItemNo = $scope.items.length + 1;
            $scope.items.push('Item ' + newItemNo);
        };
    }])