'use strict';

app.service('loginModal', function ($modal, $rootScope) {

  function assignCurrentUser (user) {
    $rootScope.currentUser = user;
    return user;
  }

  return function() {
    var instance = $modal.open({
      templateUrl: 'views/loginView.html',
      controller: 'LoginCtrl',
      controllerAs: 'LoginCtrl'
    })

    return instance.result.then(assignCurrentUser);
  };

});

app.service('UsersApi', function($rootScope, $http, $q){
  this.login = function(email, password){
    return $http.post('/api/login', {user: email, password: password}).
      then(function(response){
        return response.data;
      }, function(response){
        return $q.reject(response);
    });
  }
});

app.factory('Domains', ['$resource', '$rootScope', function($resource, $rootScope){
  return $resource(
    '/api/domains/:domain',
    null, 
    {
      'query' : {method: 'GET', headers: {'Authorization': 'Token ' + $rootScope.currentUser.token}, isArray:true},
      'create' : {method: 'POST', headers: {'Authorization': 'Token ' + $rootScope.currentUser.token}},
      'delete' : {method: 'DELETE', headers: {'Authorization': 'Token ' + $rootScope.currentUser.token}}
    }
    );
}]);

app.factory('Mailboxes', ['$resource', '$rootScope', function($resource, $rootScope){
  return $resource(
    '/api/domains/:domain/mailboxes/:mailbox',
    null, 
    {
      'query' : {method: 'GET', headers: {'Authorization': 'Token ' + $rootScope.currentUser.token}, isArray:true},
      'get' : {method: 'GET', headers: {'Authorization': 'Token ' + $rootScope.currentUser.token}},
      'create' : {method: 'POST', headers: {'Authorization': 'Token ' + $rootScope.currentUser.token}},
      'update' : {method: 'PUT', headers: {'Authorization': 'Token ' + $rootScope.currentUser.token}},
      'delete' : {method: 'DELETE', headers: {'Authorization': 'Token ' + $rootScope.currentUser.token}},
    }
    );
}]);

app.factory('Aliases', ['$resource', '$rootScope', function($resource, $rootScope){
  return $resource(
    '/api/domains/:domain/aliases/:alias',
    null, 
    {
      'query' : {method: 'GET', headers: {'Authorization': 'Token ' + $rootScope.currentUser.token}, isArray:true},
      'get' : {method: 'GET', headers: {'Authorization': 'Token ' + $rootScope.currentUser.token}},
      'create' : {method: 'POST', headers: {'Authorization': 'Token ' + $rootScope.currentUser.token}},
      'update' : {method: 'PUT', headers: {'Authorization': 'Token ' + $rootScope.currentUser.token}},
      'delete' : {method: 'DELETE', headers: {'Authorization': 'Token ' + $rootScope.currentUser.token}},
    }
    );
}]);

app.factory('MailboxPasswords', ['$resource', '$rootScope', function($resource, $rootScope){
  return $resource(
    '/api/domains/:domain/mailboxes/:mailbox/password',
    null, 
    {
      'update' : {method: 'PUT', headers: {'Authorization': 'Token ' + $rootScope.currentUser.token}}
    }
    );
}]);