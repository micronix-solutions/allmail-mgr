'use strict';

angular.module('myApp.newAlias', ['ui.router'])

.config(['$stateProvider',function($stateProvider) {
  $stateProvider.state('app.domains.domain.aliases.new-alias', {
    url: "/new",
    views: {
      'itemsdetail@':{
        templateUrl: 'views/aliases/newAlias.html',
        controller: 'newAliasCtrl',
      }
    }
  });
}])

.controller('newAliasCtrl', ['$scope', '$state', 'domainName', '$stateParams', 'Aliases', function($scope, $state, domainName, $stateParams, Aliases) {
  $scope.theDomain = domainName;
  $scope.add = function(aliasName, forwardAddresses, active) {
    var newAlias = {
      alias_name : aliasName,
      targets : forwardAddresses,
      active : active
    }
    Aliases.create({domain : domainName}, newAlias);
    $state.go('^', null, {reload: true});
  }
  $scope.cancel = function(){
    $state.go('app.domains.domain.aliases');
  }
}]);