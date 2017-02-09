var app = angular.module('PriceOMeterApp', ['ngAnimate', 'ngSanitize', 'ui.bootstrap', 'ngMaterial']);

app.service('http', ['$http', '$q', function($http, $q) {
    this.get = function(url){
      var deferred = $q.defer();

      $http({
        method : "GET",
        url : url
      }).then(function mySucces(response) {
          deferred.resolve(response.data);
      }, function myError(response) {
          deferred.reject(response.statusText);
      });

      return deferred.promise;
    };
}]);

app.controller('PriceOMeterController',['$scope', 'http', function($scope, http) {
  $scope.products = [];

  $scope.prices = [];

  $scope.currentNavItem = 'productLST';

  http.get("http://price-o-meter.local:5000/products").then(function(data){
    for(var prop in data){
      $scope.products.push(data[prop]);
    }
  });

}]);
