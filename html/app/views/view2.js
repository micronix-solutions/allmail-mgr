'use strict';

angular.module('myApp.view2', ['ui.router'])

.config(['$stateProvider',function($stateProvider) {
  $stateProvider.state('app.view2', {
    url: "/view2",
    templateUrl: 'views/view2.html',
    controller: 'View2Ctrl',
  });
}])

.controller('View2Ctrl', [function() {

}]);