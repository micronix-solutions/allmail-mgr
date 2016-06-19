'use strict';

angular.module('myApp.singleMailbox', ['ui.router'])

.config(['$stateProvider',function($stateProvider) {
  $stateProvider.state('app.domains.domain.mailboxes.mailbox', {
    url: "/:mailboxName/details",
    views: {
      'itemsdetail@':{
        templateUrl: 'views/mailboxes/singleMailbox.html',
        controller: 'singleMailboxCtrl',
      }
    }
  });
}])

.controller('singleMailboxCtrl', ['$scope', '$state', 'domainName', '$stateParams', 'Mailboxes', function($scope, $state, domainName, $stateParams, Mailboxes) {
  $scope.mailbox = Mailboxes.get({'domain': domainName, 'mailbox': $stateParams.mailboxName});
  $scope.theDomain = domainName;
  $scope.save = function(){
    Mailboxes.update({domain: domainName, mailbox: $scope.mailbox.mailbox}, $scope.mailbox);
    $state.go('^', null, {reload: true});
  }
  $scope.cancel = function(){
    $state.go('app.domains.domain.mailboxes');
  }
  $scope.delete = function(){
    Mailboxes.delete({domain: domainName, mailbox: $scope.mailbox.mailbox});
    $state.go('^', null, {reload: true});
  }
}]);