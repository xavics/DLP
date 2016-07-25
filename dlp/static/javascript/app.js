/**
 * Created by xavi on 6/06/16.
 */
var app = angular.module('DLPApp', [
    'ui.router',
    'foundation',
    'ngResource',
    'pascalprecht.translate',
    'myServices',
    'uiGmapgoogle-maps',
    'mm.foundation'
]);
app.config(function ($stateProvider, $urlRouterProvider) {
    // For any unmatched url, send to /route1
    $urlRouterProvider.otherwise("/");
    $stateProvider
        .state('welcome', {
            url: "/",
            templateUrl: "/static/templates/welcome.html",
            controller: "WelcomeCntrll",
            cache: false
        })
        .state('main', {
            url: "/dlpView",
            templateUrl: "/static/templates/index.html",
            controller: "IndexCntrll",
            params:{
                city: {
                    value: "ChIJf9M750jgphIRr6pZ0qIu06A",
                    squash: true
                },
                hiddenParam: 'YES'
            }
        })
});
app.config(['$httpProvider', function ($httpProvider){
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.withCredentials = true;
    $httpProvider.defaults.cache=true;
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/json';
    $httpProvider.defaults.headers.common['X-CSRFToken'] = '{{ csrf_token|escapejs }}';
}]);
app.config(['uiGmapGoogleMapApiProvider', function(uiGmapGoogleMapApiProvider) {
    uiGmapGoogleMapApiProvider.configure({
        key: 'AIzaSyCTuiXVTgyiTF-BVyN8UeZi_K0Jg0Mv-cE',
        v: '3.20', //defaults to latest 3.X anyhow
        libraries: 'weather,geometry,visualization'
    });
}]);
app.config(function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
});
app.run(function($rootScope){
    $rootScope.$apply($(document).foundation());
});

