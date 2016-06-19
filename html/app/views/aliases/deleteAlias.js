'use strict';

angular.module('myApp.deleteMailbox', ['ui.router', 'ui.bootstrap'])

.config(['$stateProvider',function($stateProvider) {
  $stateProvider.state('app.domains.domain.mailboxes.mailbox.delete', {
    url: "/:mailboxName/delete",
    onEnter: ['$modal', '$state', 'domainName', function($modal, $state, domainName){
      $modal.open({
        templateUrl:'views/mailboxes/deleteMailbox.html',
        controller:'deleteMailboxCtrl',
        resolve: {
          domainName: function() {return domainName; }
        }
      }).result.finally(function(){
        $state.go('^', null, {reload: true});
      })
    }]
  });
}])

.controller('deleteMailboxCtrl', ['$scope', '$state', 'domainName', '$stateParams', '$modalInstance', 'Mailboxes', function($scope, $state, domainName, $stateParams, $modalInstance, Mailboxes) {
  $scope.theDomain = domainName;
  $scope.theMailbox = $stateParams.mailboxName;
  $scope.cancel = function(){
    $modalInstance.close();
    $state.go('^');
  }
  $scope.delete = function(){
    Mailboxes.delete({domain: domainName, mailbox: $stateParams.mailboxName});
    $modalInstance.close();$modalInstance.close();
    $state.go('app.domains.domain.mailboxes', null, {reload: true});
  }
}]);