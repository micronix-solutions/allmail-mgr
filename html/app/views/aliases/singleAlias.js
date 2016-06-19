'use strict';

angular.module('myApp.singleAlias', ['ui.router'])

.config(['$stateProvider',function($stateProvider) {
  $stateProvider.state('app.domains.domain.aliases.alias', {
    url: "/:aliasName/details",
    views: {
      'itemsdetail@':{
        templateUrl: 'views/aliases/singleAlias.html',
        controller: 'singleAliasCtrl',
      }
    }
  });
}])

.controller('singleAliasCtrl', ['$scope', '$state', 'domainName', '$stateParams', 'Aliases', function($scope, $state, domainName, $stateParams, Aliases) {
  $scope.alias = Aliases.get({'domain': domainName, 'alias': $stateParams.aliasName});
  $scope.theDomain = domainName;
  $scope.save = function(){
    Aliases.update({domain: domainName, alias: $scope.alias.alias}, $scope.alias);
    $state.go('^', null, {reload: true});
  }
  $scope.cancel = function(){
    $state.go('app.domains.domain.aliases');
  }
  $scope.delete = function(){
    Aliases.delete({domain: domainName, alias: $scope.aliases.alias});
    $state.go('^', null, {reload: true});
  }
}]);