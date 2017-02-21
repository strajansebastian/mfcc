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


app.controller('PriceOMeterProductLocationController', ['$scope', 'http', function($scope, http) {
  $scope.current_nav_item = 'productLocationLST';

  $scope.product_locations_columns = ['Product ID', 'Product Location ID', 'Site Name', 'Site URL', 'Site Full URL', 'Date Added', 'Date Removed'];
  $scope.product_locations = [];

  $scope.productInsert = {
    'product_id': null,
    'product_location_id': null,
    'site_name': null,
    'site_url': null,
    'result': null
  };

  $scope.insertProduct = function(product_name, product_category, product_attributes) {
    var url = "http://price-o-meter.local:5000/product_location?";
    url = url + "name=" + product_name + "&";
    url = url + "category=" + product_category + "&";
    url = url + "attributes=" + product_attributes;

    http.put(url, {}).then(function(data) {
      var json_data = JSON.parse(data);
      $scope.productInsert.result = "Status of add operation is: " + json_data['inserted_status'] + "'. The operation affected " + json_data['inserted_row_number'] + " row(s)!";
    });
  };

  http.get("http://price-o-meter.local:5000/product_location").then(function(data) {
    for(var prop in data){
      $scope.product_locations.push(data[prop]);
    }
    console.log($scope.product_locations);
  });

}]);


