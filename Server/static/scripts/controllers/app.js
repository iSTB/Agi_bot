'use strict';

angular.module('webApp')
    .controller('ChatCtrl', function ($scope, socket) {
        $scope.messages = [];
        $scope.newMessage = '';
        $scope.username = false;
        $scope.inputUsername = '';
        $scope.glued = true;

        socket.forward('message', $scope);
        $scope.$on('socket:message', function (ev, data) {
            if ($scope.messages.length > 100) {
                $scope.messages.splice(0, 1);
            }
            $scope.messages.push(data);
        });

        $scope.sendMessage = function () {
            socket.emit('send_message', {
                message: $scope.newMessage,
                username: $scope.username
            });
            $scope.newMessage = '';
        };

        $scope.setUsername = function () {
            $scope.username = $scope.inputUsername;
            socket.emit('joined_message', {
                'username': $scope.username
            });
        };
    })
    .controller('RobotServerCtrl', function ($scope, socket) {
        //notifications manage
        toastr.options = {
          "closeButton": false,
          "debug": false,
          "newestOnTop": false,
          "progressBar": false,
          "positionClass": "toast-bottom-left",
          "preventDuplicates": false,
          "onclick": null,
          "showDuration": "300",
          "hideDuration": "1000",
          "timeOut": "5000",
          "extendedTimeOut": "1000",
          "showEasing": "swing",
          "hideEasing": "linear",
          "showMethod": "fadeIn",
          "hideMethod": "fadeOut"
        }
        
        $scope.ann_btn = "default";
        $scope.ann_on = false;
        $scope.xbee_on = false;
        $scope.music_on = false;
        
        //messages comming from the server
        //make them alerts
        socket.forward('notification', $scope);
        $scope.$on('socket:notification', function (ev, data) {
            console.log(data);
            toastr.info(data);
            //we can put sync here to change all together
        });
        
        $scope.ann_switch = function(){
            socket.emit('ann',{
                    data: $scope.ann_on
                });
            $scope.ann_on = !$scope.ann_on;
            
        }
        $scope.music_switch = function(){
            socket.emit('music',{
                    data: $scope.music_on
                });
            $scope.music_on = !$scope.music_on;
            
        }
        $scope.xbee_switch = function(){
            socket.emit('xbee',{
                    data: $scope.xbee_on
                });
            $scope.xbee_on = !$scope.xbee_on;
            
        }
    });