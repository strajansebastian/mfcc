var app = angular.module('PriceOMeterApp', ['ngAnimate', 'ngSanitize', 'ui.bootstrap', 'ngMaterial']);

app.service('http', ['$http', '$q', function($http, $q) {
    this.get = function(url, data){
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

    this.put = function(url, data){
      var deferred = $q.defer();

      $http({
        method : "PUT",
        url : url,
        data : data
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

  $scope.productAdd = {
    'name': undefined,
    'category': undefined,
    'attributes': "{}"
  }

  $scope.productUpdate = {
    'id': undefined,
    'category': undefined,
    'attributes': "{}"
  }

  $scope.productDelete = {
    'id': undefined
  }

  $scope.prices = [];

  $scope.currentNavItem = 'productLST';

  $scope.getProduct = function(product_id) {
    for (var index in $scope.products) {
      product = $scope.products[index];
      if (product.id == product_id) {
        $scope.product_current = product;
      }
    }
  };

  $scope.addProduct = function(product_name, product_category, product_attributes) {
    var url = "http://price-o-meter.local:5000/product_add?";
    url = url + "name=" + product_name + "&"
    url = url + "category=" + product_category + "&"
    // url = url + "attributes=" + product_attributes 
    var put_data = {
      'name': product_name,
      'category': product_category,
      'attributes': product_attributes
    };

    http.get(url).then(function(data){
      for(var prop in data){
        console.log("works:", data[prop]);
      }
    });
    console.log("add", product_name, product_category, product_attributes);
  };

  $scope.updateProduct = function(product_id, product_category, product_attributes) {
    console.log("update", product_id, product_category, product_attributes);
  };

  $scope.deleteProduct = function(product_id) {
    console.log("delete", product_id);
  };

  http.get("http://price-o-meter.local:5000/products").then(function(data){
    for(var prop in data){
      $scope.products.push(data[prop]);
    }
  });

}]);
