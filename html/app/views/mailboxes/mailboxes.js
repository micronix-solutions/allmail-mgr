'use strict';

angular.module('myApp.mailboxes', ['ui.router'])

.config(['$stateProvider',function($stateProvider) {
  $stateProvider.state('app.domains.domain.mailboxes', {
    url: "/mailboxes",
    views: {
      'domain-item@app.domains.domain': {
        templateUrl: 'views/mailboxes/mailboxes.html',
        controller: 'MailboxesCtrl'
      }
    },
  });
}])

.controller('MailboxesCtrl', ['$scope', 'domainName', 'Mailboxes', function($scope, domainName, Mailboxes) {
  $scope.mailboxes= Mailboxes.query({'domain': domainName});
  $scope.theDomain= domainName;
}]);