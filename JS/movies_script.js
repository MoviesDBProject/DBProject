var MoviesApp = angular.module('MoviesApp', ['ui.bootstrap']);


MoviesApp.controller('mainController', function($scope,$http) {

    $scope.actors  = [
                        {name:"dan", year:1995, country: "Israel"},
                        {name:"tomer",year:1990, country: "USA"},
                        {name:"dror",year:1780, country: "UK"}
    ];


    $scope.ActorSelected = function(){
        return !($scope.selected_actor === undefined);
    }

});

