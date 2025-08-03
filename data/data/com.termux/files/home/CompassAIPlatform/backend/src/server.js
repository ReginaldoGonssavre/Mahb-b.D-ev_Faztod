const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const authRoutes = require('./routes/auth');
const apiRoutes = require('./routes/api');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

app.use(express.json());

// Basic Routes
app.get('/', (req, res) => {
  res.send('Compass AI Platform Backend is running!');
});

// Auth Routes
app.use('/api/auth', authRoutes);

// API Routes
app.use('/api', apiRoutes);

// WebSocket connection handling
wss.on('connection', ws => {
  console.log('Client connected via WebSocket');
  ws.on('message', message => {
    console.log(`Received: ${message}`);
    ws.send(`Echo: ${message}`);
  });
  ws.on('close', () => console.log('Client disconnected'));
});

// gRPC Server setup (placeholder)
const PROTO_PATH = __dirname + '/grpc/service.proto'; // Define your proto file
const packageDefinition = protoLoader.loadSync(
  PROTO_PATH,
  {keepCase: true,
   longs: String,
   enums: String,
   defaults: true,
   oneofs: true
  });
const protoDescriptor = grpc.loadPackageDefinition(packageDefinition);
const your_service = protoDescriptor.your_package.YourService; // Replace with your package and service name

function sayHello(call, callback) {
  callback(null, { message: 'Hello ' + call.request.name });
}

function getFeature(call, callback) {
  // Implement your gRPC logic here
  callback(null, { name: 'Feature ' + call.request.id, location: { latitude: 0, longitude: 0 } });
}

const grpcServer = new grpc.Server();
grpcServer.addService(your_service.service, { SayHello: sayHello, GetFeature: getFeature }); // Add your service methods
grpcServer.bindAsync('0.0.0.0:50051', grpc.ServerCredentials.createInsecure(), () => {
  grpcServer.start();
  console.log('gRPC server running at grpc://0.0.0.0:50051');
});


const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Backend server running on port ${PORT}`);
});
