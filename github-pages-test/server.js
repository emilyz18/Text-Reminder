const express = require('express');
const server = express();

function api(request, response) {
    response.set('Access-Control-Allow-Origin', '*');
    response.status(200).send("Hello world!");
}

server.use(express.text());
server.all(/.*/, api);

server.listen(8080);