'use strict';

angular.module('myApp.domains', ['ui.router'])

.config(['$stateProvider',function($stateProvider) {
  $stateProvider.state('app.domains', {
    url: "/domains",
    views: {
      'domainlist@':{
        templateUrl: 'views/domains/domains.html',
        controller: 'DomainsCtrl'
      }
    },
  });
}])

.controller('DomainsCtrl', ['$scope', '$state', '$stateParams', 'Domains', function($scope, $state, $stateParams, Domains) {
  
  $scope.domain_name = $stateParams.domainName
  $scope.domains = Domains.query();
  $scope.newDomain = function(){
    $state.go('app.domains.new');
  }
}]);