/**
 * Created by xavi on 6/06/16.
 */
var app = angular.module('DLPApp', [
    'ui.router',
    'mm.foundation',
    'ngResource',
    'pascalprecht.translate',
    'myServices'
]);
app.config(function ($stateProvider, $urlRouterProvider) {
    // For any unmatched url, send to /route1
    $urlRouterProvider.otherwise("/");
    $stateProvider
        .state('index', {
            url: "/",
            templateUrl: "/static/templates/welcome.html",
            controller: "WelcomeCntrll"
        })
        .state('main', {
            url: "/dlpView",
            templateUrl: "/static/templates/index.html",
            controller: "IndexCntrll",
            params:{
                city: "1"
            }
        })
});
app.config(['$httpProvider', function ($httpProvider){
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.withCredentials = true;
    $httpProvider.defaults.cache=true;
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
}]);
app.config(['$translateProvider', function ($translateProvider) {
    $translateProvider.translations('en', {
        'INFORMATION': 'Information',
        'LOGISTICCENTER': 'Logistic Center',
        'DRONES': 'Drones'
    });

    $translateProvider.translations('es', {
        'INFORMATION': 'Información',
        'LOGISTICCENTER': 'Centro Logístico',
        'DRONES': 'Drones'
    });

    $translateProvider.preferredLanguage('en');
}]);

