"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { useRouter } from "next/navigation";

// Define user type
export interface User {
  id: string;
  email: string;
  display_name: string;
  profile_image_url?: string;
  created_at: string;
  updated_at: string;
}

// Define auth context type
interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, displayName: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<boolean>;
}

// Create auth context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// API URL
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Auth provider props
interface AuthProviderProps {
  children: ReactNode;
}

// Auth provider component
export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const router = useRouter();

  // Check if user is authenticated
  const isAuthenticated = !!user && !!token;

  // Initialize auth state from localStorage on mount
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const storedToken = localStorage.getItem("token");
        const storedUser = localStorage.getItem("user");

        if (storedToken && storedUser) {
          setToken(storedToken);
          setUser(JSON.parse(storedUser));
          
          // Verify token is still valid
          const isValid = await refreshToken();
          if (!isValid) {
            // Token is invalid, clear auth state
            await logout();
          }
        }
      } catch (error) {
        console.error("Error initializing auth:", error);
        // Clear potentially corrupted auth state
        localStorage.removeItem("token");
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("user");
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, []);

  // Login function
  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      // Create form data for OAuth2 password flow
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);
      formData.append("grant_type", "password");

      const response = await fetch(`${API_URL}/api/auth/token`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Login failed");
      }

      const data = await response.json();
      
      // Store tokens
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("refreshToken", data.refresh_token);
      setToken(data.access_token);

      // Fetch user profile
      const userResponse = await fetch(`${API_URL}/api/users/me`, {
        headers: {
          Authorization: `Bearer ${data.access_token}`,
        },
      });

      if (!userResponse.ok) {
        throw new Error("Failed to fetch user profile");
      }

      const userData = await userResponse.json();
      localStorage.setItem("user", JSON.stringify(userData));
      setUser(userData);

      // Redirect to home page
      router.push("/");
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Register function
  const register = async (email: string, displayName: string, password: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          display_name: displayName,
          password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Registration failed");
      }

      const data = await response.json();
      
      // Store token and user data
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user", JSON.stringify(data));
      setToken(data.access_token);
      setUser(data);

      // Redirect to home page
      router.push("/");
    } catch (error) {
      console.error("Registration error:", error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Logout function
  const logout = async () => {
    try {
      const refreshToken = localStorage.getItem("refreshToken");
      
      if (token && refreshToken) {
        // Call logout API
        await fetch(`${API_URL}/api/auth/logout`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ refresh_token: refreshToken }),
        });
      }
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      // Clear auth state regardless of API success
      localStorage.removeItem("token");
      localStorage.removeItem("refreshToken");
      localStorage.removeItem("user");
      setToken(null);
      setUser(null);
      router.push("/login");
    }
  };

  // Refresh token function
  const refreshToken = async (): Promise<boolean> => {
    try {
      const refreshToken = localStorage.getItem("refreshToken");
      
      if (!refreshToken) {
        return false;
      }

      const response = await fetch(`${API_URL}/api/auth/refresh`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });

      if (!response.ok) {
        return false;
      }

      const data = await response.json();
      
      // Update tokens
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("refreshToken", data.refresh_token);
      setToken(data.access_token);
      
      return true;
    } catch (error) {
      console.error("Token refresh error:", error);
      return false;
    }
  };

  // Create context value
  const contextValue: AuthContextType = {
    user,
    token,
    isLoading,
    isAuthenticated,
    login,
    register,
    logout,
    refreshToken,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook to use auth context
export function useAuth() {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  
  return context;
} 