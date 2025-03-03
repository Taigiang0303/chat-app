'use client';

import { useState, useEffect } from 'react';

interface ServiceResult {
  status: string;
  data: any;
  error: string | null;
}

interface ServiceResults {
  auth: ServiceResult;
  chat: ServiceResult;
  notification: ServiceResult;
  apiGateway: ServiceResult;
}

export default function TestCorsPage() {
  const [clientResults, setClientResults] = useState<Record<string, string>>({
    auth: 'Checking...',
    chat: 'Checking...',
    notification: 'Checking...',
    apiGateway: 'Checking...'
  });
  const [serverResults, setServerResults] = useState<ServiceResults | null>(null);
  const [logs, setLogs] = useState<string[]>([]);

  const addLog = (message: string) => {
    setLogs(prevLogs => {
      const timestamp = new Date().toISOString();
      return [...prevLogs, `[${timestamp}] ${message}`];
    });
  };

  useEffect(() => {
    const testServicesFromClient = async () => {
      addLog('Starting client-side tests...');

      // Test Auth Service
      try {
        addLog('Testing Auth Service from client...');
        const authResponse = await fetch('http://localhost:8001/api/health');
        const authData = await authResponse.json();
        addLog(`Auth Service response: ${JSON.stringify(authData)}`);
        setClientResults(prev => ({
          ...prev,
          auth: 'Success: ' + JSON.stringify(authData)
        }));
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        addLog(`Auth Service error: ${errorMessage}`);
        setClientResults(prev => ({
          ...prev,
          auth: 'Error: ' + errorMessage
        }));
      }

      // Test Chat Service
      try {
        addLog('Testing Chat Service from client...');
        const chatResponse = await fetch('http://localhost:8002/api/health');
        const chatData = await chatResponse.json();
        addLog(`Chat Service response: ${JSON.stringify(chatData)}`);
        setClientResults(prev => ({
          ...prev,
          chat: 'Success: ' + JSON.stringify(chatData)
        }));
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        addLog(`Chat Service error: ${errorMessage}`);
        setClientResults(prev => ({
          ...prev,
          chat: 'Error: ' + errorMessage
        }));
      }

      // Test Notification Service
      try {
        addLog('Testing Notification Service from client...');
        const notificationResponse = await fetch('http://localhost:8003/api/health');
        const notificationData = await notificationResponse.json();
        addLog(`Notification Service response: ${JSON.stringify(notificationData)}`);
        setClientResults(prev => ({
          ...prev,
          notification: 'Success: ' + JSON.stringify(notificationData)
        }));
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        addLog(`Notification Service error: ${errorMessage}`);
        setClientResults(prev => ({
          ...prev,
          notification: 'Error: ' + errorMessage
        }));
      }

      // Test API Gateway
      try {
        addLog('Testing API Gateway from client...');
        const apiGatewayResponse = await fetch('http://localhost:8000/api/health');
        const apiGatewayData = await apiGatewayResponse.json();
        addLog(`API Gateway response: ${JSON.stringify(apiGatewayData)}`);
        setClientResults(prev => ({
          ...prev,
          apiGateway: 'Success: ' + JSON.stringify(apiGatewayData)
        }));
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        addLog(`API Gateway error: ${errorMessage}`);
        setClientResults(prev => ({
          ...prev,
          apiGateway: 'Error: ' + errorMessage
        }));
      }

      addLog('Client-side tests completed.');
    };

    const testServicesFromServer = async () => {
      addLog('Starting server-side tests...');
      try {
        const response = await fetch('/api/test-cors');
        const data = await response.json();
        setServerResults(data);
        addLog(`Server-side tests completed: ${JSON.stringify(data)}`);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        addLog(`Server-side tests error: ${errorMessage}`);
      }
    };

    testServicesFromClient();
    testServicesFromServer();
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">CORS Test Page</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold mb-2">Client-Side Tests</h2>
          <div className="space-y-2">
            <div>
              <span className="font-medium">Auth Service: </span>
              <span className={clientResults.auth.includes('Success') ? 'text-green-600' : 'text-red-600'}>
                {clientResults.auth}
              </span>
            </div>
            <div>
              <span className="font-medium">Chat Service: </span>
              <span className={clientResults.chat.includes('Success') ? 'text-green-600' : 'text-red-600'}>
                {clientResults.chat}
              </span>
            </div>
            <div>
              <span className="font-medium">Notification Service: </span>
              <span className={clientResults.notification.includes('Success') ? 'text-green-600' : 'text-red-600'}>
                {clientResults.notification}
              </span>
            </div>
            <div>
              <span className="font-medium">API Gateway: </span>
              <span className={clientResults.apiGateway.includes('Success') ? 'text-green-600' : 'text-red-600'}>
                {clientResults.apiGateway}
              </span>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold mb-2">Server-Side Tests</h2>
          {serverResults ? (
            <div className="space-y-2">
              <div>
                <span className="font-medium">Auth Service: </span>
                <span className={serverResults.auth.status === 'success' ? 'text-green-600' : 'text-red-600'}>
                  {serverResults.auth.status === 'success' 
                    ? `Success: ${JSON.stringify(serverResults.auth.data)}` 
                    : `Error: ${serverResults.auth.error}`}
                </span>
              </div>
              <div>
                <span className="font-medium">Chat Service: </span>
                <span className={serverResults.chat.status === 'success' ? 'text-green-600' : 'text-red-600'}>
                  {serverResults.chat.status === 'success' 
                    ? `Success: ${JSON.stringify(serverResults.chat.data)}` 
                    : `Error: ${serverResults.chat.error}`}
                </span>
              </div>
              <div>
                <span className="font-medium">Notification Service: </span>
                <span className={serverResults.notification.status === 'success' ? 'text-green-600' : 'text-red-600'}>
                  {serverResults.notification.status === 'success' 
                    ? `Success: ${JSON.stringify(serverResults.notification.data)}` 
                    : `Error: ${serverResults.notification.error}`}
                </span>
              </div>
              <div>
                <span className="font-medium">API Gateway: </span>
                <span className={serverResults.apiGateway.status === 'success' ? 'text-green-600' : 'text-red-600'}>
                  {serverResults.apiGateway.status === 'success' 
                    ? `Success: ${JSON.stringify(serverResults.apiGateway.data)}` 
                    : `Error: ${serverResults.apiGateway.error}`}
                </span>
              </div>
            </div>
          ) : (
            <p>Loading server-side test results...</p>
          )}
        </div>
      </div>

      <div className="mt-6 bg-gray-100 p-4 rounded">
        <h2 className="text-xl font-semibold mb-2">Logs</h2>
        <div className="bg-black text-green-400 p-2 rounded font-mono text-sm h-64 overflow-y-auto">
          {logs.map((log, index) => (
            <div key={index}>{log}</div>
          ))}
        </div>
      </div>
    </div>
  );
} 