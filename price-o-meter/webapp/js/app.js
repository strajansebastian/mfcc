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

    this.put = function(url, data, config){
      var deferred = $q.defer();

      $http({
        method : "PUT",
        url : url,
        headers: {
          'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'
        },
        data : data
      }).then(function mySucces(response) {
          deferred.resolve(response.data);
      }, function myError(response) {
          deferred.reject(response.statusText);
      });

      return deferred.promise;
    };

    this.post = function(url, data, config){
      var deferred = $q.defer();

      $http({
        method : "POST",
        url : url,
        headers: {
          'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'
        },
        data : data
      }).then(function mySucces(response) {
          deferred.resolve(response.data);
      }, function myError(response) {
          deferred.reject(response.statusText);
      });

      return deferred.promise;
    };

    this.delete = function(url, data, config){
      var deferred = $q.defer();

      $http({
        method : "DELETE",
        url : url,
        headers: {
          'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'
        },
        data : data
      }).then(function mySucces(response) {
          deferred.resolve(response.data);
      }, function myError(response) {
          deferred.reject(response.statusText);
      });

      return deferred.promise;
    };
}]);




app.controller('PriceOMeterController', ['$scope', 'http', '$timeout', function($scope, http, $timeout) {
  $scope.currentNavItem = 'productLST';

  $scope.products_columns = ['ID', 'Name', 'Category', 'Date Added', 'Date Updated', 'Date Removed'];
  $scope.products = [];
  $scope.product_current_columns = $scope.products_columns.concat(["Attributes"]);
  $scope.product_current;
  $scope.product_current_id = -1;
  $scope.edit_button_status = "disabled";
  $scope.edit_button_text = "NanA!";

  var vm = this;
  vm.product_current_id = $scope.product_current_id;
  vm.product_current = $scope.product_current;

  $scope.productInsert = {
    'name': null,
    'category': null,
    'attributes': "{}",
    'result': null
  };

  $scope.productUpdate = {
    'id': -1,
    'category': null,
    'attributes': "{}",
    'result': null
  };

  $scope.productDelete = {
    'id': null,
    'result': null
  };

  $scope.prices = [];

  $scope.getProduct = function() {
    console.log('get_Product ', $scope.productUpdate.id);
    var fin_result = "The provided ID (" + $scope.productUpdate.id + ") is not available! Please try another one!";
    for (var index in $scope.products) {
      product = $scope.products[index];
      if (product.id == $scope.productUpdate.id) {
        $scope.product_current = product;
        $scope.productUpdate.id = product.id;
        $scope.productUpdate.cateogry = product.category;
        $scope.productUpdate.attributes = product.attributes;
        $scope.edit_button_status = false;
        $scope.edit_button_text = "update product info";
        fin_result = "Found product with ID="  + $scope.productUpdate.id + "! Proceed with update process!";
      }
    }
    $scope.productUpdate.result = fin_result;
  };

  $scope.insertProduct = function(product_name, product_category, product_attributes) {
    var url = "http://price-o-meter.local:5000/product?";
    url = url + "name=" + product_name + "&";
    url = url + "category=" + product_category + "&";
    url = url + "attributes=" + product_attributes;

    http.put(url, {}).then(function(data) {
      var json_data = JSON.parse(data);
      $scope.productInsert.result = "The status of the add operation for product='" + product_name + "' is '" + json_data['inserted_status'] + "'. The operation affected " + json_data['inserted_row_number'] + " row(s)!";
    });
  };

  $scope.showProduct = function() {
    console.log("show", vm.product_current_id);
  };

  $scope.updateProduct = function() {
    var product_id = $scope.productUpdate.id;
    var product_category = $scope.productUpdate.category;
    var product_attributes = $scope.productUpdate.attributes;

    // find a way to serialize this SHIT, or post it in another way
    product_attributes = "{}";

    var url = "http://price-o-meter.local:5000/product?";
    url = url + "id=" + product_id + "&";
    url = url + "category=" + product_category + "&";
    url = url + "attributes=" + product_attributes;

    http.post(url, {}).then(function(data){
      var json_data = JSON.parse(data);
      $scope.productUpdate.result = "The status of the update operation for product ID='" + product_id + "' is '" + json_data['updated_status'] + "'. The operation affected " + json_data['updated_row_number'] + " row(s)!";
    });
  };

  $scope.deleteProduct = function(product_id) {
    var url = "http://price-o-meter.local:5000/product?id=" + product_id;

    http.delete(url, {}).then(function(data){
      var json_data = JSON.parse(data);
      $scope.productDelete.result = "The status of the delete operation for product with id=" + product_id + " is '" + json_data['deleted_status'] + "'. The operation affected " + json_data['deleted_row_number'] + " row(s)!";
    });
  };

  http.get("http://price-o-meter.local:5000/product").then(function(data){
    for(var prop in data){
      $scope.products.push(data[prop]);
    }
  });

}]);

app.controller('PriceOMeterPricesController', ['$scope', 'http', function($scope, http, $timeout) {
  http.get("http://price-o-meter.local:5000/product_price").then(function(data){
    console.log(data);
  });
}]);


