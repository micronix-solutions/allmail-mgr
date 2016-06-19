'use strict';

angular.module('myApp.loginView', ['ui.router'])

.config(['$stateProvider',function($stateProvider) {
  $stateProvider.state('app.loginView', {
    url: "/login",
    templateUrl: 'loginView/loginView.html',
    controller: 'LoginCtrl',
  });
}])

.controller('LoginCtrl', function ($scope, UsersApi) {

  $scope.alerts = [];
  $scope.submit = function (email, password) {
    UsersApi.login(email, password).then(function (user) {
      $scope.$close(user);
    }, function(response){ $scope.alerts.push( {type: 'danger', msg: 'Invalid username or password'} ); } );
  };
  
  $scope.closeAlert = function(index) {
    $scope.alerts.splice(index, 1);
  };
  
  this.cancel = $scope.$dismiss;

});