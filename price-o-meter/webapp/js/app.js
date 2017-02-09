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
  $scope.products_columns = ['ID', 'Name', 'Category', 'Date Added', 'Date Updated', 'Date Removed'];
  $scope.products = [];
  $scope.product_current_columns = $scope.products_columns.concat(["Attributes"]);
  $scope.product_current;
  $scope.product_current_id = -1;

  $scope.prices = [];

  $scope.currentNavItem = 'productLST';

  $scope.getProduct = function(product_id) {
    console.log(product_id);
    for (var index in $scope.products) {
      product = $scope.products[index];
      if (product.id == product_id) {
        $scope.product_current = product;
      }
    }
  };

  http.get("http://price-o-meter.local:5000/products").then(function(data){
    for(var prop in data){
      $scope.products.push(data[prop]);
    }
  });

}]);
