import { NextResponse } from 'next/server';

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

export async function GET() {
  // Initialize results object
  const results: ServiceResults = {
    auth: { status: 'pending', data: null, error: null },
    chat: { status: 'pending', data: null, error: null },
    notification: { status: 'pending', data: null, error: null },
    apiGateway: { status: 'pending', data: null, error: null }
  };

  try {
    // Test Auth Service
    try {
      const authResponse = await fetch('http://auth-service:8000/api/health');
      const authData = await authResponse.json();
      results.auth = { status: 'success', data: authData, error: null };
    } catch (error: any) {
      console.error('Auth service error:', error);
      results.auth = { status: 'error', data: null, error: error.message };
    }

    // Test Chat Service
    try {
      const chatResponse = await fetch('http://chat-service:8000/api/health');
      const chatData = await chatResponse.json();
      results.chat = { status: 'success', data: chatData, error: null };
    } catch (error: any) {
      console.error('Chat service error:', error);
      results.chat = { status: 'error', data: null, error: error.message };
    }

    // Test Notification Service
    try {
      const notificationResponse = await fetch('http://notification-service:8000/api/health');
      const notificationData = await notificationResponse.json();
      results.notification = { status: 'success', data: notificationData, error: null };
    } catch (error: any) {
      console.error('Notification service error:', error);
      results.notification = { status: 'error', data: null, error: error.message };
    }

    // Test API Gateway
    try {
      const apiGatewayResponse = await fetch('http://api-gateway/api/health');
      const apiGatewayData = await apiGatewayResponse.json();
      results.apiGateway = { status: 'success', data: apiGatewayData, error: null };
    } catch (error: any) {
      console.error('API Gateway error:', error);
      results.apiGateway = { status: 'error', data: null, error: error.message };
    }

    return NextResponse.json(results);
  } catch (error: any) {
    console.error('Error in test-cors API route:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
} 