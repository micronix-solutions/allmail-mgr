'use strict';

angular.module('myApp.aliases', ['ui.router'])

.config(['$stateProvider',function($stateProvider) {
  $stateProvider.state('app.domains.domain.aliases', {
    url: "/aliases",
    views: {
      'domain-item@app.domains.domain': {
        templateUrl: 'views/aliases/aliases.html',
        controller: 'AliasesCtrl'
      }
    },
  });
}])

.controller('AliasesCtrl', ['$scope', 'domainName', 'Aliases', function($scope, domainName, Aliases) {
  $scope.aliases= Aliases.query({'domain': domainName});
  $scope.theDomain= domainName;
}]);