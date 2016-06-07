var MoviesApp = angular.module('MoviesApp', ['ui.bootstrap']);

MoviesApp.controller('mainController',['$scope','$http','$sce','$window', function($scope,$http,$sce,$window) {


    $scope.$on('$routeChangeSuccess', function () {
        var entries = ["actors","directors","languages","countries"];

        entries.forEach(function (entry_name) {
            $http({
            url: "/get_" + entry_name + "/" ,
            method: "GET",
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
           })
           .then(function successCallback(response) {
               var response_data = JSON.stringify(response.data);
               switch (entry_name) {
                   case "actors" :
                        $scope.actors = response_data;
                       break;
                   case "directors" :
                        $scope.directors = response_data;
                       break;
                   case "languages" :
                       $scope.languages = response_data;
                       break;
                   case "countries" :
                       $scope.countries = response_data;
                       break;
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
        })


    });


    $scope.actors  = [
                        {name:"dan", year:1995, country: "Israel"},
                        {name:"tomer",year:1990, country: "USA"},
                        {name:"dror",year:1780, country: "UK"}
    ];

    $scope.countries = ["Afghanistan", "Albania", "Algeria",
        "American Samoa", "Angola", "Anguilla", "Antartica",
        "Antigua and Barbuda", "Argentina",
        "Armenia", "Aruba", "Ashmore and Cartier Island",
        "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh",
        "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia",
        "Bosnia and Herzegovina", "Botswana", "Brazil", "British Virgin Islands", "Brunei", "Bulgaria",
        "Burkina Faso", "Burma", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Cayman Islands",
        "Central African Republic", "Chad", "Chile", "China", "Christmas Island", "Clipperton Island", "Cocos (Keeling) Islands",
        "Colombia", "Comoros", "Congo, Democratic Republic of the", "Congo, Republic of the", "Cook Islands", "Costa Rica", "Cote d'Ivoire",
        "Croatia", "Cuba", "Cyprus", "Czeck Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt",
        "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Europa Island", "Falkland Islands (Islas Malvinas)",
        "Faroe Islands", "Fiji", "Finland", "France", "French Guiana", "French Polynesia", "French Southern and Antarctic Lands", "Gabon",
        "Gambia, The", "Gaza Strip", "Georgia", "Germany", "Ghana", "Gibraltar", "Glorioso Islands", "Greece", "Greenland", "Grenada",
        "Guadeloupe", "Guam", "Guatemala", "Guernsey", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Heard Island and McDonald Islands",
        "Holy See (Vatican City)", "Honduras", "Hong Kong", "Howland Island", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq",
        "Ireland", "Ireland, Northern", "Israel", "Italy", "Jamaica", "Jan Mayen", "Japan", "Jarvis Island", "Jersey", "Johnston Atoll",
        "Jordan", "Juan de Nova Island", "Kazakhstan", "Kenya", "Kiribati", "Korea, North", "Korea, South", "Kuwait", "Kyrgyzstan", "Laos",
        "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau", "Macedonia," +
        "Former Yugoslav Republic", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Man, Isle of", "Marshall Islands",
        "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia, Federated States of", "Midway Islands", "Moldova",
        "Monaco", "Mongolia", "Montserrat", "Morocco", "Mozambique", "Namibia", "Nauru", "Nepal", "Netherlands", "Netherlands Antilles",
        "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norfolk Island", "Northern Mariana Islands", "Norway",
        "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Pitcaim Islands", "Poland",
        "Portugal", "Puerto Rico", "Qatar", "Reunion", "Romainia", "Russia", "Rwanda", "Saint Helena", "Saint Kitts and Nevis",
        "Saint Lucia", "Saint Pierre and Miquelon", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
        "Saudi Arabia", "Scotland", "Senegal", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands",
        "Somalia", "South Africa", "South Georgia and South Sandwich Islands", "Spain", "Spratly Islands", "Sri Lanka", "Sudan", "Suriname",
        "Svalbard", "Swaziland", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Tobago", "Toga",
        "Tokelau", "Tonga", "Trinidad", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates",
        "United Kingdom", "Uruguay", "USA", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Virgin Islands", "Wales", "Wallis and Futuna",
        "West Bank", "Western Sahara", "Yemen", "Yugoslavia", "Zambia", "Zimbabwe"];


    $scope.languages = ["Hebrew","English","Arabic","French"];

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

    $scope.showResults = true;
    $scope.results_contents= [{'name':'Criminal','actor':"Gal Gadot", "rating":7, "youtube_id":"JNfRQ4NBjUU"},
                              {'name':"Batman Vs. Superman", 'actor':"Ben Aflek","rating":4,"youtube_id":"X2i9Zz_AqTg"}];
    $scope.youtube_url = $sce.trustAsResourceUrl("https://www.youtube.com/embed/VIDEO_ID?playlist=JNfRQ4NBjUU,X2i9Zz_AqTg");


    $scope.submit = function(){

        $http({
            url: "/fetch_results/",
            method: "POST",
            data: $scope.formData,
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        })
        .then(function(response){
            //console.log(response.data);
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

