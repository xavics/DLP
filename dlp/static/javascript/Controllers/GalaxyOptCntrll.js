/**
 * Created by xavi on 12/06/16.
 */
angular.module('DLPApp').controller('GalaxyOptCntrll',['$scope', '$http', 'RefreshWeather', 'Tour', 'Demo', 'City', '$translate', '$timeout',
    function($scope, $http, RefreshWeather, Tour, Demo, City, $translate, $timeout){
        $scope.alert = {
            'error': {'text': 'ERROR_UPDATING_FLYING_ALT', 'show': false},
            'success': {'text': 'ERROR_UPDATING_FLYING_ALT', 'show': false}
        };
        $scope.closeAlert = function(key) {
            $scope.alert[key].show = false;
        };
        $scope.languages = [
            {'name': 'ENGLISH', 'key': 'en', 'selected': $translate.use() == 'en'},
            {'name': 'SPANISH', 'key': 'es', 'selected': $translate.use() == 'es'}
        ];
        $scope.selected_language = $translate.use();
        $scope.refresh_weather = function(city){
            RefreshWeather.refresh(city, Date.now())
        };
        $scope.play_tour = function(city){
            Tour.play(city, Date.now())
        };
        $scope.stop_tour = function(city){
            Tour.stop(city, Date.now())
        };
        $scope.run_demo = function(){
            Demo.demo()
        };
        $scope.update_city = function(){
            $scope.main_city.$update()
                .then(function(result){
                        $scope.alert.success.show = true;
                        $timeout(function(){$scope.alert.success.show = false}, 2000);
                    },
                    function(data){
                        $scope.alert.error.show = true;
                        $timeout(function(){$scope.alert.error.show = false}, 2000);
                    })
        };
        $scope.changeLanguage = function (key) {
            $translate.use(key);
        };
    }]);
