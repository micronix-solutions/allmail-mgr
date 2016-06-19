'use strict';

angular.module('myApp.newMailbox', ['ui.router'])

.config(['$stateProvider',function($stateProvider) {
  $stateProvider.state('app.domains.domain.mailboxes.new-mailbox', {
    url: "/new",
    views: {
      'itemsdetail@':{
        templateUrl: 'views/mailboxes/newMailbox.html',
        controller: 'newMailboxCtrl',
      }
    }
  });
}])

.controller('newMailboxCtrl', ['$scope', '$state', 'domainName', '$stateParams', 'Mailboxes', function($scope, $state, domainName, $stateParams, Mailboxes) {
  $scope.theDomain = domainName;
  $scope.add = function(mailboxName, password, quotaGB, isDomainAdmin, isGlobalAdmin, active) {
    var newBox = {
      mailbox_name : mailboxName,
      password : password,
      quota_gb : quotaGB,
      is_domain_admin : isDomainAdmin,
      is_global_admin : isGlobalAdmin,
      active : active
    }
    Mailboxes.create({domain : domainName}, newBox);
    $state.go('^', null, {reload: true});
  }
  $scope.cancel = function(){
    $state.go('app.domains.domain.mailboxes');
  }
}]);