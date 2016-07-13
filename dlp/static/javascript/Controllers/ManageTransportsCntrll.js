/**
 * Created by xavi on 4/07/16.
 */
angular.module('DLPApp').controller('ManageTransportsCntrll',['$scope', '$interval', 'TransportByLc', 'Transport',
    function ($scope, $interval, TransportByLc, Transport){
        var stop;
        var transports = TransportByLc.get({
            logistic_center: $scope.$parent.center.id,
            status: 1,
            time: Date.now()
        }, function () {
            $scope.transports = transports.results;
            stop = $interval(callAtInterval, 3000, false);
        });

        var callAtInterval = function() {
            TransportByLc.get({
                logistic_center: $scope.$parent.center.id,
                status: 1,
                time: Date.now()
            },function (result){
                for(var i=0; i<$scope.transports.length; i++){
                    var modified = false;
                    for(var k=0; k<result.results.length; k++){
                        if($scope.transports[i].id == result.results[k].id){
                            $scope.transports[i].step = result.results[k].step
                            result.results.splice(k, 1)
                            modified = true
                        }
                    }
                    if(!modified){
                        $scope.transports.splice(i,1)
                    }
                }
                if(result.results.length>0){
                    for(var z=0; z<result.results.length;z++){
                        $scope.transports.push(result.results[z])
                    }
                }
            })
        }

        $scope.stopInterval = function() {
          if (angular.isDefined(stop)) {
            $interval.cancel(stop);
            stop = undefined;
          }
        };

        $scope.$on('$destroy', function() {
          // Make sure that the interval is destroyed too
          $scope.stopInterval();
        });

    }]);



