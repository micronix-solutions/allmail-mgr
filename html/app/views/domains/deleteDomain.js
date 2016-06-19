'use strict';

angular.module('myApp.deleteDomain', ['ui.router', 'ui.bootstrap'])

.config(['$stateProvider',function($stateProvider) {
  $stateProvider.state('app.domains.domain.delete', {
    url: "/:domainName/delete",
    onEnter: ['$modal', '$state', function($modal, $state){
      $modal.open({
        templateUrl:'views/domains/deleteDomain.html',
        controller:'deleteDomainCtrl'
      }).result.finally(function(){
        $state.go('^', null, {reload: true});
      })
    }]
  });
}])

.controller('deleteDomainCtrl', ['$scope', '$state', '$stateParams', '$modalInstance', 'Domains', function($scope, $state, $stateParams, $modalInstance, Domains) {
  $scope.theDomain = $stateParams.domainName;
  $scope.cancel = function(){
    $modalInstance.close();
    $state.go('^');
  }
  $scope.delete = function(){
    Domains.delete({domain: $stateParams.domainName});
    $modalInstance.close();$modalInstance.close();
    $state.go('app.domains', null, {reload: true});
  }
}]);