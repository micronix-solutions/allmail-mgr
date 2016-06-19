'use strict';

angular.module('myApp.view1', ['ui.router'])

.config(['$stateProvider', function($stateProvider) {
  $stateProvider.state('app.view1', {
    url: "/view1",
    templateUrl: 'views/view1.html',
    controller: 'View1Ctrl',
    data: {
      requireLogin: false
    }
  });
}])

.controller('View1Ctrl', [function() {

}]);