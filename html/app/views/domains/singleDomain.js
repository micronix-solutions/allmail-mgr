'use strict';

angular.module('myApp.singleDomain', ['ui.router'])

.config(['$stateProvider',function($stateProvider) {
  $stateProvider.state('app.domains.domain', {
    url: "/:domainName/details",
    views: {
      'itemsgrid@':{
        templateUrl: 'views/domains/singleDomain.html',
        controller: 'singleDomainCtrl'
      }
    },
    resolve:{
      domainName: ['$stateParams', function($stateParams){
        return $stateParams.domainName;
      }]
    }
  });
}])

.controller('singleDomainCtrl', ['$scope', '$state', '$stateParams', 'Domains', function($scope, $state, $stateParams, Domains) {
  $scope.domain_name = $stateParams.domainName
  $scope.domains = Domains.query();
}]);