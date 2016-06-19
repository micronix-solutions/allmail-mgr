'use strict';

angular.module('myApp.setPassword', ['ui.router', 'ui.bootstrap'])

.config(['$stateProvider',function($stateProvider) {
  $stateProvider.state('app.domains.domain.mailboxes.mailbox.setpassword', {
    url: "/:mailboxName/passwords",
    onEnter: ['$modal', '$state', 'domainName', function($modal, $state, domainName){
      $modal.open({
        templateUrl:'views/mailboxes/setPassword.html',
        controller:'setPasswordCtrl',
        resolve: {
          domainName: function() {return domainName; }
        }
      }).result.finally(function(){
        $state.go('^', null, {reload: true});
      })
    }]
  });
}])

.controller('setPasswordCtrl', ['$scope', '$state', 'domainName', '$stateParams', '$modalInstance', 'MailboxPasswords', function($scope, $state, domainName, $stateParams, $modalInstance, MailboxPasswords) {
  $scope.theDomain = domainName;
  $scope.theMailbox = $stateParams.mailboxName;
  
  $scope.cancel = function(){
    $modalInstance.close();
    $state.go('^');
  }
  
  $scope.submit = function(newPassword){
    var password_update = {
      password: newPassword
    }
    MailboxPasswords.update({domain: domainName, mailbox: $stateParams.mailboxName}, password_update);
    $modalInstance.close();$modalInstance.close();
    $state.go('^', null, {reload: true});
  }
}]);