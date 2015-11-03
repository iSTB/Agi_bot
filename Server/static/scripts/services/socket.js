'use strict';

angular.module('webApp')
    .factory('socket', function (socketFactory) {
        var socket = socketFactory({
            ioSocket: io.connect('/control')
        });
        socket.forward('error');
        return socket;
    })
    .factory('socket_test', function (socketFactory) {
        var socketa = socketFactory({
            ioSocket: io.connect('/control_background')
        });
        socketa.forward('error');
        return socketa;
    });
