var MoviesApp = angular.module('MoviesApp', ['ui.bootstrap']);

MoviesApp.controller('mainController',['$scope','$http','$sce','$window', function($scope,$http,$sce,$window) {



    $scope.update = function(){

        $http({
            url: "/update/" ,
            method: "GET",
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
           })
            .then(function (response) {
                if (response.data.status == "OK") {
                    $window.alert("Update Request sent. Updating DB.");
                }
            })

    };

    $scope.init = function(){
        var entries = ["actors","directors","language","country","genres"];

        for (var i=0; i<entries.length;i++) {
            $http({
            url: "/init_data/" ,
            method: "POST",
            data: {'entry':entries[i]},
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
           })
           .then(function successCallback(response) {
               var response_data = response.data;
               var entry = Object.keys(response_data[0])[0]
               switch (entry) {
               	   	
                   case "actor" :
                        $scope.actors = response_data;
                       break;
                   case "director" :
                        $scope.directors = response_data;
                       break;
                   case "language" :
                       $scope.languages = response_data;
                       break;
                   case "country" :
                       $scope.countries = response_data;
                       break;
                   case "genre" :
                       $scope.genres = response_data;
                   default:
                       break;
               }
           },
           function errorCallback(response){
               if (response.status == 404) {
                   var landingUrl = "http://" + $window.location.host + "/404";
                    $window.location.href = landingUrl;
               }
           })
        }};

    $scope.init();

    $scope.createYouTubePlaylist = function(youtube_id_list){
        //var youtube_id_list = ["JNfRQ4NBjUU", "X2i9Zz_AqTg"];
        var youtube_url_str = "https://www.youtube.com/embed/VIDEO_ID?playlist=";
        for (var i = 0; i < youtube_id_list.length; i++){
            youtube_url_str = youtube_url_str + youtube_id_list[i];
            if (i < youtube_id_list.length - 1) {
                youtube_url_str += ",";
            }
        };
        return $sce.trustAsResourceUrl(youtube_url_str);

    };

    $scope.submit = function(){

        $http({
            url: "/fetch_results/",
            method: "POST",
            data: $scope.formData,
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        })
        .then(function(response){
            $scope.results_contents = response.data;
            var id_list = function(data) {
                                var lst = [];
                                for (var i=0 ; i<data.length;i++){
                                    lst.push(data[i]["youtube_id"]);
                                }
                                return lst;
                            }($scope.results_contents);
            $scope.youtube_url = createYouTubePlaylist(id_list);
            $scope.showResults = true;
            /*
            results_element.removeChild(document.getElementById("results_table"));
            var results_table = document.createElement("table");
            results_table.setAttribute("id", "results_table");
            results_element.appendChild(results_table);
            */

        } , function errorCallback(response){
               if (response.status == 404) {
                   var landingUrl = "http://" + $window.location.host + "/404";
                    $window.location.href = landingUrl;
               }
           })
    };

    /* Trailer and its description related functions */
    
    
    $scope.showResults = true;
    $scope.results_contents= [{'name':'Criminal','actor':"Gal Gadot", "rating":7, "youtube_id":"JNfRQ4NBjUU"},
                              {'name':"Batman Vs. Superman", 'actor':"Ben Aflek","rating":4,"youtube_id":"X2i9Zz_AqTg"}];


    $scope.youtube_url = $sce.trustAsResourceUrl("https://www.youtube.com/embed/VIDEO_ID?playlist=JNfRQ4NBjUU,X2i9Zz_AqTg");

    document.getElementById('youtube_iframe').src = $scope.youtube_url;


     $scope.disable_next_button = function(){
        document.getElementById("next").setAttribute("class", "btn btn-primary disabled");
        $scope.next_disabled = 1;
    };

    $scope.disable_previous_button = function(){
        document.getElementById("previous").setAttribute("class", "btn btn-primary disabled");
        $scope.previous_disabled = 1;
    };

    $scope.enable_next_button = function(){
        document.getElementById("next").setAttribute("class", "btn btn-primary");
        $scope.next_disabled = 0;
    };

    $scope.enable_previous_button = function(){
        document.getElementById("previous").setAttribute("class", "btn btn-primary");
        $scope.previous_disabled = 0;
    };

    $scope.click_next = function(){
        $scope.show_item++;
        if ($scope.show_item > 0)
            $scope.enable_previous_button();
        if ($scope.show_item == $scope.results_contents.length - 1)
            $scope.disable_next_button();
    };

    $scope.click_previous = function() {
        $scope.show_item--;
        if ($scope.show_item == 0)
           $scope.disable_previous_button();
        if ($scope.show_item < $scope.results_contents.length - 1)
            $scope.enable_next_button();
    };

    $scope.show_item = 0;
    $scope.previous_disabled = 1;
    $scope.next_disabled = 0;
    if ($scope.results_contents.length < 2)
        $scope.disable_next_button();
    $scope.disable_previous_button();


    //document.getElementById("debug").innerHTML = $scope.results_cols.indexOf("Actor").toString();


}]);

