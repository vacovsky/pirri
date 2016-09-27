(function() {
    var app = angular.module('pirriweb', []);
    app.Root = '/';
    app.config(['$interpolateProvider',
        function($interpolateProvider) {
            $interpolateProvider.startSymbol('{[');
            $interpolateProvider.endSymbol(']}');
        }
    ]); 

    app.controller('PirriControl', function ($rootScope, $scope, $http) {
        $scope.color = "random"
        $scope.colors = [];
        $scope.brightness = 1;
        $scope.length = 630;

        $scope.publishChange = function() {
            var queryString = "";
            $http.get('/send?' + queryString)
            .success(function(data, status, headers, config) {
            })
            .error(function(data, status, headers, config) {})
        };

        $scope.send = function() {
            $scope.publishChange();
        };

        $scope.loadStations = function() {
            $http.get('/stations/load')
            .success(function(data, status, headers, config) {
                
            })
            .error(function(data, status, headers, config) {})
        };

    });
})();