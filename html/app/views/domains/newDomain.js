'use strict';

angular.module('myApp.newDomain', ['ui.router'])

.config(['$stateProvider',function($stateProvider) {
  $stateProvider.state('app.domains.new', {
    views: {
      'itemsdetail@':{
        templateUrl: 'views/domains/newDomain.html',
        controller: 'newDomainCtrl'
      }
    }
  });
}])

.controller('newDomainCtrl', ['$scope', '$state', '$stateParams', 'Domains', function($scope, $state, $stateParams, Domains) {
  $scope.add = function(domainName, active) {
    var newDomain = {
      domain_name : domainName,
      active : active
    }
    Domains.create(newDomain);
    $state.go('^', null, {reload: true});
  }
  
  $scope.cancel = function(){
    $state.go('app.domains');
  }
  
}]);