'use strict';

// Declare app level module which depends on views, and components
var app = angular.module('myApp', [
  'ui.router',
  'ui.bootstrap',
  'ngResource',
  'ngAnimate',
  'myApp.view1',
  'myApp.view2',
  'myApp.domains',
  'myApp.singleDomain',
  'myApp.newDomain',
  'myApp.deleteDomain',
  'myApp.mailboxes',
  'myApp.singleMailbox',
  'myApp.newMailbox',
  'myApp.deleteMailbox',
  'myApp.setPassword',
  'myApp.aliases',
  'myApp.newAlias',
  'myApp.singleAlias',
  'myApp.loginView',
  'myApp.version'
]);

app.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {
  $urlRouterProvider.otherwise('/domains');
  $stateProvider.state('app', {
      abstract: true,
      templateUrl: 'app.html',
      data: {
        requireLogin: true // this property will apply to all children of 'app'
      }
    })

}]);

app.config(function ($httpProvider) {

  $httpProvider.interceptors.push(function ($timeout, $q, $injector) {
    var loginModal, $http, $state;

    // this trick must be done so that we don't receive
    // `Uncaught Error: [$injector:cdep] Circular dependency found`
    $timeout(function () {
      loginModal = $injector.get('loginModal');
      $http = $injector.get('$http');
      $state = $injector.get('$state');
    });

    return {
      responseError: function (rejection) {
        if (rejection.status !== 401) {
          return $q.reject(rejection);
        }

        var deferred = $q.defer();

        loginModal()
          .then(function () {
            deferred.resolve( $http(rejection.config) );
          })
          .catch(function () {
            $state.go('welcome');
            deferred.reject(rejection);
          });

        return deferred.promise;
      }
    };
  });

});

app.run(function ($rootScope, $state, loginModal) {

  $rootScope.$on('$stateChangeStart', function (event, toState, toParams) {
    var requireLogin = toState.data.requireLogin;

    if (requireLogin && typeof $rootScope.currentUser === 'undefined') {
      event.preventDefault();
      // get me a login modal!
      loginModal()
        .then(function () {
          return $state.go(toState.name, toParams);
        })
        .catch(function () {
          return $state.go('app.view1');
        });
    }
  });

});

