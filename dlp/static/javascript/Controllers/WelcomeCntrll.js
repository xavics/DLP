/**
 * Created by xavi on 7/06/16.
 */
angular.module('DLPApp').controller('WelcomeCntrll',['$scope', '$http', function($scope, $http, $translate){
    $(document).foundation('orbit', 'reflow');
    $scope.logos = [
        {'name': 'logo1', 'init': 'static/images/logos/logo-liquidgalaxylab-trans.png', 'hover': 'static/images/logos/logo-liquidgalaxylab.png'},
        {'name': 'logo2', 'init': 'static/images/logos/parc-logo-trans.png', 'hover': 'static/images/logos/parc-logo.jpg'},
        {'name': 'logo3', 'init': 'static/images/logos/lleidadrone-logo-trans.png', 'hover': 'static/images/logos/lleidadrone-logo.png'},
        {'name': 'logo4', 'init': 'static/images/logos/CataloniaSmartDrones-logo.png', 'hover': 'static/images/logos/CataloniaSmartDrones-logo-solid.png'},
        {'name': 'logo5', 'init': 'static/images/logos/hemav-academics.png', 'hover': 'static/images/logos/hemav-academics-solid.png'},
    ]
}]);